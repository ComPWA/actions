"""Print job matrix for a GitHub Actions workflow that runs `pytest`."""

from __future__ import annotations

import json
import os
from configparser import ConfigParser

import yaml


def main() -> int:
    skipped_hooks = get_skipped_precommit_hooks()
    print(" ".join(skipped_hooks))
    return 0


def get_skipped_precommit_hooks() -> list[str]:
    config_path = ".pre-commit-config.yaml"
    if not os.path.exists(config_path):
        raise FileExistsError(f"This repository does not have a {config_path}")
    with open(config_path) as f:
        config: dict[str, dict] = yaml.safe_load(f)
    precommit_ci_config = config.get("ci")
    if precommit_ci_config is None:
        return ["ALL"]
    skipped_hooks = precommit_ci_config.get("skip", [])
    return skipped_hooks


if __name__ == "__main__":
    raise SystemExit(main())
