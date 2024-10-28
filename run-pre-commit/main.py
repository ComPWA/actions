"""Determine which pre-commit hooks should be skipped."""

# /// script
# dependencies = ["rtoml"]
# ///
from pathlib import Path

import rtoml


def main() -> None:
    cmd = _get_uv_run_command()
    print(cmd)


def _get_uv_run_command() -> str:
    pyproject_path = Path("pyproject.toml")
    if pyproject_path.is_file():
        pyproject = rtoml.load(pyproject_path)
        dependency_groups = pyproject.get("dependency-groups")
        candidate_groups = [
            "style",
            "sty",
            "lint",
        ]
        if dependency_groups is not None:
            for group in candidate_groups:
                if group in dependency_groups:
                    return f"uv run --group {group} --no-dev"
        extras = pyproject.get("project", {}).get("optional-dependencies")
        if extras is not None:
            for extra in candidate_groups:
                if extra in extras:
                    return f"uv run --extra {extra} --no-dev"
    return "uvx"


if __name__ == "__main__":
    raise SystemExit(main())
