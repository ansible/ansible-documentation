.. _building_execution_environments:

######################
Building your first EE
######################

We are going to build an EE that represents an Ansible control node containing standard packages such as ``ansible-core`` and Python in addition to
an Ansible collection (``community.postgresql``) and its dependency (the ``psycopg2-binary`` Python connector).

To build your first EE:

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

Run the ``ansible-navigator`` command, type ``:images`` in the TUI, and then choose ``postgresql_ee``.

Proceed to :ref:`Running your EE<running_execution_environments>` and test the EE you just built.
