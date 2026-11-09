# ComPWA actions and shared workflows

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/license/MIT)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)
[![Spelling checked](https://img.shields.io/badge/cspell-checked-brightgreen.svg)](https://github.com/streetsidesoftware/cspell/tree/main/packages/cspell)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![ty](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)

This repository hosts [shared workflows for GitHub Actions](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows) and [shared actions](https://docs.github.com/en/actions/concepts/workflows-and-actions/custom-actions) that are used by [repositories of the ComPWA Project](https://github.com/orgs/ComPWA/repositories). See also [ComPWA/policy](https://github.com/ComPWA/policy), which enforces policies on those repositories.

Actions and shared workflows provided by this repository presume that the repository to which they are applied follow the same set-up as described on [compwa.github.io/develop](https://compwa.github.io/develop). For example, it assumes source code is located under the `src/` directory and documentation is located under `docs/`.

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for how to develop this repository.

The shared style workflow uses a configured `poe style` or `pixi run style` task, and otherwise runs `prek run --all-files`. The `run-style` action inspects Poe tasks in `pyproject.toml` and Pixi tasks in `pixi.toml` or `pyproject.toml`. Direct `prek run` command tasks without argument templates receive selected hook IDs together and skip installation of `pre-commit` and `pre-commit-uv`. Recognized options are `--all-files` (`-a`), `--show-diff-on-failure`, and `--verbose` (`-v`). Tasks using `pre-commit`, wrappers, other options, or Pixi task overrides retain one invocation per hook and install both compatibility packages. The configured task runner still executes the task with its own environment.

The [`run-style`](./run-style/action.yml) action requires checkout, `uv`, and `prek` to be set up first. With `verify-fixes`, a failing style task runs a second time, so the step only fails if a hook still fails after its fixes are applied.

## Automated fixes without a personal access token

Commits pushed with the default `GITHUB_TOKEN` [do not trigger new workflow runs](https://docs.github.com/en/actions/concepts/security/github_token), which is why the [style](./.github/workflows/style.yml) and [lock](./.github/workflows/lock.yml) workflows push with a personal access token. The [`autofix.ci`](./.github/workflows/autofix.ci.yml) workflow avoids that token: it lets the [autofix.ci GitHub App](https://autofix.ci) commit the fixes. To use it, install the app for the repository and add this caller, which must be [named `autofix.ci`](https://autofix.ci/security).

```yaml
name: autofix.ci

on:
  pull_request:
    types: [opened, reopened, synchronize, labeled]
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pull-requests: read

jobs:
  autofix:
    uses: ComPWA/actions/.github/workflows/autofix.ci.yml@v4.2.0
```

On same-repository PRs labeled `⬆️ Lock`, the workflow upgrades the lock files. It then runs the repository's style task against them, updates the Jupyter kernels of modified notebooks, and submits everything as a single commit. Other PRs, including those from forks, and push or manual runs get only style and notebook fixes. If any lock job fails, nothing is submitted. Set `upgrade-lock-files: false` to skip the upgrades.

Repositories managed by [ComPWA/policy](https://github.com/ComPWA/policy) 0.10.4 or later migrate by setting `autofix-ci = true` under `[tool.compwa.policy.github]`. Policy then writes this caller, removes the `token` secret from the `style.yml` call, removes the PR trigger from `lock.yml`, and sets pre-commit.ci's [`autofix_prs`](https://pre-commit.ci/#configuration-autofix_prs) to `false`. Scheduled and manual upgrade PRs still call `lock.yml` with the `token` secret, and the style workflow still runs its checks but leaves commits to the app. The app cannot commit changes under `.github/`, so fix workflow files by hand.
