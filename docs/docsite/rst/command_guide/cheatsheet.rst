.. _cheatsheet:

**********************
Ansible CLI cheatsheet
**********************

This page shows one or more examples of each Ansible command line utility with some common flags added and a link to the full documentation for the command.
This page offers a quick reminder of some common use cases only - it may be out of date or incomplete or both.
For canonical documentation, follow the links to the CLI pages.

.. contents::
   :local:

ansible-playbook
================

.. code-block:: bash

   ansible-playbook -i /path/to/my_inventory_file -u my_connection_user -k -f 3 -T 30 -t my_tag -M /path/to/my_modules -b -K my_playbook.yml

Loads ``my_playbook.yml`` from the current working directory and:
  - ``-i`` - uses ``my_inventory_file`` in the path provided for :ref:`inventory <intro_inventory>` to match the :ref:`pattern <intro_patterns>`.
  - ``-u`` - connects :ref:`over SSH <connections>` as ``my_connection_user``.
  - ``-k`` - asks for password which is then provided to SSH authentication.
  - ``-f`` - allocates 3 :ref:`forks <playbooks_strategies>`.
  - ``-T`` - sets a 30-second timeout.
  - ``-t`` - runs only tasks marked with the :ref:`tag <tags>` ``my_tag``.
  - ``-M`` - loads :ref:`local modules <developing_locally>` from ``/path/to/my/modules``.
  - ``-b`` - executes with elevated privileges (uses :ref:`become <become>`).
  - ``-K`` - prompts the user for the become password.

See :ref:`ansible-playbook` for detailed documentation.


ansible-galaxy
==============

Installing collections
^^^^^^^^^^^^^^^^^^^^^^

* Install a single collection:

.. code-block:: bash

    ansible-galaxy collection install mynamespace.mycollection

Downloads ``mynamespace.mycollection`` from the configured Galaxy server (`galaxy.ansible.com` by default).

* Install a list of collections:

.. code-block:: bash

    ansible-galaxy collection install -r requirements.yml

Downloads the list of collections specified in the ``requirements.yml`` file.

* List all installed collections:

.. code-block:: bash

  ansible-galaxy collection list

Installing roles
^^^^^^^^^^^^^^^^

* Install a role named `example.role`:

.. code-block:: bash

  ansible-galaxy role install example.role

  <SNIPPED>
  - extracting example.role to /home/user/.ansible/roles/example.role
  - example.role (0.0.1) was installed successfully


* List all installed roles:

.. code-block:: bash

  ansible-galaxy role list

See :ref:`ansible-galaxy` for detailed documentation.
