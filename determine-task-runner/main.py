"""Determine which task runner a repository uses."""
# /// script
# requires-python = ">=3.11"
# ///

import os
import tomllib


def main() -> int:
    if os.path.exists("pyproject.toml"):
        with open("pyproject.toml", "rb") as f:
            pyproject = tomllib.load(f)
        if pyproject.get("tool", {}).get("poe", {}).get("tasks"):
            print("poe")
            return 0
        if pyproject.get("tool", {}).get("pixi", {}).get("tasks"):
            print("pixi")
            return 0
    if os.path.exists("pixi.toml"):
        with open("pixi.toml", "rb") as f:
            pixi = tomllib.load(f)
        if pixi.get("tasks"):
            print("pixi")
            return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
