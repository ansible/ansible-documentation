.. _intro_inventory:
.. _inventory:

***************************
How to build your inventory
***************************

Ansible automates tasks on managed nodes or "hosts" in your infrastructure by using a list or group of lists known as inventory. Ansible composes its inventory from one or more 'inventory sources'. While one of these sources can be the list of host names you pass at the command line, most Ansible users create inventory files. Your inventory defines the managed nodes you automate and the variables associated with those hosts. You can also specify groups. Groups allow you to reference multiple associated hosts to target for your automation or to define variables in bulk.
Once you define your inventory, you use :ref:`patterns <intro_patterns>` to select the hosts or groups you want Ansible to run against.

The simplest inventory is a single file that contains a list of hosts and groups. The default location for this file is ``/etc/ansible/hosts``. You can specify a different inventory source or sources at the command line by using the ``-i <path or expression>`` option or by using the configuration system.

Ansible :ref:`inventory_plugins` supports a range of formats and sources, which makes your inventory flexible and customizable. As your inventory expands, you might need more than a single file to organize your hosts and groups. You have the following common options beyond the ``/etc/ansible/hosts`` file:

- You can generate an inventory dynamically. For example, you can use an inventory plugin to list resources in one or more cloud providers or other sources. See :ref:`intro_dynamic_inventory`.
- You can use multiple sources for inventory, including both dynamic inventory and static files. See :ref:`using_multiple_inventory_sources`.
- You can create a directory with multiple inventory sources, static or dynamic. See :ref:`inventory_directory`.

.. contents::
   :local:

The following YAML snippets include an ellipsis (...) to indicate that the snippets are part of a larger YAML file. You can find out more about YAML syntax at `YAML Basics <https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html#yaml-basics">`_.

.. _inventoryformat:

Inventory basics: formats, hosts, and groups
============================================

You can create your inventory file in one of many formats, depending on the inventory plugins you have.
The most common formats are INI and YAML because Ansible includes built-in support for them. This introduction focuses on these two formats, but many other formats and sources are possible.

A basic INI ``/etc/ansible/hosts`` might look like this:

.. code-block:: text

    mail.example.com

    [webservers]
    foo.example.com
    bar.example.com

    [dbservers]
    one.example.com
    two.example.com
    three.example.com

The headings in brackets are group names. You can use group names to classify hosts
and to decide which hosts you are controlling at what times and for what purpose.
Group names should follow the same guidelines as :ref:`valid_variable_names`.

Here's the same basic inventory file in YAML format:

.. code-block:: yaml

  ungrouped:
    hosts:
      mail.example.com:
  webservers:
    hosts:
      foo.example.com:
      bar.example.com:
  dbservers:
    hosts:
      one.example.com:
      two.example.com:
      three.example.com:

.. _default_groups:

Default groups
--------------

Even if you do not define any groups in your inventory, Ansible creates two default groups: ``all`` and ``ungrouped``. The ``all`` group contains every host. The ``ungrouped`` group contains all hosts that do not belong to any other group.
Every host always belongs to at least two groups (``all`` and ``ungrouped``, or ``all`` and another group). For example, in the basic inventory above, the host ``mail.example.com`` belongs to the ``all`` and ``ungrouped`` groups. The host ``two.example.com`` belongs to the ``all`` and ``dbservers`` groups. Although ``all`` and ``ungrouped`` are always present, they can be implicit and might not appear in group listings like ``group_names``.

.. _host_multiple_groups:

Hosts in multiple groups
------------------------

You can put a host in more than one group. For example, you can include a production web server in a data center in Atlanta in the ``[prod]``, ``[atlanta]``, and ``[webservers]`` groups. You can create groups that track the following criteria:

* **What** - An application, stack, or microservice (for example, database servers, web servers, and so on).
* **Where** - A datacenter or region, to talk to local DNS, storage, and so on (for example, east, west).
* **When** - The development stage, to avoid testing on production resources (for example, prod, test).

The following example extends the previous YAML inventory to include what, when, and where:

.. code-block:: yaml

  ungrouped:
    hosts:
      mail.example.com:
  webservers:
    hosts:
      foo.example.com:
      bar.example.com:
  dbservers:
    hosts:
      one.example.com:
      two.example.com:
      three.example.com:
  east:
    hosts:
      foo.example.com:
      one.example.com:
      two.example.com:
  west:
    hosts:
      bar.example.com:
      three.example.com:
  prod:
    hosts:
      foo.example.com:
      one.example.com:
      two.example.com:
  test:
    hosts:
      bar.example.com:
      three.example.com:

