import subprocess
import sys
from pathlib import Path


def test_docs_build() -> None:
    """Test that docs build without warnings."""
    docs_dir = Path(__file__).parent.parent.parent / "docs"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "sphinx",
            "-W",
            "-b",
            "html",
            str(docs_dir),
            str(docs_dir / "_build" / "html"),
        ],
        cwd=docs_dir,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, (
        "Docs build failed "
        f"with return code {result.returncode}\n"
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )
