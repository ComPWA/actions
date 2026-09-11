# ComPWA actions and shared workflows

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)
[![Spelling checked](https://img.shields.io/badge/cspell-checked-brightgreen.svg)](https://github.com/streetsidesoftware/cspell/tree/main/packages/cspell)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![ty](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)

This repository hosts [shared workflows for GitHub Actions](https://docs.github.com/en/actions/using-workflows/reusing-workflows) and [shared actions](https://docs.github.com/en/actions/creating-actions) that are used by [repositories of the ComPWA Project](https://github.com/orgs/ComPWA/repositories). See also [ComPWA/repo-maintenance](https://github.com/ComPWA/repo-maintenance), which enforces policies on those repositories.

Actions and shared workflows provided by this repository presume that the repository to which they are applied follow the same set-up as described on [compwa.github.io/develop](https://compwa.github.io/develop). For example, it assumes source code is located under the `src/` directory and documentation is located under `docs/`.

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for how to develop this repository.

The shared style workflow uses a configured `poe style` or `pixi run style` task, and otherwise runs `prek run --all-files`. Both `prek` and `pre-commit` are available to custom style tasks. The `run-style` action inspects Poe tasks in `pyproject.toml` and Pixi tasks in `pixi.toml` or `pyproject.toml`. Direct `prek run` command tasks without argument templates receive selected hook IDs together. Recognized options are `--all-files` (`-a`), `--show-diff-on-failure`, and `--verbose` (`-v`). Tasks using `pre-commit`, wrappers, other options, or Pixi task overrides retain one invocation per hook. The configured task runner still executes the task with its own environment.

The `run-style` action requires checkout, `uv`, and `prek` to be set up first. Its optional `hooks` input accepts space-separated hook IDs and defaults to `ALL`, which runs the complete style task. Its optional `python-version` input defaults to `3.13` and selects the Python version used to install task runners.