As the example shows, ``one.example.com`` exists in the ``dbservers``, ``east``, and ``prod`` groups.

.. _child_groups:

Grouping groups: parent/child group relationships
-------------------------------------------------

You can create parent/child relationships among groups. Parent groups are also known as nested groups or groups of groups. For example, if all your production hosts are already in groups such as  ``atlanta_prod`` and ``denver_prod``, you can create a ``production`` group that includes those smaller groups. This approach reduces maintenance because you add or remove hosts from the parent group by editing the child groups.

To create parent/child relationships for groups, use one of the following methods:

* In INI format, use the ``:children`` suffix.
* In YAML format, use the ``children:`` entry.

The following example shows the same inventory as above, simplified with parent groups for the ``prod`` and ``test`` groups:

.. code-block:: yaml

  ungrouped:
    hosts:
      mail.example.com:
  webservers:
    hosts:
      foo.example.com:
      bar.example.com:
  dbservers:
    hosts:
      one.example.com:
      two.example.com:
      three.example.com:
  east:
    hosts:
      foo.example.com:
      one.example.com:
      two.example.com:
  west:
    hosts:
      bar.example.com:
      three.example.com:
  prod:
    children:
      east:
  test:
    children:
      west:

Note the following properties of child groups:

* Any host that is a member of a child group is automatically a member of the parent group.
* A group can have multiple parents and children, but not circular relationships.
* A host can be in multiple groups, but Ansible processes only **one** instance of the host at runtime. Ansible merges the data from multiple groups.
* Hosts and groups are always 'global'. If you define a host or group more than once under different 'branches' or 'instances', the host or group remains the same entity. Defining a host or group more than once either adds new information to it or overwrites any conflicting information with the latest definition.

Adding ranges of hosts
----------------------

Some plugins, like YAML and INI, support adding ranges of hosts. If you have many hosts with a similar pattern, you can add the hosts as a range rather than listing each hostname separately:

In INI:

.. code-block:: text

    [webservers]
    www[01:50].example.com

In YAML:

.. code-block:: yaml

    # ...
      webservers:
        hosts:
          www[01:50].example.com:

You can specify a stride (increments between sequence numbers) when you define a numeric range of hosts:

In INI:

.. code-block:: text

    [webservers]
    www[01:50:2].example.com

In YAML:

.. code-block:: yaml

    # ...
      webservers:
        hosts:
          www[01:50:2].example.com:

The example above matches the subdomains www01, www03, www05, ..., www49, but not www00, www02, www50, and so on, because the stride (increment) is 2 units for each step.

For numeric patterns, you can include or remove leading zeros as desired. Ranges are inclusive. You can also define alphabetic ranges:

.. code-block:: text

    [databases]
    db-[a:f].example.com

.. _using_multiple_inventory_sources:

Passing multiple inventory sources
==================================

You can target multiple inventory sources (static files, directories, dynamic inventory scripts
or anything supported by inventory plugins) at the same time. To do this, specify multiple inventory sources from the command
line (see below) or by configuration, either by setting :envvar:`ANSIBLE_INVENTORY` or in ``ansible.cfg`` (:ref:`DEFAULT_HOST_LIST`).
This capability can be useful when you want to target normally separate environments, like staging and production, at the same time for a specific action.

To target two inventory sources from the command line:

.. code-block:: bash

    ansible-playbook get_logs.yml -i staging -i production


.. _inventory_directory:

Organizing inventory in a directory
===================================

You can consolidate multiple inventory sources in a single directory. The simplest version of this approach is a directory with multiple files instead of a single inventory file. Maintaining a single file becomes difficult when the file gets too long. If you have multiple teams and multiple automation projects, creating one inventory file per team or project lets everyone easily find the hosts and groups that matter to them. You can also still use the files individually or in subsets, depending on how you configure or call Ansible.

These files can use all formats or plugin configurations (for example, YAML or INI). In this case, your directory becomes your 'single' inventory source, and Ansible aggregates the multiple sources it finds in that directory. By default, Ansible ignores some directories and extensions, but you can change this behavior in the configuration (:ref:`INVENTORY_IGNORE_PATTERNS` and :ref:`INVENTORY_IGNORE_EXTS`).

