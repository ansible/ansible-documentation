.. _running_community_ee_image:

Running a playbook using the community EE image
===============================================

There is the ``community-ee`` image built with ``ansible-core`` and a set of popular collections
which you can use to run your playbooks without building your custom EE.

Run the following command to see the included collections.

.. code-block:: bash

  ansible-navigator collections --execution-environment-image ghcr.io/ansible/community-ee:latest

To try out the EE, create a simple test playbook and run it against localhost inside the container.

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

What to read next
-----------------

* :ref:`Building your first EE guide<building_execution_environments>`
* `Ansible Navigator official documentation <https://ansible-navigator.readthedocs.io/>`_
* :ref:`The list of tools for EE<ansible_tooling_for_ee>`
