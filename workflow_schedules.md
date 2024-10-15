| Workflow | Schedule | Cron |
| :------- | :------- | :--- |
| [Build Package Docs](.github/workflows/build-package-docs.yaml) | Daily at 05: 17 | `17 5 * * *` |
| [CI](.github/workflows/ci.yaml) | Daily at 07:23 | `23 7 * * *`|
| [Pip Compile Dev](.github/workflows/pip-compile-dev.yml)| Weekly, Sunday at 00:00 | `0 0 * * 0`|
| [Pip Compile Docs](.github/workflows/pip-compile-docs.yml)| Weekly, Sunday at 00:00 | `0 0 * * 0`|
| [Tag](.github/workflows/tag.yml) | Hourly | `0 * * * *`|