You can also combine multiple inventory source types in an inventory directory. This method can be useful for combining static and dynamic hosts and managing them as one inventory.
The following inventory directory combines an inventory plugin source, a dynamic inventory script,
and a file with static hosts:

.. code-block:: text

    inventory/
      openstack.yml          # configure inventory plugin to get hosts from OpenStack cloud
      dynamic-inventory.py   # add additional hosts with dynamic inventory script
      on-prem                # add static hosts and groups
      parent-groups          # add static hosts and groups

You can target this inventory directory as follows:

.. code-block:: bash

    ansible-playbook example.yml -i inventory

You can also configure the inventory directory in your ``ansible.cfg`` file. See :ref:`intro_configuration` for more details.

Ansible reads and loads files from the top directory down in alphabetically sorted order.

Managing inventory load order
-----------------------------

Ansible loads inventory sources in the order you supply them. It defines hosts, groups, and variables as it encounters them in the source files, adding the ``all`` and ``ungrouped`` groups at the end if needed.

Depending on the inventory plugin or plugins you use, you might need to rearrange the order of sources to ensure that parent/child-defined groups or hosts exist as the plugins expect. Otherwise, you might encounter a parsing error. For example, the YAML and INI inventory plugins discard empty groups (groups with no associated hosts) when they finish processing each source.

If you define a variable multiple times, Ansible overwrites the previous value. The last definition wins.

.. _variables_in_inventory:

Adding variables to inventory
=============================

You can define variables that relate to a specific host or group in your inventory. A simple way to start is by adding variables directly to the hosts and groups in a YAML or INI inventory source.

This guide documents how to add variables in the inventory source for simplicity. However, you can also use :ref:`vars_plugins` to add variables from many other sources. By default, Ansible ships with the :ref:`host_group_vars <host_group_vars_vars>` plugin, which allows you to define variables in separate host and group variable files. Using separate files is a more robust approach to describing your system policy than defining variables in the inventory source. See :ref:`splitting_out_vars` for guidelines on how to store variable values in individual files in the 'host_vars' and 'group_vars' directories. 

.. _host_variables:

Assigning a variable to one machine: host variables
===================================================

You can easily assign a variable to a single host and then use that variable later in playbooks. You can do this directly in your inventory file.

In INI:

.. code-block:: text

   [atlanta]
   host1 http_port=80 maxRequestsPerChild=808
   host2 http_port=303 maxRequestsPerChild=909

In YAML:

.. code-block:: yaml

    atlanta:
      hosts:
        host1:
          http_port: 80
          maxRequestsPerChild: 808
        host2:
          http_port: 303
          maxRequestsPerChild: 909

Unique values like non-standard SSH ports work well as host variables. You can add them to your Ansible inventory by adding the port number after the hostname with a colon:

.. code-block:: text

    badwolf.example.com:5309

You can use host variables to define 'Connection variables'. Connection variables configure ``connection``, ``shell``, and ``become`` plugins to enable task execution on the host. For example:

.. code-block:: text

   [targets]

   localhost              ansible_connection=local
   other1.example.com     ansible_connection=ssh        ansible_user=myuser
   other2.example.com     ansible_connection=ssh        ansible_user=myotheruser


.. _inventory_aliases:

Inventory aliases
-----------------

The ``inventory_hostname`` is the unique identifier for a host in Ansible. This identifier can be an IP address or a hostname, but it can also be just an 'alias' or short name for the host.

In INI:

.. code-block:: text

    jumper ansible_port=5555 ansible_host=192.0.2.50

In YAML:

.. code-block:: yaml

    # ...
      hosts:
        jumper:
          ansible_port: 5555
          ansible_host: 192.0.2.50

In this example, running Ansible against the host alias "jumper" connects to 192.0.2.50 on port 5555. See :ref:`behavioral inventory parameters <behavioral_parameters>` to further customize the connection to hosts.

This feature is also useful for targeting the same host more than once, but remember that tasks can run in parallel:

In INI:

.. code-block:: text

    jumper1 ansible_port=5555 ansible_host=192.0.2.50
    jumper2 ansible_port=5555 ansible_host=192.0.2.50

In YAML:

.. code-block:: yaml

    # ...
      hosts:
        jumper1:
          ansible_port: 5555
          ansible_host: 192.0.2.50
        jumper2:
          ansible_port: 5555
          ansible_host: 192.0.2.50


