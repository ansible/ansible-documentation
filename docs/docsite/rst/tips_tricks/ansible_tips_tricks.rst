.. _tips_and_tricks:

General tips
============

These concepts apply to all Ansible activities and artifacts.

Keep it simple
--------------

Whenever you can, do things simply.

Use advanced features only when necessary, and select the feature that best matches your use case.
For example, you will probably not need ``vars``, ``vars_files``, ``vars_prompt`` and ``--extra-vars`` all at once, while also using an external inventory file.

If something feels complicated, it probably is. Take the time to look for a simpler solution.

Use version control
-------------------

Keep your playbooks, roles, inventory, and variables files in ``git`` or another version control system and make commits with meaningful comments to the repository when you make changes.
Version control gives you an audit trail describing when and why you changed the rules that automate your infrastructure.

Customize the CLI output
-------------------------

You can change the output from Ansible CLI commands using :ref:`callback_plugins`.

Avoid configuration-dependent content
-------------------------------------

To ensure that your automation project is easy to understand, modify, and share with others, you should avoid configuration-dependent content. For example, rather than referencing an ``ansible.cfg`` as the root of a project, you can use magic variables such as ``playbook_dir`` or ``role_name`` to determine paths relative to known locations within your project directory. This can help to keep automation content flexible, reusable, and easy to maintain. For more information, see :ref:`special variables<special_variables>`.

.. _playbook_tips:

Playbook tips
=============

These tips help make playbooks and roles easier to read, maintain, and debug.

Use whitespace
--------------

Generous use of whitespace, for example, a blank line before each block or task, makes a playbook easy to scan.

Always name plays, tasks, and blocks
------------------------------------

Play, task, and block ``- name:``'s are optional, but extremely useful. In its output, Ansible shows you the name of each named entity it runs.
Choose names that describe what each play, task, and block does and why.

Always mention the state
------------------------

For many modules, the ``state`` parameter is optional.

Different modules have different default settings for ``state``, and some modules support several ``state`` settings.
Explicitly setting ``state: present`` or ``state: absent`` makes playbooks and roles clearer.

Use comments
------------

