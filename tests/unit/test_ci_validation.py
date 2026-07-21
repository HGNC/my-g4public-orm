"""CI validation gate — actionlint + dry-run release over real git history.

T16 locks in the CI/CD machinery built by T12–T15. It closes two gaps the rest
of the unit suite does *not* cover:

* **actionlint** performs the full *semantic* validation of every workflow that
  YAML structural parsing cannot — invalid action references, missing required
  fields, malformed ``${{ }}`` expressions, shell-injection patterns, and so on.
  The trigger tests in ``test_workflow_triggers.py`` only inspect the parsed
  YAML shape; they cannot catch these.
* the **release scripts run end-to-end over the *real* git history** of this
  repository. ``test_release_scripts.py`` exercises the scripts against a
  throwaway temp repo; here ``analyze_commits.py --range HEAD`` walks the actual
  commit graph and ``determine_version_bump.py`` consumes the result.

Together these mirror the project's ship-gate command (spec T16 Verify)::

    actionlint && \
    python .github/scripts/analyze_commits.py --range HEAD --output a.json && \
    python .github/scripts/determine_version_bump.py a.json

so a regression in workflow syntax or the release pipeline fails the unit
matrix *before* the first push to ``main``.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS_DIR = ROOT / ".github" / "workflows"
SCRIPTS_DIR = ROOT / ".github" / "scripts"

# Every value ``determine_version_bump.py`` is allowed to emit.
VALID_BUMP_TYPES = {"major", "minor", "patch", "none"}

# ``actionlint-py`` (a declared test dependency) ships a prebuilt
# ``actionlint`` binary on PATH inside the venv; that is also what the spec's
# ship-gate command invokes via ``uvx actionlint``.
ACTIONLINT_BIN: str | None = shutil.which("actionlint")


@pytest.mark.skipif(
    ACTIONLINT_BIN is None, reason="actionlint not installed (install actionlint-py)"
)
def test_all_workflows_pass_actionlint() -> None:
    """actionlint must report zero errors across every workflow.

    This is the semantic check the YAML-structure tests cannot perform: it
    validates action references, required fields, expression syntax, and
    runner/shell usage for real GitHub Actions.
    """
    assert ACTIONLINT_BIN is not None  # narrows for the type-checker
    workflows = sorted(
        [*WORKFLOWS_DIR.glob("*.yml"), *WORKFLOWS_DIR.glob("*.yaml")],
        key=lambda p: p.name,
    )
    assert workflows, "no workflow files found under .github/workflows"

    result = subprocess.run(
        [ACTIONLINT_BIN, *(str(w) for w in workflows)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (
        "actionlint reported errors:\n" f"{result.stdout}\n{result.stderr}"
    )


def test_release_scripts_run_end_to_end_over_real_history(tmp_path: Path) -> None:
    """The release pipeline must run cleanly over this repo's real history.

    ``analyze_commits.py --range HEAD`` walks the actual commit graph (not the
    temp repo used in ``test_release_scripts.py``) and ``determine_version_bump``
    must consume that analysis without error and emit a valid semver bump.
    """
    analysis_path = tmp_path / "analysis.json"

    analyze = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS_DIR / "analyze_commits.py"),
            "--range",
            "HEAD",
            "--output",
            str(analysis_path),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert (
        analyze.returncode == 0
    ), f"analyze_commits.py failed:\n{analyze.stdout}\n{analyze.stderr}"
    assert analysis_path.is_file(), "analyze_commits.py did not write its output"

    analysis = json.loads(analysis_path.read_text(encoding="utf-8"))
    stats = analysis.get("stats", {})
    for key in ("total_commits", "breaking_changes", "features", "fixes"):
        assert key in stats, f"analysis.stats missing required key {key!r}"
    # Real history was walked, not an empty/temp repo.
    assert stats["total_commits"] > 0, (
        "analyze_commits.py reported zero commits over HEAD; "
        "real history was not walked"
    )

    determine = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS_DIR / "determine_version_bump.py"),
            str(analysis_path),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert (
        determine.returncode == 0
    ), f"determine_version_bump.py failed:\n{determine.stdout}\n{determine.stderr}"
    assert determine.stdout.strip() in VALID_BUMP_TYPES, (
        f"determine_version_bump.py returned an invalid bump type: "
        f"{determine.stdout!r}"
    )