Defining variables in INI format
================================

Ansible interprets values that you pass in the INI format by using the ``key=value`` syntax differently depending on where you declare them:

* When you declare a value inline with the host, Ansible interprets the INI value as a Python literal structure (for example, a string, number, tuple, list, dict, boolean, or None). Host lines accept multiple ``key=value`` parameters per line. Therefore, you need a way to indicate that a space is part of a value rather than a separator. You can quote values that contain whitespace (using single or double quotes). See the `Python shlex parsing rules`_ for details.

* When you declare a value in a ``:vars`` section, Ansible interprets the INI value as a string. For example, ``var=FALSE`` creates a string with the value 'FALSE'. Unlike host lines, ``:vars`` sections accept only a single entry per line, so everything after the ``=`` becomes the value for the entry.

If you need a variable from an INI inventory to have a certain type (for example, a string or a boolean), always specify the type with a filter in your task. Do not rely on types that you set in INI inventories when you consume variables.

Consider using the YAML format for inventory sources to avoid confusion about the actual type of a variable. The YAML inventory plugin processes variable values consistently and correctly.

.. _Python shlex parsing rules: https://docs.python.org/3/library/shlex.html#parsing-rules

.. _group_variables:

Assigning a variable to many machines: group variables
======================================================

If all hosts in a group share a variable value, you can apply that variable to an entire group at once.

In INI:

.. code-block:: text

   [atlanta]
   host1
   host2

   [atlanta:vars]
   ntp_server=ntp.atlanta.example.com
   proxy=proxy.atlanta.example.com

In YAML:

.. code-block:: yaml

    atlanta:
      hosts:
        host1:
        host2:
      vars:
        ntp_server: ntp.atlanta.example.com
        proxy: proxy.atlanta.example.com

Group variables are a convenient way to apply variables to multiple hosts at once. Before executing, however, Ansible always flattens variables, including inventory variables, to the host level. If a host is a member of multiple groups, Ansible reads variable values from all of those groups. If you assign different values to the same variable in different groups, Ansible chooses which value to use based on internal :ref:`rules for merging <how_we_merge>`.

.. _subgroups:

Inheriting variable values: group variables for groups of groups
----------------------------------------------------------------

You can apply variables to parent groups (nested groups or groups of groups) as well as to child groups. The syntax is the same: ``:vars`` for INI format and ``vars:`` for YAML format:

In INI:

.. code-block:: text

   [atlanta]
   host1
   host2

   [raleigh]
   host2
   host3

   [southeast:children]
   atlanta
   raleigh

   [southeast:vars]
   some_server=foo.southeast.example.com
   halon_system_timeout=30
   self_destruct_countdown=60
   escape_pods=2

   [usa:children]
   southeast
   northeast
   southwest
   northwest

In YAML:

.. code-block:: yaml

  usa:
    children:
      southeast:
        children:
          atlanta:
            hosts:
              host1:
              host2:
          raleigh:
            hosts:
              host2:
              host3:
        vars:
          some_server: foo.southeast.example.com
          halon_system_timeout: 30
          self_destruct_countdown: 60
          escape_pods: 2
      northeast:
      northwest:
      southwest:

A child group's variables have higher precedence (they override) than a parent group's variables.

.. _splitting_out_vars:

Organizing host and group variables
===================================

Although you can define variables in the inventory source, you can also use :ref:`vars_plugins` to define alternate sources for your variables.

The default vars plugin that Ansible ships with, :ref:`host_group_vars <host_group_vars_vars>`, lets you use separate host and group variable files. This method helps you organize your variable values more easily. You can also use lists and hash data in these files, which you cannot do in your main inventory file.

For the ``host_group_vars`` plugin, your host and group variable files must use YAML syntax. Valid file extensions are '.yml', '.yaml', '.json', or no file extension. See :ref:`yaml_syntax` if you are new to YAML.

The ``host_group_vars`` plugin loads host and group variable files by searching paths relative to the inventory source or the playbook file. If your inventory file at ``/etc/ansible/hosts`` contains a host named 'foosball' that belongs to the 'raleigh' and 'webservers' groups, that host will use variables from the YAML files in the following locations:

.. code-block:: bash

    /etc/ansible/group_vars/raleigh # can optionally end in '.yml', '.yaml', or '.json'
    /etc/ansible/group_vars/webservers
    /etc/ansible/host_vars/foosball

