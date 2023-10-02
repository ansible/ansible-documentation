.. _intro_inventory:
.. _inventory:

***************************
How to build your inventory
***************************

Ansible automates tasks on managed nodes or "hosts" in your infrastructure, using a list or group of lists known as inventory. You can pass host names at the command line, but most Ansible users create inventory files. Your inventory defines the managed nodes you automate, with groups so you can run automation tasks on multiple hosts at the same time.
Once your inventory is defined, you use :ref:`patterns <intro_patterns>` to select the hosts or groups you want Ansible to run against.

The simplest inventory is a single file with a list of hosts and groups. The default location for this file is ``/etc/ansible/hosts``.
You can specify a different inventory file at the command line using the ``-i <path>`` option or in configuration using ``inventory``.

Ansible :ref:`inventory_plugins` support a range of formats and sources to make your inventory flexible and customizable. As your inventory expands, you may need more than a single file to organize your hosts and groups. Here are three options beyond the ``/etc/ansible/hosts`` file:

- You can create a directory with multiple inventory files. See :ref:`inventory_directory`. These can use different formats (YAML, ini, and so on).
- You can pull inventory dynamically. For example, you can use a dynamic inventory plugin to list resources in one or more cloud providers. See :ref:`intro_dynamic_inventory`.
- You can use multiple sources for inventory, including both dynamic inventory and static files. See :ref:`using_multiple_inventory_sources`.

.. contents::
   :local:

.. _inventoryformat:

Inventory basics: formats, hosts, and groups
============================================

You can create your inventory file in one of many formats, depending on the inventory plugins you have.
The most common formats are INI and YAML. A basic INI ``/etc/ansible/hosts`` might look like this:

.. code-block:: text

    mail.example.com

    [webservers]
    foo.example.com
    bar.example.com

    [dbservers]
    one.example.com
    two.example.com
    three.example.com

The headings in brackets are group names, which are used in classifying hosts
and deciding what hosts you are controlling at what times and for what purpose.
Group names should follow the same guidelines as :ref:`valid_variable_names`.

Here's that same basic inventory file in YAML format:

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

Even if you do not define any groups in your inventory file, Ansible creates two default groups: ``all`` and ``ungrouped``. The ``all`` group contains every host.
The ``ungrouped`` group contains all hosts that don't have another group aside from ``all``.
Every host will always belong to at least 2 groups (``all`` and ``ungrouped`` or ``all`` and some other group). For example, in the basic inventory above, the host ``mail.example.com`` belongs to the ``all`` group and the ``ungrouped`` group; the host ``two.example.com`` belongs to the ``all`` group and the ``dbservers`` group. Though ``all`` and ``ungrouped`` are always present, they can be implicit and not appear in group listings like ``group_names``.

.. _host_multiple_groups:

Hosts in multiple groups
------------------------

You can (and probably will) put each host in more than one group. For example a production webserver in a datacenter in Atlanta might be included in groups called ``[prod]`` and ``[atlanta]`` and ``[webservers]``. You can create groups that track:

* What - An application, stack or microservice (for example, database servers, web servers, and so on).
* Where - A datacenter or region, to talk to local DNS, storage, and so on (for example, east, west).
* When - The development stage, to avoid testing on production resources (for example, prod, test).

Extending the previous YAML inventory to include what, when, and where would look like this:

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

You can see that ``one.example.com`` exists in the ``dbservers``, ``east``, and ``prod`` groups.

.. _child_groups:

Grouping groups: parent/child group relationships
-------------------------------------------------

You can create parent/child relationships among groups. Parent groups are also known as nested groups or groups of groups. For example, if all your production hosts are already in groups such as  ``atlanta_prod`` and ``denver_prod``, you can create a ``production`` group that includes those smaller groups. This approach reduces maintenance because you can add or remove hosts from the parent group by editing the child groups.

To create parent/child relationships for groups:

* in INI format, use the ``:children`` suffix
* in YAML format, use the ``children:`` entry

Here is the same inventory as shown above, simplified with parent groups for the ``prod`` and ``test`` groups. The two inventory files give you the same results:

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

Child groups have a couple of properties to note:

* Any host that is member of a child group is automatically a member of the parent group.
* Groups can have multiple parents and children, but not circular relationships.
* Hosts can also be in multiple groups, but there will only be **one** instance of a host at runtime. Ansible merges the data from the multiple groups.

Adding ranges of hosts
----------------------

If you have a lot of hosts with a similar pattern, you can add them as a range rather than listing each hostname separately:

In INI:

