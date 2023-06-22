.. _build_and_test_ee:

*******************************************
Building and testing execution environments
*******************************************

.. note::

  Do you have any questions or ideas on how to improve this document?
  Please share them with us by creating an issue in the `GitHub repository <https://github.com/ansible/ansible-documentation/issues>`_.

This getting-started guide shows you how to build and test a simple execution environment.

For general information about execution environments, see the :ref:`getting_started_execution_environments` document.

.. _setting_up_environment:

Setting up your environment
===========================

Ensure the following packages are installed on your system:

* podman or docker
* python3

If you use the DNF as a package manager, you can install them as follows:

.. code-block:: bash

  sudo dnf install -y podman python3

Complete the following steps to set up a local environment for your first execution environment:

1. Upgrade the `pip` package manager and install `ansible-navigator`.

.. code-block:: bash

  python3 -m pip install --upgrade pip ansible-navigator

Installing `ansible-navigator` lets you run EEs.
It includes the `ansible-builder` package to build EEs.

You can verify your environment with the following commands:

.. code-block:: bash

  ansible-navigator --version
  ansible-builder --version

.. _build_first_ee:

Building your first EE
======================

We are going to build an EE containing, in addition to standard packages like ansible-core and Python,
an Ansible collection (``community.postgresql``) and its dependency (the ``psycopg2-binary`` Python connector).

The resulting image represents an :ref:`Ansible control node<terminology>` that contains:

* Python
* ansible-core
* ansible-runner
* the community.postgresql collection
* the psycopg2-binary Python package

To build your first ee, do the following:

1. Create a project folder on your filesystem.

.. code-block:: bash

  mkdir my_first_ee && cd my_first_ee

2. Create a ``execution-environment.yml`` file that specifies dependencies to include in the image.

.. code-block:: yaml

  cat > execution-environment.yml<<EOF
  ---
  version: 3

  dependencies:
    galaxy:
      collections:
      - name: community.postgresql
  EOF

.. note::

  The ``psycopg2-binary`` Python package is included in the ``requirements.txt`` file for the collection.
  For collections that do not include ``requirements.txt`` files, you need to specify Python dependencies explicitly.

3. Build a EE container image called ``postgresql_ee``. If you use docker, add the ``--container-runtime docker`` argument.

.. code-block:: bash

  ansible-builder build --tag postgresql_ee

4. List container images to verify that you built it successfully.

.. code-block:: bash

  podman image list

  localhost/postgresql_ee          latest      2e866777269b  6 minutes ago  1.11 GB

You can verify the image you created by inspecting the ``Containerfile`` or ``Dockerfile`` in the ``context`` directory to view its configuration.

.. code-block:: bash

  less context/Containerfile

You can also use Ansible Navigator to view detailed information about the image.

1. Run ``ansible-navigator``.
2. Type ``:images`` in the TUI and then choose ``postgresql_ee``.

Proceed to :ref:`Running your EE in command line<run_first_ee>` and test the EE you have just created.

.. _run_first_ee:

Running your EE in command line
===============================

Here, we will test the EE you created in the :ref:`Building your first EE<build_first_ee>` section against the localhost and a remote target.

Run against localhost
---------------------

1. Create a ``test_localhost.yml`` playbook.

.. code-block:: yaml

  cat > test_localhost.yml<<EOF
  ---
  - hosts: localhost
    become: yes
    gather_facts: yes
    tasks:
    - name: Print facts
      ansible.builtin.debug:
        msg: '{{ ansible_facts }}'
  EOF

2. Run the playbook inside the ``postgresql_ee`` EE.

.. code-block:: bash

  ansible-navigator run test_localhost.yml --execution-environment-image postgresql_ee --mode stdout --pull-policy missing

You may notice the facts being gathered are about the container and not the developer machine.
This is because the ansible playbook was run inside the container.

Run against a remote target
---------------------------

In this example, you execute a playbook inside the ``postgresql_ee`` EE against a remote host machine.
Before you start, ensure you have the following:

* At least one IP address or hostname for a remote target.
* Valid credentials for the remote host.
* Root or superuser permissions on the remote host.

1. Create a directory for inventory files.

.. code-block:: yaml

  mkdir inventory

2. Create the ``hosts.yml`` inventory file in the ``inventory`` directory.

.. code-block:: yaml

  cat > inventory/hosts.yml<<EOF
  ---
  all:
    hosts:
      192.168.0.2  # Replace with the IP of your target host
  EOF

3. Create a ``test_remote.yml`` playbook.

.. code-block:: yaml

  cat > test_remote.yml<<EOF
  ---
  - hosts: all
    become: yes
    gather_facts: yes
    tasks:
    - name: Print facts
      ansible.builtin.debug:
        msg: '{{ ansible_facts }}'
  EOF

4. Run the playbook inside the ``postgresql_ee`` EE. Replace ``student`` with the appropriate user name.

.. code-block:: bash

  ansible-navigator run test_remote.yml -i inventory --execution-environment-image postgresql_ee:latest --mode stdout --pull-policy missing --enable-prompts -u student -k -K

What to read next
=================

* More about the `EE definition file <https://ansible-builder.readthedocs.io/en/stable/definition/>`_ and available options.
* `Ansible Builder CLI usage <https://ansible-builder.readthedocs.io/en/stable/usage/>`_.
* `Ansible Navigator official documentation <https://ansible-navigator.readthedocs.io/>`_.