For example, if you group hosts in your inventory by datacenter, and each datacenter uses its own NTP server and database server, you can create a file named ``/etc/ansible/group_vars/raleigh`` to store the variables for the ``raleigh`` group:

.. code-block:: yaml

    ---
    ntp_server: acme.example.org
    database_server: storage.example.org

You can also create *directories* named after your groups or hosts. Ansible reads all the files in these directories in lexicographical order. Here is an example with the 'raleigh' group:

.. code-block:: bash

    /etc/ansible/group_vars/raleigh/db_settings
    /etc/ansible/group_vars/raleigh/cluster_settings

All hosts in the 'raleigh' group have the variables that you define in these files
available to them. This method is very useful for keeping your variables organized when a single
file gets too big, or when you want to use :ref:`Ansible Vault <playbooks_vault>` on some group variables.

Ansible's :ref:`host_group_vars <host_group_vars_vars>` vars plugin can also add ``group_vars/`` and ``host_vars/`` directories to your playbook directory when you use ``ansible-playbook``. However, not all Ansible commands have a playbook (for example, ``ansible`` or ``ansible-console``). For those commands, you can use the ``--playbook-dir`` option to provide the directory on the command line.
If you have sources for the vars plugins relative to both the playbook directory and the inventory directory, the variables that Ansible sources relative to the playbook override the variables that it sources relative to the inventory source.

To track changes to your inventory and variable definitions, keep your inventory sources and their relative variable directories and files in a Git repository or other version control system.

.. _how_we_merge:

How variables are merged
========================

.. note:: Ansible merges variables from different sources and applies precedence to some variables over others according to a set of rules. For example, variables that occur higher in an inventory can override variables that occur lower in the inventory. See :ref:`ansible_variable_precedence` for more information.

Before it runs a play, Ansible merges and flattens variables to the specific host. This process keeps Ansible focused on the Host and Task, so groups do not survive outside of inventory and host matching. By default, Ansible overwrites variables, including the ones that you define for a group or host (see :ref:`DEFAULT_HASH_BEHAVIOUR<DEFAULT_HASH_BEHAVIOUR>`). The order/precedence for inventory entities is (from lowest to highest):

The following list shows the order of precedence for inventory entities, from lowest to highest:

- ``all`` group (because it is the 'parent' of all other groups)
- parent group
- child group
- host

By default, Ansible merges groups at the same parent/child level in alphabetical order. Variables from the last group that Ansible loads overwrite variables from the previous groups. For example, Ansible merges an ``a_group`` with a ``b_group``, and matching variables from ``b_group`` overwrite the variables in ``a_group``.

You can fine-tune this merge behavior by setting the group variable ``ansible_group_priority``. This variable overrides the alphabetical sorting for the merge order for groups of the same level (after Ansible resolves the parent/child order). The larger the number, the later Ansible merges the group, giving it higher priority. This variable defaults to ``1`` if you do not set it. For example:

.. code-block:: yaml

    a_group:
      vars:
        testvar: a
        ansible_group_priority: 10
    b_group:
      vars:
        testvar: b

In this example, if both groups have the same priority, the result would normally be ``testvar == b``. However, because we give ``a_group`` a higher priority, the result is ``testvar == a``.

You can set ``ansible_group_priority`` only in an inventory source, not in ``group_vars/``. Ansible uses this variable when it loads the ``group_vars/`` directory.

Managing inventory variable load order
--------------------------------------

This section describes how to control variable precedence by managing the load order of inventory sources. You can pass sources in a specific order at the command line or use prefixes in the filenames of sources within a directory.

When you use multiple inventory sources, remember that Ansible resolves any variable conflicts according to
the rules described in :ref:`how_we_merge` and :ref:`ansible_variable_precedence`. You can control the merging order of variables in inventory sources to get the variable value you need.

When you pass multiple inventory sources at the command line, Ansible merges variables in the order you pass those parameters. If the ``[all:vars]`` section in the staging inventory defines ``myvar = 1`` and the production inventory defines ``myvar = 2``, then the following outcomes are true:

* If you pass ``-i staging -i production``, Ansible runs the playbook with ``myvar = 2``.
* If you pass ``-i production -i staging``, Ansible runs the playbook with ``myvar = 1``.

When you put multiple inventory sources in a directory, Ansible merges the sources in alphabetical order according to their filenames. You can control the load order by adding prefixes to the files:

