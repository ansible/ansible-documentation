.. _running_community_ee_image:

Running Ansible with the community EE image
===========================================

You can run ansible without the need to build a custom EE. 
Use the ``community-ee`` image that includes ``ansible-core`` and a set of Ansible community collections.

Run the following command to see the collections available in the ``community-ee`` image:

.. code-block:: bash

  ansible-navigator collections --execution-environment-image ghcr.io/ansible/community-ee:latest

Run the following Ansible ad-hoc command against localhost inside the ``community-ee`` container:

.. code-block:: bash

  ansible-navigator exec "ansible localhost -m setup" --execution-environment-image ghcr.io/ansible/community-ee:latest --mode stdout

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

  ansible-navigator run test_localhost.yml --execution-environment-image ghcr.io/ansible/community-ee:latest --mode stdout

See the :ref:`Running your EE guide<running_execution_environments_remote_target>` for an example of how to run your playbook against a remote target.

What to read next
-----------------

* :ref:`Building your first execution environment<building_execution_environments>`
* `Ansible Navigator documentation <https://ansible-navigator.readthedocs.io/>`_
* :ref:`The list of tools for EE<ansible_tooling_for_ee>`
