# ansible-documentation

This repository holds the ReStructuredText (RST) source, and other files, for user documentation related to the Ansible package and Ansible core.

> Documentation for modules and plugins that are officially supported by the Ansible core engineering team is available in the [`ansible/ansible`](https://github.com/ansible/ansible) repository.

## Building Ansible community documentation

Follow the documentation to [set up your environment](https://docs.ansible.com/ansible/latest/community/documentation_contributions.html#setting-up-your-environment-to-build-documentation-locally) and then [build Ansible community documentation locally](https://docs.ansible.com/ansible/latest/community/documentation_contributions.html#building-the-documentation-locally)

## Updating the dependencies

To update dependencies, you can use `nox -e pip-compile`. Since this requires Python 3.10, this might not work in your environment if you do not have Python 3.10 installed. In that case, you can use root-less podman with a Python 3.10 image:
```bash
podman run --rm --tty --volume "$(pwd):/mnt" --workdir /mnt python:3.10 /bin/bash -c 'pip install nox ; nox -e pip-compile'
```