.. code-block:: text

    inventory/
      01-openstack.yml          # configure inventory plugin to get hosts from Openstack cloud
      02-dynamic-inventory.py   # add additional hosts with dynamic inventory script
      03-static-inventory       # add static hosts
      group_vars/
        all.yml                 # assign variables to all hosts

If ``01-openstack.yml`` defines ``myvar = 1`` for the group ``all``, ``02-dynamic-inventory.py`` defines ``myvar = 2``,
and ``03-static-inventory`` defines ``myvar = 3``, Ansible runs the playbook with ``myvar = 3``.

For more details on inventory plugins and dynamic inventory scripts see :ref:`inventory_plugins` and :ref:`intro_dynamic_inventory`.

.. _behavioral_parameters:

Connecting to hosts: behavioral inventory parameters
====================================================

As described above, you can set the following variables to control how Ansible interacts with remote hosts.

Host connection:

.. include:: shared_snippets/SSH_password_prompt.txt

ansible_connection
    Specifies the connection type to the host. This can be the name of any Ansible connection plugin. SSH protocol types are ``ssh`` or ``paramiko``. The default is ``ssh``.

General for all connections:

ansible_host
    Specifies the resolvable name or IP of the host to connect to, if it is different from the alias you wish to give to it. Never set it to depend on ``inventory_hostname``. If you really need something like that, use ``inventory_hostname_short`` so it can work with delegation.
ansible_port
    The connection port number, if not the default (22 for ssh).
ansible_user
    The username to use when connecting (logging in) to the host.
ansible_password
    The password to use to authenticate to the host. (Never store this variable in plain text. Always use a vault. See :ref:`tip_for_variables_and_vaults`.)


Specific to the SSH connection plugin:

ansible_ssh_private_key_file
    Private key file used by SSH. This is useful if you use multiple keys and you do not want to use SSH agent.
ansible_ssh_common_args
    Ansible always appends this setting to the default command line for :command:`sftp`, :command:`scp`,
    and :command:`ssh`. This is useful for configuring a ``ProxyCommand`` for a certain host or
    group.
ansible_sftp_extra_args
    Ansible always appends this setting to the default :command:`sftp` command line.
ansible_scp_extra_args
    Ansible always appends this setting to the default :command:`scp` command line.
ansible_ssh_extra_args
    Ansible always appends this setting to the default :command:`ssh` command line.
ansible_ssh_pipelining
    Specifies whether to use SSH pipelining. This can override the ``pipelining`` setting in :file:`ansible.cfg`.
ansible_ssh_executable (added in version 2.2)
    This setting overrides the default behavior to use the system :command:`ssh`. It can override the ``ssh_executable`` setting in the ``ssh_connection`` section of :file:`ansible.cfg`.


Privilege escalation (see :ref:`Ansible Privilege Escalation<become>` for further details):

ansible_become
    Equivalent to ``ansible_sudo`` or ``ansible_su``; allows you to force privilege escalation.
ansible_become_method
    Allows you to set the privilege escalation method to a matching become plugin.
ansible_become_user
    Equivalent to ``ansible_sudo_user`` or ``ansible_su_user``; allows you to set the user you become through privilege escalation.
ansible_become_password
    Equivalent to ``ansible_sudo_password`` or ``ansible_su_password``; allows you to set the privilege escalation password. (Never store this variable in plain text. Always use a vault. See :ref:`tip_for_variables_and_vaults`.)
ansible_become_exe
    Equivalent to ``ansible_sudo_exe`` or ``ansible_su_exe``; allows you to set the executable for the escalation method you selected.
ansible_become_flags
    Equivalent to ``ansible_sudo_flags`` or ``ansible_su_flags``; allows you to set the flags passed to the selected escalation method. You can also set this globally in :file:`ansible.cfg` in the ``become_flags`` option under ``privilege_escalation``.

Remote host environment parameters:

.. _ansible_shell_type:

ansible_shell_type
    Specifies the shell type of the target system. You should not use this setting unless you have set the
    :ref:`ansible_shell_executable<ansible_shell_executable>` to a non-Bourne (sh) compatible shell.  By default, Ansible
    formats commands using ``sh``-style syntax.  If you set this to ``csh`` or ``fish``, commands
    that Ansible executes on target systems follow those shell's syntax instead.

.. _ansible_python_interpreter:

