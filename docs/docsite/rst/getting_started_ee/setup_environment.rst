.. _setting_up_ee_environment:

***************************
Setting up your environment
***************************

Complete the following steps to set up a local environment for your first Execution Environment:

#. Ensure the following packages are installed on your system:

    * ``podman`` or ``docker``
    * ``python3``
    * ``python3-pip``

    If you use the DNF package manager, install these prerequisites as follows:

    .. code-block:: bash

       sudo dnf install -y podman python3 python3-pip

#. Install ``ansible-navigator``:

    .. code-block:: bash

       pip3 install ansible-navigator

    Installing ``ansible-navigator`` lets you run EEs on the command line.
    It includes the ``ansible-builder`` package to build EEs.

    If you want to build EEs without testing, install only ``ansible-builder``:

    .. code-block:: bash

       pip3 install ansible-builder

#. Verify your environment with the following commands:

    .. code-block:: bash

       ansible-navigator --version
       ansible-builder --version

Ready to build an EE in a few easy steps? Proceed to :ref:`building_execution_environment`.

Want to try an EE without having to build one? Proceed to :ref:`running_community_execution_environment`.
