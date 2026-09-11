"""Inspect style tasks without executing caller configuration."""
# cspell:ignore shlex
# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///

import os
import shlex
import tomllib
from pathlib import Path
from typing import Any


def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("rb") as stream:
        return tomllib.load(stream)


def supports_multiple_hooks(task: Any) -> bool:
    """Recognize direct commands with options that leave trailing IDs as selectors.

    Unknown options, shell syntax, and argument templates retain the single-hook
    fallback rather than guessing how the task forwards its arguments.
    """
    if isinstance(task, dict):
        if "args" in task or "depends-on" in task:
            return False
        task = task.get("cmd")
    if not isinstance(task, str):
        return False
    try:
        command = shlex.split(task)
    except ValueError:
        return False
    return command[:2] == ["prek", "run"] and all(
        option in {"--all-files", "-a", "--show-diff-on-failure", "--verbose", "-v"}
        for option in command[2:]
    )


def has_style_override(config: dict[str, Any]) -> bool:
    return "style" in config.get("tasks", {}) or any(
        has_style_override(value)
        for value in config.values()
        if isinstance(value, dict)
    )


def determine_command(directory: Path) -> tuple[str, bool]:
    pyproject = load_config(directory / "pyproject.toml")
    poe = pyproject.get("tool", {}).get("poe", {})
    if "style" in poe.get("tasks", {}):
        task = poe["tasks"]["style"]
        batch = supports_multiple_hooks(task)
        if isinstance(task, str) and poe.get("default_task_type", "cmd") != "cmd":
            batch = False
        return "poe style", batch

    if (directory / "pixi.toml").exists():
        pixi = load_config(directory / "pixi.toml")
    else:
        pixi = pyproject.get("tool", {}).get("pixi", {})
    if "style" in pixi.get("tasks", {}):
        batch = supports_multiple_hooks(pixi["tasks"]["style"])
        if any(has_style_override(pixi.get(key, {})) for key in ("feature", "target")):
            batch = False
        return "pixi run style", batch
    return "prek run --all-files", True


def main() -> None:
    command, batch = determine_command(Path.cwd())
    output = f"cmd={command}\nbatch-hooks={str(batch).lower()}\n"
    print(output, end="")
    with open(os.environ["GITHUB_OUTPUT"], "a") as stream:
        stream.write(output)


if __name__ == "__main__":
    main()
