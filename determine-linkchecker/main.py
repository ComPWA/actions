"""Select lychee for recognized linkcheck tasks, otherwise keep task execution."""
# /// script
# requires-python = ">=3.11"
# ///

import os
import tomllib
from pathlib import Path
from typing import Any


def main() -> int:
    value = determine_linkchecker()
    output = os.environ.get("GITHUB_OUTPUT")
    if output is not None:
        with open(output, "a") as stream:
            print(f"value={value}", file=stream)
    print(f"Link checker: {value}")
    return 0


def determine_linkchecker() -> str:
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
    commands = [
        task.get("cmd", task.get("shell", "")) if isinstance(task, dict) else task
        for task in tasks
    ]
    if commands and all(
        isinstance(cmd, str) and "lychee" in cmd and "sphinx" not in cmd
        for cmd in commands
    ):
        return "lychee"
    return "task"


def _load(path: str) -> dict[str, Any]:
    file = Path(path)
    if not file.exists():
        return {}
    return tomllib.loads(file.read_text())


if __name__ == "__main__":
    raise SystemExit(main())
