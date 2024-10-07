# ansible-documentation

This repository holds the ReStructuredText (RST) source, and other files, for user documentation related to the Ansible package and Ansible Core.

> Documentation for modules and plugins that are officially supported by the Ansible Core engineering team is available in the [`ansible/ansible`](https://github.com/ansible/ansible) repository.

## Verifying your pull request

We welcome all contributions to Ansible community documentation.
If you plan to submit a pull request with changes, you should [verify your PR](https://docs.ansible.com/ansible/latest/community/documentation_contributions.html#verifying-your-documentation-pr) to ensure it conforms with style guidelines and can build successfully.

### Setting up nox

This project includes a `nox` configuration to automate tests, checks, and other functions.
You can use these automated tests to help you verify changes before you submit a PR.
You can manually
[set up your environment](https://docs.ansible.com/ansible/latest/community/documentation_contributions.html#setting-up-your-environment-to-build-documentation-locally)
if you prefer, but `nox` is more straightforward and create an isolated environment for you.

* Install `nox` using `python3 -m pip install nox` or your distribution's package manager.

* Execute `nox` from the repository root with no arguments to run
  all docs checkers, Python code checkers, and a minimal HTML docs build.

* Alternatively, you can run only certain tasks as outlined in the following sections.
  Run `nox --list` to view available sessions.

### Building docs

The different Makefile targets used to build the documentation are outlined in
[Building the documentation locally](https://docs.ansible.com/ansible/latest/community/documentation_contributions.html#building-the-documentation-locally).
The `nox` configuration has a `make` session that creates a build environment and uses the Makefile to generate HTML.

* Clone required parts of the `ansible/ansible` repository.

  ``` bash
  nox -s clone-core
  ```

  See [Periodically cloning Ansible core](https://docs.ansible.com/ansible/latest/community/documentation_contributions.html#periodically-cloning-ansible-core) for more information.

* Build minimal Ansible Core docs.

  ``` bash
  nox -s make
  ```

* Run a specific Makefile target:

  ``` bash
  nox -s make -- clean htmlsingle rst=community/documentation_contributions.rst
  ```

### Running automated tests

The `nox` configuration also contains session to run automated docs checkers.

* Ensure there are no syntax errors in the reStructuredText source files.

  ``` bash
  nox -s "checkers(rstcheck)"
  ```

  See [Running the final tests](https://docs.ansible.com/ansible/latest/community/documentation_contributions.html#running-the-final-tests) for more information.

* Verify the docs build.

  ``` bash
  nox -s "checkers(docs-build)"
  ```

  This session cleans the generated docs after it runs.
  If you want to view the generated HTML in your browser, you should build the documentation locally.
  See [Building the documentation locally](https://docs.ansible.com/ansible/latest/community/documentation_contributions.html#building-the-documentation-locally) for more information.

* Lint, type check, and format Python scripts in this repository.

  ``` bash
  nox -s lint
  ```

  The `actionlint` linter that is run as part of the `lint` session requires
  `podman` or `docker` to be installed.
  If both container engines are installed, `podman` is preferred.
  Set `CONTAINER_ENGINE=docker` to change this behavior.

### Checking spelling

Use [`codespell`](https://github.com/codespell-project/codespell) to check for common spelling mistakes in the documentation source.

* Check spelling.

  ``` bash
  nox -s spelling
  ```

* Correct any detected spelling errors.

  ``` bash
  nox -s spelling -- -w
  ```

* Select an option when `codespell` suggests more than one word as a correction.

  ``` bash
  nox -s spelling -- -w -i 3
  ```

## Dependency files

`nox` sessions use dependencies from requirements files in the `tests/` directory.
Each session has a `tests/{name}.in` file with direct dependencies and a lock file in `tests/{name}.txt` that pins *exact versions* for both direct and transitive dependencies.
The lock files contain tested dependencies that are automatically updated on a weekly basis.

If you'd like to use untested dependencies, set `PINNED=false` as in the following example:

```bash
PINNED=false nox -s "checkers(docs-build)"
```

For more details about using unpinned and tested dependencies for doc builds, see [Setting up your environment to build documentation locally](https://docs.ansible.com/ansible/latest/community/documentation_contributions.html#setting-up-your-environment-to-build-documentation-locally).

## Updating dependencies

Use the following `nox` session to update the dependency lock files in `tests/`.

  ``` bash
  nox -s pip-compile
  ```

To synchronize dependency lock files with base requirements files without changing transitive dependencies, use the `--no-upgrade` flag:

  ``` bash
  nox -s pip-compile -- --no-upgrade
  ```

> This session requires Python 3.10.

If you do not have Python 3.10 installed, you can use root-less podman with a Python 3.10 image as follows:

```bash
podman run --rm --tty --volume "$(pwd):/mnt:z" --workdir /mnt docker.io/library/python:3.10 bash -c 'pip install nox ; nox -s pip-compile'
```

## Creating release tags

When a tag is created in the [`ansible/ansible`](https://github.com/ansible/ansible) repository for a release or release candidate, a corresponding tag should be created in this `ansible-documentation` repository.

First, ensure that you have the [`ansible/ansible`](https://github.com/ansible/ansible) and [`ansible/ansible-documentation`](https://github.com/ansible/ansible-documentation) repositories checked out.
The tool assumes that both checkouts have the same parent directory. You can set different paths to your checkouts with the `--docs` and `--core` options if you have them set up another way.

Next, run the `tag` `nox` session.

This will determine any missing `ansible-core` tags and create them in `ansible-documentation` if needed, exiting normally otherwise:

``` bash
# The tagger scripts assumes "origin" as the upstream remote.
nox -s tag

# If you use a different upstream remote, specify the name.
nox -s tag -- --remote <name> tag

# If your core repo is not in the same filesystem location, specify the path.
nox -s tag -- --core <path> tag
```

See `nox -s tag -- --help` for extended options.

## Branching for new stable versions

The branching strategy for this repository mirrors the [`ansible/ansible`](https://github.com/ansible/ansible) repository.
When a new `stable-*` branch is created in the core repository, a corresponding branch in the `ansible-documentation` repository needs to be created.
There are various other changes that should occur around the same time that the new stable branch is cut.

### Creating stable branches

Someone with maintainer access must create the new branch.

```bash
# Make sure your checkout is up to date.
git fetch upstream

# Create a new stable branch against the devel branch.
git checkout -b stable-2.18 upstream/devel

# Push the new stable branch to the repository.
git push upstream stable-2.18:stable-2.18
```

### Updating the core branch

The script that grafts portions of the core repository uses the `docs/ansible-core-branch.txt` file to specify which branch to clone.
When a new stable branch is created, someone needs to create a pull request to ensure that the file specifies the correct version.

```bash
sed -i 's/devel/stable-2.18/g' docs/ansible-core-branch.txt
```

### Updating the tagger script

On the `devel` branch, update the list of active branches in the `hacking/tagger/tag.py` script by adding the new stable branch and remove the lowest version, for example:

#### Previous active branches list

```python
DEFAULT_ACTIVE_BRANCHES: tuple[str, ...] = (
    "stable-2.14",
    "stable-2.15",
    "stable-2.16",
    "stable-2.17",
)
```

#### Updated active branches list

```python
DEFAULT_ACTIVE_BRANCHES: tuple[str, ...] = (
    "stable-2.15",
    "stable-2.16",
    "stable-2.17",
    "stable-2.18",
)
```

### Remove devel-only tooling

There are some scripts and other tooling artefacts that should be on the `devel` branch only.
After creating a new stable branch, someone should remove the appropriate files and references.

```bash
# Remove the following workflow files, the tagger script, and tagger requirements.
git rm -r .github/workflows/pip-compile-dev.yml .github/workflows/pip-compile-docs.yml .github/workflows/reusable-pip-compile.yml hacking/tagger tests/tag.*
```

Next, remove references to the tagger dependencies as follows:

1. Remove the reference from the typing input file.

   ```bash
   sed -i '/-r tag.in/d' tests/typing.in
   ```

2. Clean up the typing lockfile.

   ```bash
   nox -s pip-compile -- --no-upgrade
   ```

Finally, open `noxfile.py` and remove `"hacking/tagger/tag.py",` from the `LINT_FILES` tuple, for example:

#### Previous lint files tuple

```python
LINT_FILES: tuple[str, ...] = (
    "hacking/pr_labeler/pr_labeler",
    "hacking/tagger/tag.py",
    "noxfile.py",
    *iglob("docs/bin/*.py"),
)
```

#### Updated lint files tuple

```python

LINT_FILES: tuple[str, ...] = (
    "hacking/pr_labeler/pr_labeler",
    "noxfile.py",
    *iglob("docs/bin/*.py"),
)
```

### Update Python versions in the support matrix

The minimum supported Python version changes with each Ansible core version.
This requires an update to the support matrix documentation after a new stable branch is created to reflect the appropriate Control Node Python versions.

Uncomment the new stable version from the `ansible-core support matrix` section in the `docs/docsite/rst/reference_appendices/release_and_maintenance.rst` file.
Submit a PR with the changes and request a core team review.
