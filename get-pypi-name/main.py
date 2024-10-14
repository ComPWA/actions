"""Print job matrix for a GitHub Actions workflow that runs `pytest`."""

import os
from configparser import ConfigParser

import tomlkit


def main() -> int:
    for getter in (
        _get_package_name_setup_cfg,
        _get_package_name_pyproject_toml,
    ):
        package_name = getter()
        if package_name is not None:
            print(package_name)
            return 0
    return 1


def _get_package_name_setup_cfg() -> str | None:
    if not os.path.exists("setup.cfg"):
        return None
    cfg = ConfigParser()
    cfg.read("setup.cfg")
    return cfg.get("metadata", "name", fallback=None)


def _get_package_name_pyproject_toml() -> str | None:
    if not os.path.exists("pyproject.toml"):
        return None
    with open("pyproject.toml") as f:
        pyproject = tomlkit.load(f)
    return pyproject.get("project", {}).get("name")


if __name__ == "__main__":
    raise SystemExit(main())
