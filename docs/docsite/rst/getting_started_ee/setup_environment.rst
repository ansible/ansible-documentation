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

2. Install ``ansible-navigator``:

.. code-block:: bash

  pip3 install ansible-navigator

Installing ``ansible-navigator`` lets you run EEs on the command line.
It includes the ``ansible-builder`` package to build EEs.

If you want to build EEs without testing, install only ``ansible-builder``:

.. code-block:: bash

  pip3 install ansible-builder

3. Verify your environment with the following commands:

.. code-block:: bash

  ansible-navigator --version
  ansible-builder --version

Ready to build your first EE?
Proceed to :ref:`Building your first EE<building_execution_environments>`
