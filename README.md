# ComPWA actions and shared workflows

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)
[![Spelling checked](https://img.shields.io/badge/cspell-checked-brightgreen.svg)](https://github.com/streetsidesoftware/cspell/tree/master/packages/cspell)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

This repository hosts [shared workflows for GitHub Actions](https://docs.github.com/en/actions/using-workflows/reusing-workflows) and [shared actions](https://docs.github.com/en/actions/creating-actions) that are used by [repositories of the ComPWA Project](https://github.com/orgs/ComPWA/repositories). See also [ComPWA/repo-maintenance](https://github.com/ComPWA/repo-maintenance), which enforces policies on those repositories.

Actions and shared workflows provided by this repository presume that the repository to which they are applied follow the same set-up as described on [compwa.github.io/develop](https://compwa.github.io/develop). For example, it assumes source code is located under the `src/` directory and documentation is located under `docs/`.

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for how to develop this repository.
