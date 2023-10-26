# ansible-documentation

This repository holds the ReStructuredText (RST) source, and other files, for user documentation related to the Ansible package and Ansible Core.

> Documentation for modules and plugins that are officially supported by the Ansible Core engineering team is available in the [`ansible/ansible`](https://github.com/ansible/ansible) repository.

## Building Ansible community documentation

Follow the documentation to [set up your environment](https://docs.ansible.com/ansible/latest/community/documentation_contributions.html#setting-up-your-environment-to-build-documentation-locally) and then [build Ansible community documentation locally](https://docs.ansible.com/ansible/latest/community/documentation_contributions.html#building-the-documentation-locally)

## Verifying your pull request

We welcome all contributions to Ansible community documentation.
If you plan to submit a pull request with changes, you should [verify your PR](https://docs.ansible.com/ansible/latest/community/documentation_contributions.html#verifying-your-documentation-pr) to ensure it conforms with style guidelines and can build successfully.

### Running automated tests

This project includes a `nox` configuration to automate tests, checks, and other functions.
You can use these automated tests to help you verify changes before you submit a PR.

1. Install `nox` using `python3 -m pip install nox` or your distribution's package manager.
2. Run `nox --list` from the repository root to view available sessions.

Each `nox` session creates a temporary environment that installs all requirements and runs the test or check.
This means you only need to run one command to perform the test accurately and consistently.
The following are some of the `nox` sessions you can run:

* Run all available sessions.

  ```
  nox
  ```

* Clone required parts of the `ansible/ansible` repository.

  ```
  nox -s clone-core
  ```

  See [Periodically cloning Ansible core](https://docs.ansible.com/ansible/latest/community/documentation_contributions.html#periodically-cloning-ansible-core) for more information.

* Ensure there are no syntax errors in the reStructuredText source files.

  ```
  nox -s "checkers(rstcheck)"
  ```

  See [Running the final tests](https://docs.ansible.com/ansible/latest/community/documentation_contributions.html#running-the-final-tests) for more information.

* Verify the docs build.

  ```
  nox -s "checkers(docs-build)"
  ```

  This session cleans the generated docs after it runs.
  If you want to view the generated HTML in your browser, you should build the documentation locally.
  See [Building the documentation locally](https://docs.ansible.com/ansible/latest/community/documentation_contributions.html#building-the-documentation-locally) for more information.

* Lint, type check, and format Python scripts in this repository.

  ```
  nox -s lint
  ```

## Checking spelling

Use [`codespell`](https://github.com/codespell-project/codespell) to check for common spelling mistakes in the documentation source.

* Check spelling.

  ```
  nox -s spelling
  ```

* Correct any detected spelling errors.

  ```
  nox -s spelling -- -w
  ```

* Select an option when `codespell` suggests more than one word as a correction.

  ```
  nox -s spelling -- -w -i 3
  ```

## Dependency files

`nox` sessions use dependencies from requirements files in the `tests/` directory.
Each session has a `tests/{name}.in` file with direct dependencies and a lock file in `tests/{name}.txt` that pins *exact versions* for both direct and transitive dependencies.
The lock files contain tested dependencies that are automatically updated on a weekly basis.

If you'd like to use untested dependencies, set `PINNED=false` as in the following example:

```
PINNED=false nox -s "checkers(docs-build)"
```

For more details about using unpinned and tested dependencies for doc builds, see [Setting up your environment to build documentation locally](https://docs.ansible.com/ansible/latest/community/documentation_contributions.html#setting-up-your-environment-to-build-documentation-locally).

## Updating dependencies

Use the following `nox` session to update the dependency lock files in `tests/`.

  ```
  nox -e pip-compile
  ```

> This session requires Python 3.10.

If you do not have Python 3.10 installed, you can use root-less podman with a Python 3.10 image as follows:

```bash
podman run --rm --tty --volume "$(pwd):/mnt:z" --workdir /mnt docker.io/library/python:3.10 bash -c 'pip install nox ; nox -e pip-compile'
```
