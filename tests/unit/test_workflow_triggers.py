"""Tests for the main + PR GitHub Actions workflow trigger policy.

The workflows created in T14 are the gate that fires on push to ``main`` and on
pull requests against ``main``. They must follow the agreed trigger policy
(spec § CI/CD):

* ``ci`` / ``coverage`` / ``docs`` fire on ``push: [main]`` AND
  ``pull_request: [main]``
* ``development`` fires on ``pull_request: [main]`` only (no ``push``)
* no workflow references ``dev`` / ``develop`` / ``feature/*`` branches
* ``ci.yml`` matrix is ``unit`` + ``integration`` only (no ``performance`` leg)
* the ``ci`` integration leg uses a ``mysql:8.0`` service container + the
  ``mysql`` extra (never the postgres image/extra this package replaces)
* every workflow is renamed off the ``pg_g4public_orm`` / ``pg-g4public-orm``
  sibling names and contains no postgres references
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

try:
    import yaml
except ImportError:
    pytest.skip("PyYAML not available", allow_module_level=True)

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS_DIR = ROOT / ".github" / "workflows"

# Workflows created in this task.
WORKFLOWS = ["ci.yml", "coverage.yml", "docs.yml", "development.yml"]

# Branch names that must never appear in any workflow trigger.
FORBIDDEN_BRANCHES = {"dev", "develop"}


def _load_workflow(name: str) -> dict:
    path = WORKFLOWS_DIR / name
    assert path.is_file(), f"Missing workflow: .github/workflows/{name}"
    with path.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    assert isinstance(data, dict), f"{name} did not parse to a mapping"
    return data


def _on_section(data: dict) -> dict:
    """Return the ``on:`` trigger mapping.

    PyYAML parses the YAML 1.1 truthy key ``on`` as the boolean ``True``, so try
    both spellings.
    """
    on = data.get("on")
    if on is None:
        on = data.get(True)  # type: ignore[call-overload]
    assert isinstance(on, dict), "workflow has no `on:` trigger mapping"
    return on


def _branches(on: dict, trigger: str) -> list[str]:
    section = on.get(trigger)
    if section is None:
        return []
    if isinstance(section, list):
        return [str(b) for b in section]
    if isinstance(section, dict):
        return [str(b) for b in section.get("branches", [])]
    return []


def _collect_run_text(jobs: dict) -> str:
    chunks: list[str] = []
    for job in jobs.values():
        for step in job.get("steps") or []:
            run = step.get("run")
            if run:
                chunks.append(run)
    return "\n".join(chunks)


def test_workflows_readme_exists() -> None:
    assert (
        WORKFLOWS_DIR / "README.md"
    ).is_file(), "Missing .github/workflows/README.md"


def test_ci_triggers_push_and_pull_request_on_main() -> None:
    on = _on_section(_load_workflow("ci.yml"))
    assert _branches(on, "push") == ["main"]
    assert _branches(on, "pull_request") == ["main"]


def test_coverage_triggers_push_and_pull_request_on_main() -> None:
    on = _on_section(_load_workflow("coverage.yml"))
    assert _branches(on, "push") == ["main"]
    assert _branches(on, "pull_request") == ["main"]


def test_docs_triggers_push_and_pull_request_on_main() -> None:
    on = _on_section(_load_workflow("docs.yml"))
    assert _branches(on, "push") == ["main"]
    assert _branches(on, "pull_request") == ["main"]


def test_development_triggers_pull_request_only() -> None:
    on = _on_section(_load_workflow("development.yml"))
    assert _branches(on, "pull_request") == ["main"]
    assert "push" not in on, "development.yml must not fire on push"


@pytest.mark.parametrize("name", WORKFLOWS)
def test_no_workflow_references_forbidden_branches(name: str) -> None:
    on = _on_section(_load_workflow(name))
    seen: list[str] = []
    for trigger in ("push", "pull_request"):
        seen.extend(_branches(on, trigger))
    for branch in seen:
        assert (
            branch not in FORBIDDEN_BRANCHES
        ), f"{name}: forbidden branch {branch!r} in trigger"
        assert not branch.startswith(
            "feature/"
        ), f"{name}: forbidden feature/* branch {branch!r} in trigger"


def test_ci_matrix_is_unit_and_integration_only() -> None:
    data = _load_workflow("ci.yml")
    matrix_keys: list[str] = []
    for job in data.get("jobs", {}).values():
        include = (job.get("strategy", {}).get("matrix") or {}).get("include")
        if include:
            for entry in include:
                # pg-g4public uses a `matrix:` discriminator key per entry.
                if isinstance(entry, dict) and "matrix" in entry:
                    matrix_keys.append(str(entry["matrix"]))
            break
    assert set(matrix_keys) == {
        "unit",
        "integration",
    }, f"ci.yml matrix must be {{unit, integration}}; got {set(matrix_keys)!r}"
    assert "performance" not in matrix_keys


def test_ci_integration_leg_uses_mysql_service_and_extra() -> None:
    data = _load_workflow("ci.yml")
    jobs = data.get("jobs", {})
    assert jobs, "ci.yml declares no jobs"

    # 1. A mysql:8.0 service container is declared on some job.
    images: list[str] = []
    for job in jobs.values():
        for svc in (job.get("services") or {}).values():
            img = svc.get("image")
            if img:
                images.append(str(img))
    assert any(
        i == "mysql:8.0" for i in images
    ), f"ci.yml must declare a mysql:8.0 service; found images={images!r}"

    # 2. The install steps use the `mysql` extra, never the postgres one.
    run_text = _collect_run_text(jobs)
    assert (
        "postgres" not in run_text.lower()
    ), f"ci.yml must not reference postgres; run text:\n{run_text}"
    assert re.search(
        r"\[\s*[^\]]*\bmysql\b", run_text
    ), f"ci.yml must install the mysql extra; run text:\n{run_text}"


@pytest.mark.parametrize("name", WORKFLOWS)
def test_workflows_renamed_off_pg_sibling_and_no_postgres(name: str) -> None:
    text = (WORKFLOWS_DIR / name).read_text(encoding="utf-8")
    assert "pg_g4public_orm" not in text, f"{name}: still references pg_g4public_orm"
    assert "pg-g4public-orm" not in text, f"{name}: still references pg-g4public-orm"
    assert (
        "postgres" not in text.lower()
    ), f"{name}: must not reference postgres (this is the MySQL edition)"