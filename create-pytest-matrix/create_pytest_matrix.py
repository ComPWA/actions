"""Print job matrix for a GitHub Actions workflow that runs `pytest`."""

from __future__ import annotations

import json
from argparse import ArgumentParser
from configparser import ConfigParser
from typing import Optional, Sequence


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = ArgumentParser(__doc__)
    parser.add_argument("coverage-python-version")
    parser.add_argument("coverage-target")
    parser.add_argument("macos-python-version")
    args = parser.parse_args(argv)
    matrix = create_job_matrix(
        args.__dict__["coverage-python-version"],
        args.__dict__["coverage-target"],
        args.__dict__["macos-python-version"],
    )
    print(json.dumps(matrix, indent=2))
    return 0


def create_job_matrix(
    coverage_python_version: str,
    coverage_target: str,
    macos_python_version: str,
) -> dict:
    python_versions = get_supported_python_versions()
    if coverage_target:
        try:
            python_versions.remove(coverage_python_version)
        except ValueError as e:
            raise ValueError(
                f"Selected Python {coverage_python_version} for the coverage job, "
                f"but the package only supports Python {', '.join(python_versions)}"
            ) from e
    includes = []
    if coverage_target:
        includes.append(
            {
                "coverage-target": coverage_target,
                "python-version": coverage_python_version,
            }
        )
    if macos_python_version:
        includes.append(
            {
                "python-version": macos_python_version,
                "runs-on": "macos-12",
            }
        )
    matrix = {
        "python-version": python_versions,
        "runs-on": ["ubuntu-22.04"],
    }
    if includes:
        matrix["include"] = includes
    return {
        "fail-fast": False,
        "matrix": matrix,
    }


def get_supported_python_versions() -> list[str]:
    cfg = ConfigParser()
    cfg.read("setup.cfg")
    if not cfg.has_option("metadata", "classifiers"):
        raise ValueError(
            "This package does not have Python version classifiers."
            " See https://pypi.org/classifiers."
        )
    raw = cfg.get("metadata", "classifiers")
    lines = [s.strip() for s in raw.split("\n")]
    identifier = "Programming Language :: Python :: 3."
    classifiers = list(filter(lambda s: s.startswith(identifier), lines))
    if not classifiers:
        raise ValueError(
            f'setup.cfg does not have any classifiers of the form "{identifier}*"'
        )
    prefix = identifier[:-2]
    return [s.replace(prefix, "") for s in classifiers]


if __name__ == "__main__":
    raise SystemExit(main())
