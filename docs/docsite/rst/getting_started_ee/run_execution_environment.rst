.. _running_execution_environments:

Running your EE
===============

You can run your EE on the command line against ``localhost`` or a remote target
using ``ansible-navigator``.

.. note::

  There are other tools besides ``ansible-navigator`` you can run EEs with.

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

* At least one IP address or resolvable hostname for a remote target.
* Valid credentials for the remote host.
* A user with ``sudo`` permissions on the remote host.

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
-----------------

* More about the `EE definition file <https://ansible-builder.readthedocs.io/en/stable/definition/>`_ and available options.
* `Ansible Builder CLI usage <https://ansible-builder.readthedocs.io/en/stable/usage/>`_.
* `Ansible Navigator official documentation <https://ansible-navigator.readthedocs.io/>`_.
* :ref:`The list of tools for EE<ansible_tooling_for_ee>`
