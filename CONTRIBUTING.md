# Help developing

## Local set-up

Please install `pre-commit`, for example [through Conda](https://anaconda.org/conda-forge/pre_commit). For more information, see [Help developing](https://compwa-org.rtfd.io/develop.html) on [compwa-org.rtfd.io](https://compwa-org.readthedocs.io).

## Conventions

- It is assumed that repositories that use shared workflows from this repository can run their CI jobs locally with [`tox`](https://tox.wiki). Names of the workflow files should therefore be the same as the name of the corresponding `tox` job. For example, a common job is `docnb`, which builds HTML pages with [Sphinx](https://www.sphinx-doc.org) using the [`myst-nb`](https://myst-nb.rtfd.io) extension. The corresponding job file for this job is [`docnb.yml`](./.github/workflows/docnb.yml).
- Workflow definitions are located under [`.github/workflows`](./.github/workflows/): GitHub Actions [does not yet support sharing workflows in subdirectories](https://docs.github.com/en/actions/using-workflows/reusing-workflows#creating-a-reusable-workflow).
- Actions are located under directories in the root folder, for example [`pip-install/action.yml`](./pip-install/action.yml).
