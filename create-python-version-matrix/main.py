"""Print job matrix for a GitHub Actions workflow that runs `pytest`."""

from __future__ import annotations

import json
import os
from configparser import ConfigParser

import toml

PYPROJECT_TOML = "pyproject.toml"
SETUP_CFG = "setup.cfg"

CLASSIFIERS_ERROR_MSG = (
    "This package does not have Python version classifiers, so cannot determine"
    " intended Python versions. See https://pypi.org/classifiers."
)
VERSION_IDENTIFIER = "Programming Language :: Python :: 3."


def main() -> int:
    matrix = create_job_matrix()
    print(json.dumps(matrix, indent=2))
    return 0


def create_job_matrix() -> dict:
    return {
        "python-version": get_supported_python_versions(),
    }


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
