.. _setting_up_environment:

###########################
Setting up your environment
###########################

Complete the following steps to set up a local environment for your first execution environment:

1. Ensure the following packages are installed on your system:

* ``podman`` or ``docker``
* ``python3``

If you use the DNF package manager, install these prerequisites as follows:

.. code-block:: bash

  sudo dnf install -y podman python3

2. Upgrade the `pip` package manager and install `ansible-navigator` to run EEs.

Installing `ansible-navigator` lets you run EEs.
It includes the `ansible-builder` package to build EEs.

.. code-block:: bash

  python3 -m pip install --upgrade pip ansible-navigator

3. Verify your environment with the following commands:

.. code-block:: bash

  ansible-navigator --version
  ansible-builder --version

Ready to build your first EE?
Proceed to :ref:`Building your first EE<building_execution_environments>`
