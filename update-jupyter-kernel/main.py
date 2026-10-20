"""Update Python version in Jupyter kernel."""
# /// script
# dependencies = [
#   "nbformat",
# ]
# requires-python = ">=3.9"
# ///

from __future__ import annotations

import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import TYPE_CHECKING

import nbformat

if TYPE_CHECKING:
    from collections.abc import Sequence


def main(argv: Sequence[str] | None = None) -> None:
    parser = ArgumentParser(__doc__)
    parser.add_argument("notebook_path", type=Path)
    args = parser.parse_args(argv)
    notebook = nbformat.read(args.notebook_path, as_version=nbformat.NO_CONVERT)
    metadata = notebook.get("metadata")
    if not metadata:
        return
    kernelspec = metadata.get("kernelspec")
    if not kernelspec:
        return
    if kernelspec.get("language") != "python":
        return
    language_info = metadata.get("language_info")
    if not language_info:
        return
    version = language_info.get("version")
    if not version:
        return
    v = sys.version_info
    expected_version = f"{v.major}.{v.minor}.{v.micro}"
    if version != expected_version:
        language_info["version"] = expected_version
        nbformat.write(notebook, args.notebook_path)


if __name__ == "__main__":
    raise SystemExit(main())
