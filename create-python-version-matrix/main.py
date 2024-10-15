"""Print job matrix for a GitHub Actions workflow that runs `pytest`."""
# /// script
# dependencies = [
#   "packaging",
# ]
# requires-python = ">=3.12"
# ///

import json
import os
import tomllib
from dataclasses import dataclass

from packaging.specifiers import SpecifierSet
from packaging.version import Version


def main() -> int:
    matrix = create_job_matrix()
    print(json.dumps(matrix, indent=2))
    return 0


def create_job_matrix() -> dict:
    return {
        "python-version": get_supported_python_versions(),
    }


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
    allowed_versions = [f"3.{v}" for v in range(6, 13)]
    versions_to_check = [Version(v) for v in sorted(allowed_versions)]
    return [str(v) for v in versions_to_check if v in specifier]


if __name__ == "__main__":
    raise SystemExit(main())
