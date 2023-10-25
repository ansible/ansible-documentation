# ansible-documentation

This repository holds the ReStructuredText (RST) source, and other files, for user documentation related to the Ansible package and Ansible core.

> Documentation for modules and plugins that are officially supported by the Ansible core engineering team is available in the [`ansible/ansible`](https://github.com/ansible/ansible) repository.

## Building Ansible community documentation

Follow the documentation to [set up your environment](https://docs.ansible.com/ansible/latest/community/documentation_contributions.html#setting-up-your-environment-to-build-documentation-locally) and then [build Ansible community documentation locally](https://docs.ansible.com/ansible/latest/community/documentation_contributions.html#building-the-documentation-locally)

## Using nox

This project includes a `nox` configuration to automate checks and other functions.
You should use `nox` to run checks locally before you submit a pull request.

Install `nox` using `python3 -m pip install nox` or your distribution's package manager.

Run `nox --list` from the repository root to view available sessions.

Run `nox` with no arguments to execute the default sessions.

## Running the spelling check

This repository uses [`codespell`](https://github.com/codespell-project/codespell) to check for common spelling mistakes in the documentation source.

Run `nox -s spelling` to check spelling.

Run `nox -s spelling -- -w` to correct spelling errors.

When `codespell` suggests more than one word as a correction, run `nox -s spelling -- -w -i 3` to select an option.

## Updating the dependencies

To update dependencies, you can use `nox -e pip-compile`. Since this requires Python 3.10, this might not work in your environment if you do not have Python 3.10 installed. In that case, you can use root-less podman with a Python 3.10 image:
```bash
podman run --rm --tty --volume "$(pwd):/mnt:z" --workdir /mnt python:3.10 bash -c 'pip install nox ; nox -e pip-compile'
```
