.. _run_community_ee_image:

Running Ansible with the community EE image
===========================================

You can run ansible without the need to build a custom EE using community images.
Use the ``community-ee-minimal`` image that includes only ``ansible-core`` or
the ``community-ee-base`` image that also includes several base collections.

Run the following command to see the collections included in the ``community-ee-base`` image:

.. code-block:: bash

  ansible-navigator collections --execution-environment-image ghcr.io/ansible-community/community-ee-base:latest

Run the following Ansible ad-hoc command against localhost inside the ``community-ee-minimal`` container:

.. code-block:: bash

  ansible-navigator exec "ansible localhost -m setup" --execution-environment-image ghcr.io/ansible-community/community-ee-minimal:latest --mode stdout

Now, create a simple test playbook and run it against localhost inside the container:

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

.. code-block:: bash

  ansible-navigator run test_localhost.yml --execution-environment-image ghcr.io/ansible-community/community-ee-minimal:latest --mode stdout

See the :ref:`Running your EE guide<running_execution_environments_remote_target>` for an example of how to run your playbook against a remote target.

Ready to learn how to build an Execution Environment in a few easy steps?
Proceed to the :ref:`Building your first EE<building_execution_environments>`.

.. seealso::

   `Ansible Navigator documentation <https://ansible-navigator.readthedocs.io/>`_
       Learn more about the ansible-navigator utility.
   :ref:`The list of tools for EE<ansible_tooling_for_ee>`
       See the list of tools you can use Execution Environments with.