.. code-block:: text

    [webservers]
    www[01:50].example.com

In YAML:

.. code-block:: yaml

    ...
      webservers:
        hosts:
          www[01:50].example.com:

You can specify a stride (increments between sequence numbers) when defining a numeric range of hosts:

In INI:

.. code-block:: text

    [webservers]
    www[01:50:2].example.com

In YAML:

.. code-block:: yaml

    ...
      webservers:
        hosts:
          www[01:50:2].example.com:

The example above would make the subdomains www01, www03, www05, ..., www49 match, but not www00, www02, www50 and so on, because the stride (increment) is 2 units each step.

For numeric patterns, leading zeros can be included or removed, as desired. Ranges are inclusive. You can also define alphabetic ranges:

.. code-block:: text

    [databases]
    db-[a:f].example.com

.. _using_multiple_inventory_sources:

Passing multiple inventory sources
==================================

You can target multiple inventory sources (directories, dynamic inventory scripts
or files supported by inventory plugins) at the same time by giving multiple inventory parameters from the command
line or by configuring :envvar:`ANSIBLE_INVENTORY`. This can be useful when you want to target normally
separate environments, like staging and production, at the same time for a specific action.

To target two inventory sources from the command line:

.. code-block:: bash

    ansible-playbook get_logs.yml -i staging -i production

.. _inventory_directory:

Organizing inventory in a directory
===================================

You can consolidate multiple inventory sources in a single directory. The simplest version of this is a directory with multiple files instead of a single inventory file. A single file gets difficult to maintain when it gets too long. If you have multiple teams and multiple automation projects, having one inventory file per team or project lets everyone easily find the hosts and groups that matter to them.

You can also combine multiple inventory source types in an inventory directory. This can be useful for combining static and dynamic hosts and managing them as one inventory.
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

Managing inventory load order
-----------------------------

Ansible loads inventory sources in ASCII order according to the filenames. If you define parent groups in one file or directory and child groups in other files or directories, the files that define the child groups must be loaded first. If the parent groups are loaded first, you will see the error ``Unable to parse /path/to/source_of_parent_groups as an inventory source``.

For example, if you have a file called ``groups-of-groups`` that defines a ``production`` group with child groups defined in a file called ``on-prem``, Ansible cannot parse the ``production`` group. To avoid this problem, you can control the load order by adding prefixes to the files:

.. code-block:: text

    inventory/
      01-openstack.yml          # configure inventory plugin to get hosts from OpenStack cloud
      02-dynamic-inventory.py   # add additional hosts with dynamic inventory script
      03-on-prem                # add static hosts and groups
      04-groups-of-groups       # add parent groups

You can find examples of how to organize your inventories and group your hosts in :ref:`inventory_setup_examples`.

.. _variables_in_inventory:

Adding variables to inventory
=============================

You can store variable values that relate to a specific host or group in inventory. To start with, you may add variables directly to the hosts and groups in your main inventory file.

We document adding variables in the main inventory file for simplicity. However, storing variables in separate host and group variable files is a more robust approach to describing your system policy. Setting variables in the main inventory file is only a shorthand. See :ref:`splitting_out_vars` for guidelines on storing variable values in individual files in the 'host_vars' directory. See :ref:`splitting_out_vars` for details.

.. _host_variables:

Assigning a variable to one machine: host variables
===================================================

You can easily assign a variable to a single host, then use it later in playbooks. You can do this directly in your inventory file.

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

Connection variables also work well as host variables:

.. code-block:: text

   [targets]

   localhost              ansible_connection=local
   other1.example.com     ansible_connection=ssh        ansible_user=myuser
   other2.example.com     ansible_connection=ssh        ansible_user=myotheruser

.. note:: If you list non-standard SSH ports in your SSH config file, the ``openssh`` connection will find and use them, but the ``paramiko`` connection will not.

.. _inventory_aliases:

Inventory aliases
-----------------

You can also define aliases in your inventory using host variables:

In INI:

.. code-block:: text

    jumper ansible_port=5555 ansible_host=192.0.2.50

In YAML:

.. code-block:: yaml

    ...
      hosts:
        jumper:
          ansible_port: 5555
          ansible_host: 192.0.2.50

In this example, running Ansible against the host alias "jumper" will connect to 192.0.2.50 on port 5555. See :ref:`behavioral inventory parameters <behavioral_parameters>` to further customize the connection to hosts.

Defining variables in INI format
================================

Values passed in the INI format using the ``key=value`` syntax are interpreted differently depending on where they are declared:

* When declared inline with the host, INI values are interpreted as Python literal structures           (strings, numbers, tuples, lists, dicts, booleans, None). Host lines accept multiple ``key=value`` parameters per line. Therefore they need a way to indicate that a space is part of a value rather than a separator. Values that contain whitespace can be quoted (single or double). See the `Python shlex parsing rules`_ for details.
   
* When declared in a ``:vars`` section, INI values are interpreted as strings. For example ``var=FALSE`` would create a string equal to 'FALSE'. Unlike host lines, ``:vars`` sections accept only a single entry per line, so everything after the ``=`` must be the value for the entry.

If a variable value set in an INI inventory must be a certain type (for example, a string or a boolean value), always specify the type with a filter in your task. Do not rely on types set in INI inventories when consuming variables.

Consider using YAML format for inventory sources to avoid confusion on the actual type of a variable. The YAML inventory plugin processes variable values consistently and correctly.

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

A child group's variables will have higher precedence (override) a parent group's variables.

.. _splitting_out_vars:

Organizing host and group variables
===================================

Although you can store variables in the main inventory file, storing separate host and group variables files may help you organize your variable values more easily. You can also use lists and hash data in host and group variables files, which you cannot do in your main inventory file.

Host and group variable files must use YAML syntax. Valid file extensions include '.yml', '.yaml', '.json', or no file extension. See :ref:`yaml_syntax` if you are new to YAML.

Ansible loads host and group variable files by searching paths relative to the inventory file or the playbook file. If your inventory file at ``/etc/ansible/hosts`` contains a host named 'foosball' that belongs to two groups, 'raleigh' and 'webservers', that host will use variables in YAML files at the following locations:

.. code-block:: bash

    /etc/ansible/group_vars/raleigh # can optionally end in '.yml', '.yaml', or '.json'
    /etc/ansible/group_vars/webservers
    /etc/ansible/host_vars/foosball

For example, if you group hosts in your inventory by datacenter, and each datacenter uses its own NTP server and database server, you can create a file called ``/etc/ansible/group_vars/raleigh`` to store the variables for the ``raleigh`` group:

.. code-block:: yaml

    ---
    ntp_server: acme.example.org
    database_server: storage.example.org

You can also create *directories* named after your groups or hosts. Ansible will read all the files in these directories in lexicographical order. An example with the 'raleigh' group:

.. code-block:: bash

    /etc/ansible/group_vars/raleigh/db_settings
    /etc/ansible/group_vars/raleigh/cluster_settings

All hosts in the 'raleigh' group will have the variables defined in these files
available to them. This can be very useful to keep your variables organized when a single
file gets too big, or when you want to use :ref:`Ansible Vault<playbooks_vault>` on some group variables.

For ``ansible-playbook`` you can also add ``group_vars/`` and ``host_vars/`` directories to your playbook directory. Other Ansible commands (for example, ``ansible``, ``ansible-console``, and so on) will only look for ``group_vars/`` and ``host_vars/`` in the inventory directory. If you want other commands to load group and host variables from a playbook directory, you must provide the ``--playbook-dir`` option on the command line.
If you load inventory files from both the playbook directory and the inventory directory, variables in the playbook directory will override variables set in the inventory directory.

Keeping your inventory file and variables in a git repo (or other version control)
is an excellent way to track changes to your inventory and host variables.

.. _how_we_merge:

How variables are merged
========================

By default variables are merged/flattened to the specific host before a play is run. This keeps Ansible focused on the Host and Task, so groups don't really survive outside of inventory and host matching. By default, Ansible overwrites variables including the ones defined for a group and/or host (see :ref:`DEFAULT_HASH_BEHAVIOUR<DEFAULT_HASH_BEHAVIOUR>`). The order/precedence is (from lowest to highest):

- all group (because it is the 'parent' of all other groups)
- parent group
- child group
- host

By default Ansible merges groups at the same parent/child level in ASCII order, and variables from the last group loaded overwrite variables from the previous groups. For example, an a_group will be merged with b_group and b_group vars that match will overwrite the ones in a_group.

You can change this behavior by setting the group variable ``ansible_group_priority`` to change the merge order for groups of the same level (after the parent/child order is resolved). The larger the number, the later it will be merged, giving it higher priority. This variable defaults to ``1`` if not set. For example:

.. code-block:: yaml

    a_group:
      vars:
        testvar: a
        ansible_group_priority: 10
    b_group:
      vars:
        testvar: b

In this example, if both groups have the same priority, the result would normally have been ``testvar == b``, but since we are giving the ``a_group`` a higher priority the result will be ``testvar == a``.

.. note:: ``ansible_group_priority`` can only be set in the inventory source and not in group_vars/, as the variable is used in the loading of group_vars.

Managing inventory variable load order
--------------------------------------

When using multiple inventory sources, keep in mind that any variable conflicts are resolved according
to the rules described in :ref:`how_we_merge` and :ref:`ansible_variable_precedence`. You can control the merging order of variables in inventory sources to get the variable value you need.

When you pass multiple inventory sources at the command line, Ansible merges variables in the order you pass those parameters. If ``[all:vars]`` in staging inventory defines ``myvar = 1`` and production inventory defines ``myvar = 2``, then:

* Pass  ``-i staging -i production`` to run the playbook with ``myvar = 2``.
* Pass ``-i production -i staging`` to run the playbook with ``myvar = 1``. 

When you put multiple inventory sources in a directory, Ansible merges them in ASCII order according to the filenames. You can control the load order by adding prefixes to the files:

.. code-block:: text

    inventory/
      01-openstack.yml          # configure inventory plugin to get hosts from Openstack cloud
      02-dynamic-inventory.py   # add additional hosts with dynamic inventory script
      03-static-inventory       # add static hosts
      group_vars/
        all.yml                 # assign variables to all hosts

If ``01-openstack.yml`` defines ``myvar = 1`` for the group ``all``, ``02-dynamic-inventory.py`` defines ``myvar = 2``,
and ``03-static-inventory`` defines ``myvar = 3``, the playbook will be run with ``myvar = 3``.

For more details on inventory plugins and dynamic inventory scripts see :ref:`inventory_plugins` and :ref:`intro_dynamic_inventory`.

.. _behavioral_parameters:

Connecting to hosts: behavioral inventory parameters
====================================================

As described above, setting the following variables control how Ansible interacts with remote hosts.

Host connection:

.. include:: shared_snippets/SSH_password_prompt.txt

ansible_connection
    Connection type to the host. This can be the name of any of ansible's connection plugins. SSH protocol types are ``smart``, ``ssh`` or ``paramiko``.  The default is smart. Non-SSH based types are described in the next section.

General for all connections:

ansible_host
    The name of the host to connect to, if different from the alias you wish to give to it.
ansible_port
    The connection port number, if not the default (22 for ssh)
ansible_user
    The user name to use when connecting to the host
ansible_password
    The password to use to authenticate to the host (never store this variable in plain text; always use a vault. See :ref:`tip_for_variables_and_vaults`)


Specific to the SSH connection:

ansible_ssh_private_key_file
    Private key file used by ssh.  Useful if using multiple keys and you don't want to use SSH agent.
ansible_ssh_common_args
    This setting is always appended to the default command line for :command:`sftp`, :command:`scp`,
    and :command:`ssh`. Useful to configure a ``ProxyCommand`` for a certain host (or
    group).
ansible_sftp_extra_args
    This setting is always appended to the default :command:`sftp` command line.
ansible_scp_extra_args
    This setting is always appended to the default :command:`scp` command line.
ansible_ssh_extra_args
    This setting is always appended to the default :command:`ssh` command line.
ansible_ssh_pipelining
    Determines whether or not to use SSH pipelining. This can override the ``pipelining`` setting in :file:`ansible.cfg`.
ansible_ssh_executable (added in version 2.2)
    This setting overrides the default behavior to use the system :command:`ssh`. This can override the ``ssh_executable`` setting in :file:`ansible.cfg`.


Privilege escalation (see :ref:`Ansible Privilege Escalation<become>` for further details):

ansible_become
    Equivalent to ``ansible_sudo`` or ``ansible_su``, allows to force privilege escalation
ansible_become_method
    Allows to set privilege escalation method
ansible_become_user
    Equivalent to ``ansible_sudo_user`` or ``ansible_su_user``, allows to set the user you become through privilege escalation
ansible_become_password
    Equivalent to ``ansible_sudo_password`` or ``ansible_su_password``, allows you to set the privilege escalation password (never store this variable in plain text; always use a vault. See :ref:`tip_for_variables_and_vaults`)
ansible_become_exe
    Equivalent to ``ansible_sudo_exe`` or ``ansible_su_exe``, allows you to set the executable for the escalation method selected
ansible_become_flags
    Equivalent to ``ansible_sudo_flags`` or ``ansible_su_flags``, allows you to set the flags passed to the selected escalation method. This can be also set globally in :file:`ansible.cfg` in the ``sudo_flags`` option

Remote host environment parameters:

.. _ansible_shell_type:

ansible_shell_type
    The shell type of the target system. You should not use this setting unless you have set the
    :ref:`ansible_shell_executable<ansible_shell_executable>` to a non-Bourne (sh) compatible shell.  By default commands are
    formatted using ``sh``-style syntax.  Setting this to ``csh`` or ``fish`` will cause commands
    executed on target systems to follow those shell's syntax instead.

.. _ansible_python_interpreter:

ansible_python_interpreter
    The target host python path. This is useful for systems with more
    than one Python or not located at :command:`/usr/bin/python` such as \*BSD, or where :command:`/usr/bin/python`
    is not a 2.X series Python.  We do not use the :command:`/usr/bin/env` mechanism as that requires the remote user's
    path to be set right and also assumes the :program:`python` executable is named python, where the executable might
    be named something like :program:`python2.6`.

ansible_*_interpreter
    Works for anything such as ruby or perl and works just like :ref:`ansible_python_interpreter<ansible_python_interpreter>`.
    This replaces shebang of modules which will run on that host.

.. versionadded:: 2.1

.. _ansible_shell_executable:

ansible_shell_executable
    This sets the shell the ansible controller will use on the target machine,
    overrides ``executable`` in :file:`ansible.cfg` which defaults to
    :command:`/bin/sh`.  You should really only change it if is not possible
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

As stated in the previous section, Ansible executes playbooks over SSH but it is not limited to this connection type.
With the host specific parameter ``ansible_connection=<connector>``, the connection type can be changed.
The following non-SSH based connectors are available:

**local**

This connector can be used to deploy the playbook to the control machine itself.

**docker**

This connector deploys the playbook directly into Docker containers using the local Docker client. The following parameters are processed by this connector:

ansible_host
    The name of the Docker container to connect to.
ansible_user
    The user name to operate within the container. The user must exist inside the container.
ansible_become
    If set to ``true`` the ``become_user`` will be used to operate within the container.
ansible_docker_extra_args
    Could be a string with any additional arguments understood by Docker, which are not command specific. This parameter is mainly used to configure a remote Docker daemon to use.

Here is an example of how to instantly deploy to created containers:

.. code-block:: yaml

   - name: Create a jenkins container
     community.general.docker_container:
       docker_host: myserver.net:4243
       name: my_jenkins
       image: jenkins

   - name: Add the container to inventory
     ansible.builtin.add_host:
       name: my_jenkins
       ansible_connection: docker
       ansible_docker_extra_args: "--tlsverify --tlscacert=/path/to/ca.pem --tlscert=/path/to/client-cert.pem --tlskey=/path/to/client-key.pem -H=tcp://myserver.net:4243"
       ansible_user: jenkins
     changed_when: false

   - name: Create a directory for ssh keys
     delegate_to: my_jenkins
     ansible.builtin.file:
       path: "/var/jenkins_home/.ssh/jupiter"
       state: directory

For a full list with available plugins and examples, see :ref:`connection_plugin_list`.

.. note:: If you're reading the docs from the beginning, this may be the first example you've seen of an Ansible playbook. This is not an inventory file.
          Playbooks will be covered in great detail later in the docs.

.. _inventory_setup_examples:

Inventory setup examples
========================

See also :ref:`sample_setup`, which shows inventory along with playbooks and other Ansible artifacts.

.. _inventory_setup-per_environment:

Example: One inventory per environment
--------------------------------------

If you need to manage multiple environments it's sometimes prudent to
have only hosts of a single environment defined per inventory. This
way, it is harder to, for example, accidentally change the state of
nodes inside the "test" environment when you actually wanted to update
some "staging" servers.

For the example mentioned above you could have an
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
environment. Define the "staging" machines in another file
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

In the previous section you already saw an example for using groups in
order to cluster hosts that have the same function. This allows you,
for example, to define firewall rules inside a playbook or role
affecting only database servers:

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

Other tasks might be focused on where a certain host is located. Let's
say that ``db01.test.example.com`` and ``app01.test.example.com`` are
located in DC1 while ``db02.test.example.com`` is in DC2:

.. code-block:: ini

  [dc1]
  db01.test.example.com
  app01.test.example.com

  [dc2]
  db02.test.example.com

In practice, you might even end up mixing all these setups as you
might need to, on one day, update all nodes in a specific data center
while, on another day, update all the application servers no matter
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
   `Mailing List <https://groups.google.com/group/ansible-project>`_
       Questions? Help? Ideas?  Stop by the list on Google Groups
   :ref:`communication_irc`
       How to join Ansible chat channels
