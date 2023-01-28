"""Print job matrix for a GitHub Actions workflow that runs `pytest`."""

from __future__ import annotations

import json
from argparse import ArgumentParser
from configparser import ConfigParser
from typing import Optional, Sequence


def main(argv: Sequence[str] | None = None) -> int:
    parser = ArgumentParser(__doc__)
    parser.add_argument("coverage-python-version")
    parser.add_argument("coverage-target")
    parser.add_argument("macos-python-version")
    parser.add_argument("skipped-python-versions")
    args = parser.parse_args(argv)
    matrix = create_job_matrix(
        args.__dict__["coverage-python-version"],
        args.__dict__["coverage-target"],
        args.__dict__["macos-python-version"],
        _format_skipped_version(args.__dict__["skipped-python-versions"]),
    )
    print(json.dumps(matrix, indent=2))
    return 0


def _format_skipped_version(skipped_python_versions: str) -> set[str] | None:
    if skipped_python_versions == "all":
        return None
    if skipped_python_versions == "":
        return set()
    return set(skipped_python_versions.split(" "))


def create_job_matrix(
    coverage_python_version: str,
    coverage_target: str,
    macos_python_version: str,
    skipped_python_versions: set[str] | None,
) -> dict:
    supported_python_versions = get_supported_python_versions()
    if skipped_python_versions is None:
        python_versions = []
    else:
        python_versions = sorted(
            set(supported_python_versions) - skipped_python_versions
        )
    if coverage_target:
        if coverage_python_version not in supported_python_versions:
            raise ValueError(
                f"Selected Python {coverage_python_version} for the coverage job, but"
                " the package only supports Python"
                f" {', '.join(supported_python_versions)}"
            )
        if coverage_python_version in python_versions:
            python_versions.remove(coverage_python_version)
    includes = []
    if "3.6" in python_versions:
        python_versions.remove("3.6")
        includes.append(
            {
                "python-version": "3.6",
                "runs-on": "ubuntu-20.04",
            }
        )
    if coverage_target:
        includes.append(
            {
                "coverage-target": coverage_target,
                "python-version": coverage_python_version,
                "runs-on": "ubuntu-22.04",
            }
        )
    if macos_python_version:
        includes.append(
            {
                "python-version": macos_python_version,
                "runs-on": "macos-12",
            }
        )
    matrix = {}
    if python_versions:
        matrix = {
            "python-version": python_versions,
            "runs-on": ["ubuntu-22.04"],
        }
    if includes:
        matrix["include"] = includes
    return matrix


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
