"""Documentation consistency tests.

These tests guard against docs/marketing drift from the project metadata in
``pyproject.toml``.
"""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent


def _pyproject_text() -> str:
    return (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")


def _pyproject_version() -> str:
    text = _pyproject_text()
    match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
    assert match, "version not found in pyproject.toml"
    return match.group(1)


def test_docs_conf_release_matches_pyproject_version() -> None:
    """Sphinx ``release`` must stay in sync with the package version."""
    conf_path = PROJECT_ROOT / "docs" / "conf.py"
    spec = importlib.util.spec_from_file_location("docs_conf", conf_path)
    assert spec and spec.loader
    conf = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(conf)
    expected = _pyproject_version()
    assert conf.release == expected, (
        f"docs/conf.py release {conf.release!r} != "
        f"pyproject.toml version {expected!r}"
    )


def test_python_classifiers_match_tested_versions() -> None:
    """Only claim Python versions that the tooling actually targets/tests.

    The project configures black/ruff/mypy for Python 3.13 and CI runs on
    3.13, so claiming 3.14 support via classifier is unverified drift.
    """
    text = _pyproject_text()
    versions = [
        int(v)
        for v in re.findall(r'"Programming Language :: Python :: 3\.(\d+)"', text)
    ]
    assert versions, "no Python 3.x classifiers found in pyproject.toml"
    max_claimed = max(versions)
    assert max_claimed == 13, (
        f"Python 3.{max_claimed} classifier present; "
        "tooling only targets/tests Python 3.13"
    )


def test_readme_python_version_matches_requires_python() -> None:
    """README's stated Python requirement matches ``requires-python``."""
    readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
    pyproject = _pyproject_text()
    requires_match = re.search(r'requires-python\s*=\s*"([^"]+)"', pyproject)
    assert requires_match, "requires-python not found in pyproject.toml"
    assert (
        "Python >= 3.13" in readme
    ), "README Requirements section no longer states Python >= 3.13"
    assert requires_match.group(1) == ">=3.13"
