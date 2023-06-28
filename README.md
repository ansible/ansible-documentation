# ansible-documentation

This repository holds the ReStructuredText (RST) source, and other files, for user documentation related to the Ansible package and Ansible core.

> Documentation for modules and plugins that are officially supported by the Ansible core engineering team is available in the [`ansible/ansible`](https://github.com/ansible/ansible) repository.

## Building Ansible community documentation

Complete the following steps to build Ansible community documentation from this repository:

* Optionally create a Python virtual environment.

    ```bash
    # Create a virtual environment in your current directory.
    python3 -m venv venv

    # Activate the virtual environment to start using it.
    source venv/bin/activate
    ```

1. Set up your environment.

    ```bash
    # Optionally upgrade the Python package manager and install build tools.
    python3 -m pip install --upgrade pip setuptools six wheel

    # Clone required parts of Ansible core for the docs build.
    python3 docs/bin/clone-core.py
    ```

2. Install required Python packages for the docs build.

    ```bash
    python3 -m pip install -r docs/docsite/requirements.txt
    ```

    There are two versions of the docs build requirements.
    For most cases you should install the development version as in the preceding step.

    If necessary, install tested docs build requirements from `tests/requirements.txt`.

3. Run the desired make target to build the documentation, for example:

    ```bash
    make coredocs -C docs/docsite
    ```

When the build succeeds, generated HTML is available in ``docs/docsite/_build/html``.

> To re-build the documentation, even for a different branch, you only need to run the desired make target again. You do not need to clone Ansible core or install requirements every time you build.