ansible_python_interpreter
    Specifies the target host Python path. This is useful for systems with more
    than one Python or for systems where Python is not located at :command:`/usr/bin/python`, such as \*BSD, or where :command:`/usr/bin/python`
    is not a 2.X series Python.  We do not use the :command:`/usr/bin/env` mechanism because that requires the remote user's
    path to be set correctly and also assumes the :program:`python` executable is named python, where the executable might
    be named something like :program:`python2.6`.

ansible_*_interpreter
    Works for any language, such as Ruby or Perl, and works just like :ref:`ansible_python_interpreter<ansible_python_interpreter>`.
    This variable replaces the shebang of modules that will run on that host.

.. versionadded:: 2.1

.. _ansible_shell_executable:

ansible_shell_executable
    This setting sets the shell the Ansible control node will use on the target machine.
    It overrides ``executable`` in :file:`ansible.cfg`, which defaults to
    :command:`/bin/sh`.  You should only change this value if it is not possible
    to use :command:`/bin/sh` (in other words, if :command:`/bin/sh` is not installed on the target
    machine or cannot be run from sudo.).

Examples from an Ansible-INI host file:

.. code-block:: text

  some_host         ansible_port=2222     ansible_user=manager
  aws_host          ansible_ssh_private_key_file=/home/example/.ssh/aws.pem
  freebsd_host      ansible_python_interpreter=/usr/local/bin/python
  ruby_module_host  ansible_ruby_interpreter=/usr/bin/ruby.1.9.3

Non-SSH connection types
------------------------

As stated in the previous section, Ansible executes playbooks over SSH by default, but it is not limited to this connection type.
You can change the connection type with the host-specific parameter ``ansible_connection=<connection plugin name>``.
For a full list of available plugins and examples, see :ref:`connection_plugin_list`.

.. _inventory_setup_examples:

Inventory setup examples
========================

See also :ref:`sample_setup`, which shows inventory along with playbooks and other Ansible artifacts.

.. _inventory_setup-per_environment:

Example: One inventory per environment
--------------------------------------

If you need to manage multiple environments, consider defining only the
hosts of a single environment in each inventory. This
way, it is harder to, for example, accidentally change the state of
nodes inside the "test" environment when you wanted to update
some "staging" servers.

For the example mentioned above, you could have an
:file:`inventory_test` file:

.. code-block:: ini

  [dbservers]
  db01.test.example.com
  db02.test.example.com

  [appservers]
  app01.test.example.com
  app02.test.example.com
  app03.test.example.com

That file only includes hosts that are part of the "test"
environment. You can define the "staging" machines in another file
called :file:`inventory_staging`:

.. code-block:: ini

  [dbservers]
  db01.staging.example.com
  db02.staging.example.com

  [appservers]
  app01.staging.example.com
  app02.staging.example.com
  app03.staging.example.com

To apply a playbook called :file:`site.yml`
to all the app servers in the test environment, use the
following command:

.. code-block:: bash

  ansible-playbook -i inventory_test -l appservers site.yml

.. _inventory_setup-per_function:

Example: Group by function
--------------------------

In the previous section, you already saw an example of using groups to
cluster hosts that have the same function. This approach allows you,
for example, to define firewall rules inside a playbook or role
that affect only database servers:

.. code-block:: yaml

  - hosts: dbservers
    tasks:
    - name: Allow access from 10.0.0.1
      ansible.builtin.iptables:
        chain: INPUT
        jump: ACCEPT
        source: 10.0.0.1

.. _inventory_setup-per_location:

Example: Group by location
--------------------------

Other tasks might focus on where a certain host is located. Let's
say that ``db01.test.example.com`` and ``app01.test.example.com`` are
located in DC1, while ``db02.test.example.com`` is in DC2:

.. code-block:: ini

  [dc1]
  db01.test.example.com
  app01.test.example.com

  [dc2]
  db02.test.example.com

In practice, you might end up mixing all these setups. For example, you
might need to update all nodes in a specific data center
on one day, while on another day, you might need to update all the application servers no matter
their location.

.. seealso::

   :ref:`inventory_plugins`
       Pulling inventory from dynamic or static sources
   :ref:`intro_dynamic_inventory`
       Pulling inventory from dynamic sources, such as cloud providers
   :ref:`intro_adhoc`
       Examples of basic commands
   :ref:`working_with_playbooks`
       Learning Ansible's configuration, deployment, and orchestration language.
   :ref:`Communication<communication>`
       Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide
