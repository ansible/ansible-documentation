.. _running_community_execution_environment:

*******************************************
Running Ansible with the community EE image
*******************************************

You can run ansible without the need to build a custom EE using community images.

Use the ``community-ee-minimal`` image that includes only ``ansible-core`` or the ``community-ee-base`` image that also includes several base collections.
Run the following command to see the collections included in the ``community-ee-base`` image:

.. code-block:: bash

   ansible-navigator collections --execution-environment-image ghcr.io/ansible-community/community-ee-base:latest

Run the following Ansible ad-hoc command against localhost inside the ``community-ee-minimal`` container:

.. code-block:: bash

   ansible-navigator exec "ansible localhost -m setup" --execution-environment-image ghcr.io/ansible-community/community-ee-minimal:latest --mode stdout

Now, create a simple test playbook and run it against ``localhost`` inside the container:

.. literalinclude:: yaml/test_localhost.yml
   :language: yaml

.. code-block:: bash

   ansible-navigator run test_localhost.yml --execution-environment-image ghcr.io/ansible-community/community-ee-minimal:latest --mode stdout

.. seealso::

   * :ref:`building_execution_environment`
   * :ref:`running_custom_execution_environment`
   * `Ansible Navigator documentation <https://ansible-navigator.readthedocs.io/>`_
