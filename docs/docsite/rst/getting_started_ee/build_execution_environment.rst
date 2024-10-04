.. _building_execution_environment:

*****************************************
Building your first Execution Environment
*****************************************

We are going to build an EE that represents an Ansible control node containing standard packages such as ``ansible-core`` and Python in addition to an Ansible collection (``community.postgresql``) and its dependency (the ``psycopg2-binary`` Python connector).

To build your first EE:

#. Create a project folder on your filesystem.

   .. code-block:: bash

      mkdir my_first_ee && cd my_first_ee

#. Create a ``execution-environment.yml`` file that specifies dependencies to include in the image.

   .. literalinclude:: yaml/execution-environment.yml
      :language: yaml

   .. note::

      The `psycopg2-binary` Python package is included in the `requirements.txt` file for the collection.
      For collections that do not include `requirements.txt` files, you need to specify Python dependencies explicitly.
      See the `Ansible Builder documentation <https://ansible-builder.readthedocs.io/en/stable/definition/>`_ for details.

#. Build a EE container image called ``postgresql_ee``.

   If you use docker, add the ``--container-runtime docker`` argument.

   .. code-block:: bash

      ansible-builder build --tag postgresql_ee

#. List container images to verify that you built it successfully.

   .. code-block:: bash

      podman image list

      localhost/postgresql_ee          latest      2e866777269b  6 minutes ago  1.11 GB

You can verify the image you created by inspecting the ``Containerfile`` or ``Dockerfile`` in the ``context`` directory to view its configuration.

.. code-block:: bash

   less context/Containerfile

You can also use Ansible Navigator to view detailed information about the image.

Run the `ansible-navigator` command, type ``:images`` in the TUI, and then choose ``postgresql_ee``.

Proceed to :ref:`running_custom_execution_environment` and test the EE you just built.

.. seealso::

   `Running a local container registry for Execution Environments <https://forum.ansible.com/t/running-a-local-container-registry-for-execution-environments/206>`_
      This guide in the Ansible community forum explains how to set up a local registry for your Execution Environment images.
