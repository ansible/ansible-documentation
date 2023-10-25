.. _shell_plugins:

Shell plugins
=============

.. contents::
   :local:
   :depth: 2

Shell plugins work to ensure that the basic commands Ansible runs are properly formatted to work with
the target machine and allow the user to configure certain behaviors related to how Ansible executes tasks.

.. _enabling_shell:

Enabling shell plugins
----------------------

You can add a custom shell plugin by dropping it into a ``shell_plugins`` directory adjacent to your play, inside a role,
or by putting it in one of the shell plugin directory sources configured in :ref:`ansible.cfg <ansible_configuration_settings>`.

.. warning:: You should not alter which plugin is used unless you have a setup in which the default ``/bin/sh``
 is not a POSIX compatible shell or is not available for execution.

.. _using_shell:

Using shell plugins
-------------------

In addition to the default configuration settings in :ref:`ansible_configuration_settings`, you can use
the connection variable :ref:`ansible_shell_type <ansible_shell_type>` to select the plugin to use.
In this case, you will also want to update the :ref:`ansible_shell_executable <ansible_shell_executable>` to match.

You can further control the settings for each plugin with other configuration options
detailed in the plugin themselves (linked below).

.. seealso::

   :ref:`about_playbooks`
       An introduction to playbooks
   :ref:`inventory_plugins`
       Inventory plugins
   :ref:`callback_plugins`
       Callback plugins
   :ref:`filter_plugins`
       Filter plugins
   :ref:`test_plugins`
       Test plugins
   :ref:`lookup_plugins`
       Lookup plugins
   `User Mailing List <https://groups.google.com/group/ansible-devel>`_
       Have a question?  Stop by the Google group!
   :ref:`communication_irc`
       How to join Ansible chat channels
