"""Print job matrix for a GitHub Actions workflow that runs `pytest`."""

from __future__ import annotations

import json
from configparser import ConfigParser


def main() -> int:
    matrix = create_job_matrix()
    print(json.dumps(matrix, indent=2))
    return 0


def create_job_matrix() -> dict:
    return {
        "python-version": get_supported_python_versions(),
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
