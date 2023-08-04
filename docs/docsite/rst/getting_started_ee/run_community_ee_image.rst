.. _running_community_ee_image:

Running a playbook with the community EE image
===============================================

You can run ansible without the need to build a custom EE. 
Use the ``community-ee`` image that includes ``ansible-core`` and a set of Ansible community collections.

Run the following command to see the collections available in the ``community-ee`` image:

.. code-block:: bash

  ansible-navigator collections --execution-environment-image ghcr.io/ansible/community-ee:latest

Run the following Ansible ad-hoc command against localhost inside the ``community-ee`` container:

.. code-block:: bash

  ansible-navigator exec "ansible localhost -m setup" --execution-environment-image ghcr.io/ansible/community-ee:latest --mode stdout

What to read next
-----------------

* :ref:`Building your first EE guide<building_execution_environments>`
* `Ansible Navigator official documentation <https://ansible-navigator.readthedocs.io/>`_
* :ref:`The list of tools for EE<ansible_tooling_for_ee>`
