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
  - name: Gather and print local facts
    hosts: localhost
    become: yes
    gather_facts: yes
    tasks:

    - name: Print facts
      ansible.builtin.debug:
        var: ansible_facts
  EOF

2. Run the playbook inside the ``postgresql_ee`` EE.

.. code-block:: bash

  ansible-navigator run test_localhost.yml --execution-environment-image postgresql_ee --mode stdout --pull-policy missing

You may notice the facts being gathered are about the container and not the developer machine.
This is because the ansible playbook was run inside the container.

.. _running_execution_environments_remote_target:

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
  all:
    hosts:
      192.168.0.2  # Replace with the IP of your target host
  EOF

3. Create a ``test_remote.yml`` playbook.

.. code-block:: yaml

  cat > test_remote.yml<<EOF
  - name: Gather and print facts
    hosts: all
    become: yes
    gather_facts: yes
    tasks:

    - name: Print facts
      ansible.builtin.debug:
        var: ansible_facts
  EOF

4. Run the playbook inside the ``postgresql_ee`` EE. Replace ``student`` with the appropriate username.

.. code-block:: bash

  ansible-navigator run test_remote.yml -i inventory --execution-environment-image postgresql_ee:latest --mode stdout --pull-policy missing --enable-prompts -u student -k -K

.. seealso::

   `Execution Environment Definition <https://ansible-builder.readthedocs.io/en/stable/definition/>`_
       More about Execution Environment definition file and available options.
   `Ansible Builder CLI usage <https://ansible-builder.readthedocs.io/en/stable/usage/>`_
       Find out more about Ansible Builder's command-line arguments.
   `Ansible Navigator documentation <https://ansible-navigator.readthedocs.io/>`_
       Learn more about the ansible-navigator utility.
   :ref:`The list of tools for EE<ansible_tooling_for_ee>`
       See the list of tools you can use Execution Environments with.
   :ref:`Running community EE guide<run_community_ee_image>`
       Learn more about running the community-provided Execution Environment.
   `Running a local container registry for EE <https://forum.ansible.com/t/running-local-container-registry-for-execution-environments/206>`_
       Learn how to quickly set up a local container registry for your Execution Environments.
