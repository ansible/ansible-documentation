.. _installation_guide:
.. _intro_installation_guide:

******************
Installing Ansible
******************

Ansible is an agentless automation tool that runs on a single host, called the **control node**. From the control node, Ansible remotely manages a fleet of machines and other devices, called **managed nodes**. It requires no databases or daemons and uses SSH, PowerShell Remoting, and other transports from a command-line interface.

.. contents::
  :local:

.. _control_node_requirements:

Control node requirements
=========================

The **control node**, the machine that runs Ansible, must be a UNIX-like machine with Python installed. Supported systems include Red Hat, Debian, Ubuntu, macOS, BSDs, and Windows with a `Windows Subsystem for Linux (WSL) distribution <https://docs.microsoft.com/en-us/windows/wsl/about>`_. A native Windows host cannot be a control node. For more information, see `this blog post <http://blog.rolpdog.com/2020/03/why-no-ansible-controller-for-windows.html>`_.

.. _managed_node_requirements:

Managed node requirements
=========================

A **managed node**, the device that Ansible manages, does not require Ansible. By default, it requires Python to run Ansible modules. The managed node also needs a user account that can connect to the node through SSH with an interactive POSIX shell.

.. note::

   Some modules, such as network modules, do not require Python on the managed device. For specific requirements, see the documentation for each module.

.. _node_requirements_summary:

Node requirement summary
========================

For detailed requirements, including supported Python versions for each Ansible release, see the :ref:`support_life` and :ref:`ansible_core_support_matrix` sections.

.. _getting_ansible:

.. _what_version:

Selecting an Ansible package and version to install
====================================================

Ansible provides two community packages:

* ``ansible-core``: A minimalist package that contains the language, runtime, and a set of `built-in modules and plugins <plugins_in_ansible.builtin>`_.
* ``ansible``: A "batteries included" package that adds a community-curated selection of :ref:`Ansible Collections <collections>` for automating many different devices.

Choose the package that fits your needs. The following instructions use ``ansible``, but you can substitute ``ansible-core`` if you prefer the minimal package.

You can install ``ansible`` or ``ansible-core`` from your OS package manager. For more information, see the :ref:`installing_distros` guide. These instructions cover only the official installation method, which uses ``pip``.

See the :ref:`Ansible package release status table<ansible_changelogs>` for the ``ansible-core`` version included in each ``ansible`` package.

Installing and upgrading Ansible with pipx
==========================================

Some operating systems restrict ``pip``, which prevents a direct Ansible installation. In these cases, use ``pipx`` as an alternative.

This guide does not cover ``pipx`` installation. For instructions, see the `pipx installation instructions`_.

.. _pipx installation instructions: https://pypa.github.io/pipx/installation/

.. _pipx_install:

Installing Ansible
------------------

To install the ``ansible`` package, run:

.. code-block:: console

    $ pipx install --include-deps ansible

To install the minimal ``ansible-core`` package, run:

.. code-block:: console

    $ pipx install ansible-core

To install a specific version of ``ansible-core``, run:

.. code-block:: console

    $ pipx install ansible-core==2.12.3

.. _pipx_upgrade:

Upgrading Ansible
-----------------

To upgrade an existing ``ansible`` package to the latest version, run:

.. code-block:: console

    $ pipx upgrade --include-injected ansible

.. _pipx_inject:

Installing Extra Python Dependencies
------------------------------------

To install an additional Python dependency, such as ``argcomplete``, run:

.. code-block:: console

    $ pipx inject ansible argcomplete

To add an application's executables to your PATH, use the ``--include-apps`` option. This option lets you run the application's commands from the shell.

.. code-block:: console

    $ pipx inject --include-apps ansible argcomplete

To install dependencies from a ``requirements.txt`` file, use the ``pipx runpip`` command. For example, to install the Azure collection dependencies:

.. code-block:: console

    $ pipx runpip ansible install -r ~/.ansible/collections/ansible_collections/azure/azcollection/requirements.txt


Installing and upgrading Ansible with pip
=========================================

This procedure describes how to install Ansible with ``pip``. It covers locating Python, ensuring ``pip`` is available, and installing or upgrading Ansible.

Locating Python
---------------

First, locate the Python interpreter that you want to use. This guide refers to it as ``python3``. If your Python interpreter is at a specific path, such as ``/usr/bin/python3.9``, use that full path instead of ``python3`` in the following commands.

Ensuring ``pip`` is available
-----------------------------

To verify that ``pip`` is available for your chosen Python interpreter, run:

.. code-block:: console

    $ python3 -m pip -V

A successful command returns output similar to this:

.. code-block:: console

    $ python3 -m pip -V
    pip 21.0.1 from /usr/lib/python3.9/site-packages/pip (python 3.9)

If ``pip`` is available, go to the :ref:`next step <pip_install>`.

If you see a ``No module named pip`` error, you must install ``pip`` before you continue. You can install an OS package, such as ``python3-pip``, or you can install ``pip`` directly from the Python Packaging Authority:

.. code-block:: console

    $ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    $ python3 get-pip.py --user

You might need more configuration to run Ansible. For details, see the Python documentation on `installing to the user site`_.

.. _installing to the user site: https://packaging.python.org/tutorials/installing-packages/#installing-to-the-user-site

.. _pip_install:

Installing Ansible
------------------

To install the ``ansible`` package for the current user, run:

.. code-block:: console

    $ python3 -m pip install --user ansible

To install the minimal ``ansible-core`` package for the current user, run:

