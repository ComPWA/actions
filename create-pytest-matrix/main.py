"""Print job matrix for a GitHub Actions workflow that runs `pytest`."""

from __future__ import annotations

import json
import os
from argparse import ArgumentParser
from configparser import ConfigParser
from typing import Sequence

import toml


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
    if not skipped_python_versions:
        return set()
    return set(skipped_python_versions.split(" "))


def create_job_matrix(  # noqa: C901
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
            msg = (
                f"Selected Python {coverage_python_version} for the coverage job, but"
                " the package only supports Python"
                f" {', '.join(supported_python_versions)}"
            )
            raise ValueError(msg)
        if coverage_python_version in python_versions:
            python_versions.remove(coverage_python_version)
    includes = []
    if "3.6" in python_versions:
        python_versions.remove("3.6")
        includes.append({
            "python-version": "3.6",
            "runs-on": "ubuntu-20.04",
        })
    if "3.7" in python_versions:
        python_versions.remove("3.7")
        includes.append({
            "python-version": "3.7",
            "runs-on": "ubuntu-22.04",
        })
    if coverage_target:
        includes.append({
            "coverage-target": coverage_target,
            "python-version": coverage_python_version,
            "runs-on": "ubuntu-24.04",
        })
    if macos_python_version:
        includes.append({
            "python-version": macos_python_version,
            "runs-on": "macos-14",
        })
    matrix = {}
    if python_versions:
        matrix = {
            "python-version": python_versions,
            "runs-on": ["ubuntu-24.04"],
        }
    if includes:
        matrix["include"] = includes
    return matrix


PYPROJECT_TOML = "pyproject.toml"
SETUP_CFG = "setup.cfg"
CLASSIFIERS_ERROR_MSG = (
    "This package does not have Python version classifiers, so cannot determine"
    " intended Python versions. See https://pypi.org/classifiers."
)
VERSION_IDENTIFIER = "Programming Language :: Python :: 3."


def get_supported_python_versions() -> list[str]:
    classifiers = _get_classifiers()
    return _determine_python_versions(classifiers)


def _get_classifiers() -> list[str]:
    if os.path.exists(SETUP_CFG):
        return __get_classifiers_from_cfg(SETUP_CFG)
    if os.path.exists(PYPROJECT_TOML):
        return __get_classifiers_from_toml(PYPROJECT_TOML)
    msg = f"This project does not contain a {SETUP_CFG} or {PYPROJECT_TOML}"
    raise FileNotFoundError(msg)


def __get_classifiers_from_cfg(path: str) -> list[str]:
    cfg = ConfigParser()
    cfg.read(path)
    if not cfg.has_option("metadata", "classifiers"):
        raise ValueError(CLASSIFIERS_ERROR_MSG)
    raw = cfg.get("metadata", "classifiers")
    return [s.strip() for s in raw.split("\n") if s.strip()]


def __get_classifiers_from_toml(path: str) -> list[str]:
    with open(path) as f:
        cfg = toml.load(f)
    classifiers = cfg.get("project", {}).get("classifiers")
    if classifiers is None:
        raise ValueError(CLASSIFIERS_ERROR_MSG)
    return classifiers


def _determine_python_versions(classifiers: list[str]) -> list[str]:
    versions = [s for s in classifiers if s.startswith(VERSION_IDENTIFIER)]
    if not versions:
        msg = (
            f"{SETUP_CFG} does not have any classifiers of the form"
            f' "{VERSION_IDENTIFIER}*"'
        )
        raise ValueError(msg)
    prefix = VERSION_IDENTIFIER[:-2]
    return [s.replace(prefix, "") for s in versions]


if __name__ == "__main__":
    raise SystemExit(main())
