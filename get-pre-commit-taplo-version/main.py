"""Print job matrix for a GitHub Actions workflow that runs `pytest`."""

from __future__ import annotations

import os

import yaml


def main() -> int:
    version = get_taplo_version()
    if version is None:
        return 1
    print(version)
    return 0


def get_taplo_version() -> str | None:
    config_path = ".pre-commit-config.yaml"
    if not os.path.exists(config_path):
        raise FileExistsError(f"This repository does not have a {config_path}")
    with open(config_path) as f:
        config = yaml.safe_load(f)
    repos: list[dict] = config["repos"]
    for repo in repos:
        if repo["repo"] == "https://github.com/ComPWA/mirrors-taplo":
            if _has_taplo_hook(repo):
                return repo["rev"]
    return None


def _has_taplo_hook(repo_def: dict) -> bool:
    for hook in repo_def["hooks"]:
        if hook["id"] == "taplo":
            return True
    return False


if __name__ == "__main__":
    raise SystemExit(main())
