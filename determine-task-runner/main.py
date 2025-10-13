"""Determine which task runner a repository uses."""
# /// script
# dependencies = [
#   "rtoml",
# ]
# requires-python = ">=3.13"
# ///

import os

import rtoml


def main() -> int:
    if os.path.exists("pyproject.toml"):
        with open("pyproject.toml") as f:
            pyproject = rtoml.load(f)
        if pyproject.get("tool", {}).get("poe", {}).get("tasks"):
            print("poe")
            return 0
        if pyproject.get("tool", {}).get("pixi", {}).get("tasks"):
            print("pixi")
            return 0
    if os.path.exists("pixi.toml"):
        with open("pixi.toml") as f:
            pixi = rtoml.load(f)
        if pixi.get("tasks"):
            print("pixi")
            return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
