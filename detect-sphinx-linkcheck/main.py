"""Check whether a Poe or Pixi linkcheck task of the repository runs Sphinx."""
# /// script
# requires-python = ">=3.11"
# ///

import os
import tomllib
from pathlib import Path
from typing import Any


def main() -> int:
    value = runs_sphinx_linkcheck()
    output = os.environ.get("GITHUB_OUTPUT")
    if output is not None:
        with open(output, "a") as stream:
            print(f"value={str(value).lower()}", file=stream)
    print(f"Sphinx linkcheck task: {value}")
    return 0


def runs_sphinx_linkcheck() -> bool:
    pyproject = _load("pyproject.toml")
    tool = pyproject.get("tool", {})
    pixi = tool.get("pixi", {}) or _load("pixi.toml")
    poe = tool.get("poe", {})
    task_tables = [
        poe.get("tasks", {}),
        *(group.get("tasks", {}) for group in poe.get("groups", {}).values()),
        pixi.get("tasks", {}),
        *(feature.get("tasks", {}) for feature in pixi.get("feature", {}).values()),
    ]
    tasks = [table["linkcheck"] for table in task_tables if "linkcheck" in table]
    return any("sphinx" in str(task) for task in tasks)


def _load(path: str) -> dict[str, Any]:
    file = Path(path)
    if not file.exists():
        return {}
    return tomllib.loads(file.read_text())


if __name__ == "__main__":
    raise SystemExit(main())
