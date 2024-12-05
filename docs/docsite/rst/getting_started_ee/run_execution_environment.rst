.. _running_custom_execution_environment:

***************
Running your EE
***************

You can run your EE on the command line against ``localhost`` or a remote target using ``ansible-navigator``.

.. note::

   There are other tools besides ``ansible-navigator`` you can run EEs with.

Run against localhost
=====================

#. Create a ``test_localhost.yml`` playbook.

   .. literalinclude:: yaml/test_localhost.yml
      :language: yaml

#. Run the playbook inside the ``postgresql_ee`` EE.

   .. code-block:: bash

      ansible-navigator run test_localhost.yml --execution-environment-image postgresql_ee --mode stdout --pull-policy missing --container-options='--user=0'

You may notice the facts being gathered are about the container and not the developer machine.
This is because the ansible playbook was run inside the container.

Run against a remote target
===========================

Before you start, ensure you have the following:

  * At least one IP address or resolvable hostname for a remote target.
  * Valid credentials for the remote host.
  * A user with `sudo` permissions on the remote host.

Execute a playbook inside the ``postgresql_ee`` EE against a remote host machine as in the following example:

#. Create a directory for inventory files.

   .. code-block:: bash

      mkdir inventory

#. Create the ``hosts.yml`` inventory file in the ``inventory`` directory.

   .. literalinclude:: yaml/hosts.yml
      :language: yaml

#. Create a ``test_remote.yml`` playbook.

   .. literalinclude:: yaml/test_remote.yml
      :language: yaml

#. Run the playbook inside the ``postgresql_ee`` EE.

   Replace ``student`` with the appropriate username.
   Some arguments in the command can be optional depending on your target host authentication method.

   .. code-block:: bash

      ansible-navigator run test_remote.yml -i inventory --execution-environment-image postgresql_ee:latest --mode stdout --pull-policy missing --enable-prompts -u student -k -K

.. seealso::

   `Execution Environment Definition <https://ansible-builder.readthedocs.io/en/stable/definition/>`_
      Provides information about the about Execution Environment definition file and available options.
   `Ansible Builder CLI usage <https://ansible-builder.readthedocs.io/en/stable/usage/>`_
      Provides details about using Ansible Builder.
   `Ansible Navigator documentation <https://ansible-navigator.readthedocs.io/>`_
      Provides details about using Ansible Navigator.
   `Running a local container registry for EEs <https://forum.ansible.com/t/running-local-container-registry-for-execution-environments/206>`_
      This guide in the Ansible community forum explains how to set up a local registry for your Execution Environment images.
