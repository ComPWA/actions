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

The shared style workflow uses a configured `poe style` or `pixi run style` task, and otherwise runs `prek run --all-files`. The `run-style` action inspects Poe tasks in `pyproject.toml` and Pixi tasks in `pixi.toml` or `pyproject.toml`. Direct `prek run` command tasks without argument templates receive selected hook IDs together and skip installation of `pre-commit` and `pre-commit-uv`. Recognized options are `--all-files` (`-a`), `--show-diff-on-failure`, and `--verbose` (`-v`). Tasks using `pre-commit`, wrappers, other options, or Pixi task overrides retain one invocation per hook and install both compatibility packages. The configured task runner still executes the task with its own environment.

The `run-style` action requires checkout, `uv`, and `prek` to be set up first. Its optional `hooks` input accepts space-separated hook IDs and defaults to `ALL`, which runs the complete style task. Its optional `python-version` input defaults to `3.14` and selects the Python version used to install task runners. Its optional `verify-fixes` input defaults to `"false"`; autofix sets it to `"true"` so that a failed style task runs again on the fixed tree. A remaining style failure is reported even when fixes are submitted. Without a configured style task or pre-commit configuration, there are no style checks to run.

## Automated fixes without a personal access token

Install the [autofix.ci GitHub App](https://autofix.ci) for the caller repository and add `.github/workflows/autofix.ci.yml` with the following contents. The workflow name must be `autofix.ci`. The example uses `main`; after this feature is released, pin the workflow to that release or its commit SHA.

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
    uses: ComPWA/actions/.github/workflows/autofix.ci.yml@main
```

The shared workflow upgrades lock files on same-repository PRs with the `⬆️ Lock` label, collects the resulting artifacts, runs the repository's style task, and updates Jupyter kernels in modified notebooks. It submits the combined changes to autofix.ci once, using the app's credentials. Ordinary PRs, including forks, receive style and notebook fixes without dependency upgrades. Failed lock-update jobs prevent submission of a partial upgrade. Push and manual runs apply style fixes without upgrading dependencies or creating PRs.

The optional `python-version` input defaults to `"3.14"`. Set `upgrade-lock-files: false` to disable dependency upgrades. Callers do not pass secrets to this workflow. Keep its concurrency group distinct from any caller-level group to avoid cancellation of the caller run.

When migrating, remove the separate PR-triggered call to `ComPWA/actions/.github/workflows/lock.yml` and remove the style workflow's `token` secret. Keep the shared style workflow for validation; it already leaves commits to autofix.ci when the caller has `.github/workflows/autofix.ci.yml`. Scheduled or manual creation of upgrade PRs remains a separate call to the lock workflow with its `token` secret. Codecov authentication, publishing to another repository, and release branch updates are separate from autofix.

The policy templates also need to preserve this caller configuration. This repository uses `tool.compwa.policy.github.no-github-actions = true` to maintain its workflows manually while the templates still insert a style PAT; its other policy checks remain enabled.

The lock workflow's optional `generate-only` input defaults to `false`, preserving publishing for existing reusable-workflow callers. Setting it to `true` generates artifacts without pushing or creating PRs and requires no token. Its `lock-files` output lists the selected paths, separated by spaces, and is empty when no upgrade is requested. This repository routes its own PR upgrades through autofix; the lock workflow's direct trigger only supports manual PR creation.

Autofix.ci rejects changes under `.github/`, so workflow-file fixes still need to be applied manually. Installing the app is required; removing PAT secrets alone does not enable automated commits.
