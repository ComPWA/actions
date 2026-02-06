"""Print job matrix for a GitHub Actions workflow that runs `pytest`."""
# /// script
# dependencies = [
#   "packaging",
# ]
# requires-python = ">=3.13"
# ///

from __future__ import annotations

import json
import os
import tomllib
from argparse import ArgumentParser
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from packaging.specifiers import SpecifierSet
from packaging.version import Version

if TYPE_CHECKING:
    from collections.abc import Sequence

PYTHON_VERSION = Literal[
    "3.6", "3.7", "3.8", "3.9", "3.10", "3.11", "3.12", "3.13", "3.14"
]


def main(argv: Sequence[str] | None = None) -> int:
    parser = ArgumentParser(__doc__)
    parser.add_argument(
        "--coverage-python-version", choices=[*PYTHON_VERSION.__args__, ""]
    )
    parser.add_argument(
        "--macos-python-version", choices=[*PYTHON_VERSION.__args__, ""]
    )
    parser.add_argument("--skipped-python-versions", type=str)
    args = parser.parse_args(argv)
    matrix = create_job_matrix(
        args.coverage_python_version,
        args.macos_python_version,
        _format_skipped_version(args.skipped_python_versions),
    )
    print(json.dumps(matrix, indent=2))
    return 0


def _format_skipped_version(skipped_python_versions: str) -> set[PYTHON_VERSION] | None:
    if skipped_python_versions == "all":
        return None
    if not skipped_python_versions:
        return set()
    return set(skipped_python_versions.split(" "))  # ty:ignore[invalid-return-type]


def create_job_matrix(
    coverage_python_version: PYTHON_VERSION | Literal[""],
    macos_python_version: PYTHON_VERSION | Literal[""],
    skipped_python_versions: set[PYTHON_VERSION] | None,
) -> dict:
    supported_python_versions = get_supported_python_versions()
    if skipped_python_versions is None:
        python_versions = []
    else:
        python_versions = sorted(
            set(supported_python_versions) - skipped_python_versions
        )
    if coverage_python_version:
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
    if coverage_python_version:
        includes.append({
            "codecov": "codecov",
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


def _is_version_allowed(
    version: PYTHON_VERSION, supported_versions: list[PYTHON_VERSION]
) -> None:
    if version not in supported_versions:
        supported_versions_str = ", ".join(supported_versions)
        msg = f"Selected Python {version}, but the package only supports Python {supported_versions_str}"
        raise ValueError(msg)


PYPROJECT_TOML = "pyproject.toml"
VERSION_IDENTIFIER = "Programming Language :: Python :: 3."


def get_supported_python_versions() -> list[PYTHON_VERSION]:
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


def _determine_python_versions(version_info: VersionInfo) -> list[PYTHON_VERSION]:
    supported_versions = _determine_python_versions_from_classifiers(version_info)
    if supported_versions is not None:
        return supported_versions
    if version_info.requires_python is not None:
        return __get_allowed_versions(version_info.requires_python)
    msg = "No PyPI classifiers or minimal Python version defined"
    raise ValueError(msg)


def _determine_python_versions_from_classifiers(
    version_info: VersionInfo,
) -> list[PYTHON_VERSION] | None:
    if version_info.classifiers is None:
        return None
    version_identifier = "Programming Language :: Python :: 3."
    versions = [s for s in version_info.classifiers if s.startswith(version_identifier)]
    if not versions:
        return None
    prefix = version_identifier[:-2]
    return [s.replace(prefix, "") for s in versions]  # ty:ignore[invalid-return-type]


def __get_allowed_versions(version_range: str) -> list[PYTHON_VERSION]:
    """Get a list of allowed versions from a version range specifier.

    >>> __get_allowed_versions(">=3.9,<3.13")
    ['3.9', '3.10', '3.11', '3.12']
    """
    specifier = SpecifierSet(version_range)
    allowed_versions = [f"3.{v}" for v in range(6, 15)]
    versions_to_check = [Version(v) for v in sorted(allowed_versions)]
    return [str(v) for v in versions_to_check if v in specifier]  # ty:ignore[invalid-return-type]


if __name__ == "__main__":
    raise SystemExit(main())
