.. _running_community_ee_image:

Running a playbook using the community EE image
===============================================

There is the ``community-ee`` image built with ``ansible-core`` and a set of popular collections
which you can use to run your playbooks without building your custom EE.

Run the following command to see the collections available in the ``community-ee`` image:

.. code-block:: bash

  ansible-navigator collections --execution-environment-image ghcr.io/ansible/community-ee:latest

To try out the EE, run the following ad hoc command against localhost inside the container.

.. code-block:: bash

  ansible-navigator exec "ansible localhost -m setup" --execution-environment-image ghcr.io/ansible/community-ee:latest --mode stdout

What to read next
-----------------

* :ref:`Building your first EE guide<building_execution_environments>`
* `Ansible Navigator official documentation <https://ansible-navigator.readthedocs.io/>`_
* :ref:`The list of tools for EE<ansible_tooling_for_ee>`