Even with task names and explicit states, sometimes a part of a playbook or role (or inventory/variable file) needs more explanation.
Adding a comment (any line starting with ``#``) helps others (and possibly yourself in the future) understand what a play or task (or variable setting) does, how it does it, and why.

Use fully qualified collection names
------------------------------------

Use `fully qualified collection names (FQCN) <https://docs.ansible.com/ansible/latest/reference_appendices/glossary.html#term-Fully-Qualified-Collection-Name-FQCN>`_ to avoid ambiguity in which collection to search for the correct module or plugin for each task.

For `builtin modules and plugins <https://docs.ansible.com/ansible/latest/collections/ansible/builtin/index.html#plugin-index>`_, use the ``ansible.builtin`` collection name as a prefix, for example, ``ansible.builtin.copy``.

.. _inventory_tips:

Inventory tips
==============

These tips help keep your inventory well organized.

Use dynamic inventory with clouds
---------------------------------

With cloud providers and other systems that maintain canonical lists of your infrastructure, use :ref:`dynamic inventory <intro_dynamic_inventory>` to retrieve those lists instead of manually updating static inventory files.
With cloud resources, you can use tags to differentiate production and staging environments.

Group inventory by function
---------------------------

A system can be in multiple groups.  See :ref:`intro_inventory` and :ref:`intro_patterns`.
If you create groups named for the function of the nodes in the group, for example, ``webservers`` or ``dbservers``, your playbooks can target machines based on function.
You can assign function-specific variables using the group variable system, and design Ansible roles to handle function-specific use cases.
See :ref:`playbooks_reuse_roles`.

Separate production and staging inventory
-----------------------------------------

You can keep your production environment separate from development, test, and staging environments by using separate inventory files or directories for each environment.
This way you pick with -i what you are targeting.
Keeping all your environments in one file can lead to surprises!
For example, all vault passwords used in an inventory need to be available when using that inventory.
If an inventory contains both production and development environments, developers using that inventory would be able to access production secrets.

.. _tip_for_variables_and_vaults:

Keep vaulted variables safely visible
-------------------------------------

You should encrypt sensitive or secret variables with Ansible Vault.
However, encrypting the variable names as well as the variable values makes it hard to find the source of the values.
To circumvent this, you can encrypt the variables individually using ``ansible-vault encrypt_string``, or add the following layer of indirection to keep the names of your variables accessible (by ``grep``, for example) without exposing any secrets:

#. Create a ``group_vars/`` subdirectory named after the group.
#. Inside this subdirectory, create two files named ``vars`` and ``vault``.
#. In the ``vars`` file, define all of the variables needed, including any sensitive ones.
#. Copy all of the sensitive variables over to the ``vault`` file and prefix these variables with ``vault_``.
#. Adjust the variables in the ``vars`` file to point to the matching ``vault_`` variables using jinja2 syntax: ``db_password: "{{ vault_db_password }}"``.
#. Encrypt the ``vault`` file to protect its contents.
#. Use the variable name from the ``vars`` file in your playbooks.

When running a playbook, Ansible finds the variables in the unencrypted file, which pulls the sensitive variable values from the encrypted file.
There is no limit to the number of variable and vault files or their names.

Note that using this strategy in your inventory still requires *all vault passwords to be available* (for example for ``ansible-playbook`` or `AWX/Ansible Tower <https://github.com/ansible/awx/issues/223#issuecomment-768386089>`_) when run with that inventory.

.. _execution_tips:

Execution tricks
================

These tips apply to using Ansible, rather than to Ansible artifacts.

Use Execution Environments
--------------------------

Reduce complexity with portable container images known as :ref:`Execution Environments<getting_started_ee_index>`.

Try it in staging first
-----------------------

Testing changes in a staging environment before rolling them out in production is always a great idea.
Your environments need not be the same size, and you can use group variables to control the differences between environments. You can also check for any syntax errors in the staging environment using the flag ``--syntax-check`` such as in the following example:

.. code-block:: yaml

      ansible-playbook --syntax-check

Update in batches
-----------------

Use the ``serial`` keyword to control how many machines you update at once in the batch.
See :ref:`playbooks_delegation`.

.. _os_variance:

Handling OS and distro differences
----------------------------------

Group variables files and the ``group_by`` module work together to help Ansible execute across a range of operating systems and distributions that require different settings, packages, and tools.
The ``group_by`` module creates a dynamic group of hosts that match certain criteria.
This group does not need to be defined in the inventory file.
This approach lets you execute different tasks on different operating systems or distributions.

For example, the following play categorizes all systems into dynamic groups based on the operating system name:

.. literalinclude:: yaml/tip_group_by.yaml
      :language: yaml

Subsequent plays can use these groups as patterns on the ``hosts`` line as follows:

.. literalinclude:: yaml/tip_group_hosts.yaml
      :language: yaml

You can also add group-specific settings in group vars files.
In the following example, CentOS machines get the value of '42' for `asdf` but other machines get '10'.
You can also use group vars files to apply roles to systems as well as set variables.

.. code-block:: yaml

   ---
   # file: group_vars/all
   asdf: 10

   ---
   # file: group_vars/os_CentOS.yml
   asdf: 42

.. note::
   All three names must match: the name created by the ``group_by`` task, the name of the pattern in subsequent plays, and the name of the group vars file.

You can use the same setup with ``include_vars`` when you only need OS-specific variables, not tasks:

.. literalinclude:: yaml/tip_include_vars.yaml
      :language: yaml

This pulls in variables from the `group_vars/os_CentOS.yml` file.

.. seealso::

   :ref:`yaml_syntax`
       Learn about YAML syntax
   :ref:`working_with_playbooks`
       Review the basic playbook features
   :ref:`list_of_collections`
       Browse existing collections, modules, and plugins
   :ref:`developing_modules`
       Learn how to extend Ansible by writing your own modules
   :ref:`intro_patterns`
       Learn about how to select hosts
   :ref:`Communication<communication>`
       Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide
