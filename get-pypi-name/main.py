"""Print the name of the Python package defined in pyproject.toml."""
# /// script
# requires-python = ">=3.11"
# ///

import os
import tomllib


def main() -> int:
    package_name = _get_package_name_pyproject_toml()
    if package_name is None:
        return 1
    print(package_name)
    return 0


def _get_package_name_pyproject_toml() -> str | None:
    if not os.path.exists("pyproject.toml"):
        return None
    with open("pyproject.toml", "rb") as f:
        pyproject = tomllib.load(f)
    return pyproject.get("project", {}).get("name")


if __name__ == "__main__":
    raise SystemExit(main())