.. code-block:: console

    $ python3 -m pip install --user ansible-core

To install a specific version of ``ansible-core``, run:

.. code-block:: console

    $ python3 -m pip install --user ansible-core==2.12.3

.. _pip_upgrade:

Upgrading Ansible
-----------------

To upgrade an existing ``ansible`` package to the latest version, add the ``--upgrade`` option to the install command:

.. code-block:: console

    $ python3 -m pip install --upgrade --user ansible

Installing Ansible to containers
================================

You can use a container as your control node instead of installing Ansible manually. Build an execution environment container image or use an available community image. See :ref:`getting_started_ee_index` for details.

.. _development_install:

Installing for development
==========================

To test new features, fix bugs, or contribute to the ``ansible-core`` code, you can install and run Ansible from the GitHub source repository.

.. note::

   Install the ``devel`` branch only if you are modifying ``ansible-core`` or testing features in development. The ``devel`` branch code changes rapidly and can be unstable.

For more information on getting involved in the Ansible project, see the :ref:`ansible_community_guide`.

For more information on creating Ansible modules and Collections, see the :ref:`developer_guide`.

.. _from_pip_devel:

Installing ``devel`` from GitHub with ``pip``
---------------------------------------------

To install the ``devel`` branch of ``ansible-core`` from GitHub with ``pip``, run:

.. code-block:: console

    $ python3 -m pip install --user https://github.com/ansible/ansible/archive/devel.tar.gz

You can replace ``devel`` in the URL with another branch name or tag to install other versions, such as tagged alphas, betas, or release candidates.

.. _from_source:

Running the ``devel`` branch from a clone
-----------------------------------------

This procedure describes how to clone the ``ansible-core`` GitHub repository and run the ``devel`` branch from the source code.

You can run ``ansible-core`` from a source clone without ``root`` permissions or software installation. No daemons or database setup are required.

#. Clone the ``ansible-core`` repository.

   .. code-block:: console

      $ git clone https://github.com/ansible/ansible.git
      $ cd ./ansible

#. Set up the Ansible environment by sourcing the ``env-setup`` script.
   The script provides options for different shells.

   For Bash:

     .. code-block:: console

        $ source ./hacking/env-setup

   For the Fish shell:

     .. code-block:: console

        $ source ./hacking/env-setup.fish

   To suppress warnings and errors, add the ``-q`` flag:

     .. code-block:: console

        $ source ./hacking/env-setup -q

#. Install Python dependencies.

     .. code-block:: console

        $ python3 -m pip install --user -r ./requirements.txt

#. Update the ``devel`` branch on your local machine.
   Use ``git pull --rebase`` to replay any local changes.

     .. code-block:: console

        $ git pull --rebase

.. _shell_completion:

Confirming your installation
============================

To confirm that Ansible is installed correctly, check the version:

.. code-block:: console

    $ ansible --version

This command displays the version of the installed ``ansible-core`` package.

To check the version of the installed ``ansible`` community package, run:

.. code-block:: console

    $ ansible-community --version

Adding Ansible command shell completion
=======================================

This procedure describes how to install and configure ``argcomplete`` to add shell completion for Ansible command-line utilities.

You can add shell completion for Ansible command-line utilities by installing ``argcomplete``. Argcomplete supports Bash and has limited support for zsh and tcsh.

For more information about installation and configuration, see the `argcomplete documentation <https://kislyuk.github.io/argcomplete/>`_.

Installing ``argcomplete``
--------------------------

If you installed Ansible with ``pipx``, run:

.. code-block:: console

    $ pipx inject --include-apps ansible argcomplete

If you installed Ansible with ``pip``, run:

.. code-block:: console

    $ python3 -m pip install --user argcomplete

Configuring ``argcomplete``
---------------------------

You can configure ``argcomplete`` for shell completion in two ways: globally or per command.

Global configuration
^^^^^^^^^^^^^^^^^^^^

Global completion requires Bash 4.2 or higher.

.. code-block:: console

   $ activate-global-python-argcomplete --user

This command writes a Bash completion file to a user location. To change the location, use the ``--dest`` option. To set up completion globally, use ``sudo``.

Per command configuration
^^^^^^^^^^^^^^^^^^^^^^^^^

If you do not have Bash 4.2 or higher, you must register each script independently.

.. code-block:: console

    $ eval $(register-python-argcomplete ansible)
    $ eval $(register-python-argcomplete ansible-config)
    $ eval $(register-python-argcomplete ansible-console)
    $ eval $(register-python-argcomplete ansible-doc)
    $ eval $(register-python-argcomplete ansible-galaxy)
    $ eval $(register-python-argcomplete ansible-inventory)
    $ eval $(register-python-argcomplete ansible-playbook)
    $ eval $(register-python-argcomplete ansible-pull)
    $ eval $(register-python-argcomplete ansible-vault)

Add these commands to your shell's profile file, for example, ``~/.profile`` or ``~/.bash_profile``.

Using ``argcomplete`` with zsh or tcsh
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See the `argcomplete documentation <https://kislyuk.github.io/argcomplete/>`_.


.. seealso::

   :ref:`intro_adhoc`
       Examples of basic Ansible commands.
   :ref:`working_with_playbooks`
       Learn Ansible's playbook language for configuration management.
   :ref:`installation_faqs`
       Frequently asked questions about installing Ansible.
   :ref:`ansible_forum`
       Join the Ansible community forum for help and insights.
   :ref:`communication_irc`
       Join Ansible chat channels.
