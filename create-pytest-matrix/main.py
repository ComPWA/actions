"""Print job matrix for a GitHub Actions workflow that runs `pytest`."""
# /// script
# dependencies = [
#   "packaging",
# ]
# requires-python = ">=3.12"
# ///

from __future__ import annotations

import json
import os
import tomllib
from argparse import ArgumentParser
from dataclasses import dataclass
from typing import TYPE_CHECKING

from packaging.specifiers import SpecifierSet
from packaging.version import Version

if TYPE_CHECKING:
    from collections.abc import Sequence


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
        _is_version_allowed(coverage_python_version, supported_python_versions)
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
        _is_version_allowed(macos_python_version, supported_python_versions)
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


def _is_version_allowed(version: str, supported_versions: list[str]) -> None:
    if version not in supported_versions:
        supported_versions_str = ", ".join(supported_versions)
        msg = f"Selected Python {version}, but the package only supports Python {supported_versions_str}"
        raise ValueError(msg)


PYPROJECT_TOML = "pyproject.toml"
VERSION_IDENTIFIER = "Programming Language :: Python :: 3."


def get_supported_python_versions() -> list[str]:
    version_info = _get_version_info()
    return _determine_python_versions(version_info)


@dataclass
class VersionInfo:
    classifiers: list[str] | None
    requires_python: str | None


def _get_version_info() -> VersionInfo:
    pyproject_toml_path = "pyproject.toml"
    if not os.path.exists(pyproject_toml_path):
        msg = f"This project does not contain a {pyproject_toml_path}"
        raise FileNotFoundError(msg)
    with open(pyproject_toml_path, "rb") as f:
        cfg = tomllib.load(f)
    project_table: dict = cfg.get("project", {})
    return VersionInfo(
        classifiers=project_table.get("classifiers"),
        requires_python=project_table.get("requires-python"),
    )


def _determine_python_versions(version_info: VersionInfo) -> list[str]:
    supported_versions = _determine_python_versions_from_classifiers(version_info)
    if supported_versions is not None:
        return supported_versions
    if version_info.requires_python is not None:
        return __get_allowed_versions(version_info.requires_python)
    msg = "No PyPI classifiers or minimal Python version defined"
    raise ValueError(msg)


def _determine_python_versions_from_classifiers(
    version_info: VersionInfo,
) -> list[str] | None:
    if version_info.classifiers is None:
        return None
    version_identifier = "Programming Language :: Python :: 3."
    versions = [s for s in version_info.classifiers if s.startswith(version_identifier)]
    if not versions:
        return None
    prefix = version_identifier[:-2]
    return [s.replace(prefix, "") for s in versions]


def __get_allowed_versions(version_range: str) -> list[str]:
    """Get a list of allowed versions from a version range specifier.

    >>> __get_allowed_versions(">=3.9,<3.13")
    ['3.9', '3.10', '3.11', '3.12']
    """
    specifier = SpecifierSet(version_range)
    allowed_versions = [f"3.{v}" for v in range(6, 15)]
    versions_to_check = [Version(v) for v in sorted(allowed_versions)]
    return [str(v) for v in versions_to_check if v in specifier]


if __name__ == "__main__":
    raise SystemExit(main())
