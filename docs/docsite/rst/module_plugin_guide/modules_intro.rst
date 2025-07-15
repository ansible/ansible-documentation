.. _intro_modules:

Introduction to modules
=======================

Modules (also referred to as "task plugins" or "library plugins") are discrete units of code that can be used from the command line or in a playbook task. Ansible executes each module, usually on the remote managed node, and collects return values. In Ansible 2.10 and later, most modules are hosted in collections.

You can execute modules from the command line.

.. code-block:: shell-session

    ansible webservers -m service -a "name=httpd state=started"
    ansible webservers -m ping
    ansible webservers -m command -a "/sbin/reboot -t now"

Each module supports arguments.  Nearly all modules take ``key=value`` arguments, space delimited.  Some modules take no arguments, and the command/shell modules simply take the string of the command you want to run.

From playbooks, Ansible modules are executed in a very similar way.

.. code-block:: yaml

    - name: reboot the servers
      command: /sbin/reboot -t now

Another way to pass arguments to a module is using YAML syntax, also called 'complex args'.

.. code-block:: yaml

    - name: restart webserver
      service:
        name: httpd
        state: restarted

All modules return JSON format data. This means modules can be written in any programming language. Modules should be idempotent, and should avoid making any changes if they detect that the current state matches the desired final state. When used in an Ansible playbook, modules can trigger 'change events' in the form of notifying :ref:`handlers <handlers>` to run additional tasks.

You can access the documentation for each module from the command line with the ansible-doc tool.

.. code-block:: shell-session

    ansible-doc yum

For a list of all available modules, see the :ref:`Collection docs <list_of_collections>`, or run the following at a command prompt.

.. code-block:: shell-session

    ansible-doc -l

.. _boolean_variables:

Boolean variables
=================

Ansible accepts a broad range of values for ``bool`` in module arguments: ``true/false``, ``1/0``, ``yes/no``, ``True/False`` and so on. The matching of valid strings is case insensitive.
While documentation examples focus on ``true/false`` to be compatible with ``ansible-lint`` default settings, you can use any of the following:

.. table::
   :class: documentation-table

   ========================================================================================================== ====================================================================
    Valid values                                                                                               Description
   ========================================================================================================== ====================================================================
    ``True`` , ``'true'`` , ``'t'`` , ``'yes'`` , ``'y'`` , ``'on'`` , ``'1'`` , ``1`` , ``1.0``                 Truthy values

    ``False`` , ``'false'`` , ``'f'`` , ``'no'`` , ``'n'`` , ``'off'`` , ``'0'`` , ``0`` , ``0.0``               Falsy values

   ========================================================================================================== ====================================================================

.. seealso::

   :ref:`intro_adhoc`
       Examples of using modules in /usr/bin/ansible
   :ref:`working_with_playbooks`
       Examples of using modules with /usr/bin/ansible-playbook
   :ref:`developing_modules`
       How to write your own modules
   :ref:`developing_api`
       Examples of using modules with the Python API
   :ref:`Communication<communication>`
       Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide
   :ref:`all_modules_and_plugins`
       All modules and plugins available
