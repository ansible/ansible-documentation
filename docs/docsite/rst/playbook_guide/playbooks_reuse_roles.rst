.. _playbooks_reuse_roles:

*****
Roles
*****

Roles let you automatically load related vars, files, tasks, handlers, and other Ansible artifacts based on a known file structure. After you group your content into roles, you can easily reuse them and share them with other users.

.. contents::
   :local:

.. _role_directory_structure:

Role directory structure
========================

An Ansible role has a defined directory structure with seven main standard directories. You must include at least one of these directories in each role. You can omit any directories the role does not use. For example:

.. code-block:: text

    # playbooks
    site.yml
    webservers.yml
    fooservers.yml
.. include:: shared_snippets/role_directory.txt


By default, Ansible will look in most role directories for a ``main.yml`` file for relevant content (also ``main.yaml`` and ``main``):

- ``tasks/main.yml`` - A list of tasks that the role provides to the play for execution.
- ``handlers/main.yml`` - handlers that are imported into the parent play for use by the role or other roles and tasks in the play.
- ``defaults/main.yml`` - very low precedence values for variables provided by the role (see :ref:`playbooks_variables` for more information). A role's own defaults will take priority over other role's defaults, but any/all other variable sources will override this.
- ``vars/main.yml`` - high precedence variables provided by the role to the play (see :ref:`playbooks_variables` for more information).
- ``files/stuff.txt`` - one or more files that are available for the role and it's children.
- ``templates/something.j2`` - templates to use in the role or child roles.
- ``meta/main.yml`` - metadata for the role, including role dependencies and optional Galaxy metadata such as platforms supported. This is required for uploading into galaxy as a standalone role, but not for using the role in your play.

.. note::
   - None of the files above are required for a role. For example, you can just provide ``files/something.txt`` or ``vars/for_import.yml`` and it will still be a valid role.
   - On stand alone roles you can also include custom modules and/or plugins, for example ``library/my_module.py``, which may be used within this role (see :ref:`embedding_modules_and_plugins_in_roles` for more information).
   - A 'stand alone' role refers to role that is not part of a collection but as individually installable content.
   - Variables from ``vars/`` and ``defaults/`` are imported into play scope unless you disable it via the ``public`` option in ``import_role``/``include_role``.
   
You can add other YAML files in some directories, but they won't be used by default. They can be included/imported directly or specified when using ``include_role/import_role``.
For example, you can place platform-specific tasks in separate files and refer to them in the ``tasks/main.yml`` file:

.. code-block:: yaml

    # roles/example/tasks/main.yml
    - name: Install the correct web server for RHEL
      import_tasks: redhat.yml
      when: ansible_facts['os_family']|lower == 'redhat'

    - name: Install the correct web server for Debian
      import_tasks: debian.yml
      when: ansible_facts['os_family']|lower == 'debian'

    # roles/example/tasks/redhat.yml
    - name: Install web server
      ansible.builtin.yum:
        name: "httpd"
        state: present

    # roles/example/tasks/debian.yml
    - name: Install web server
      ansible.builtin.apt:
        name: "apache2"
        state: present


Or call those tasks directly when loading the role, which bypasses the ``main.yml`` files:

.. code-block:: yaml

   - name: include apt tasks
     include_role:
         name: package_manager_bootstrap
         tasks_from: apt.yml
     when: ansible_facts['os_family'] == 'Debian'


Directories ``defaults`` and ``vars`` may also include *nested directories*. If your variables file is a directory, Ansible reads all variables files and directories inside in alphabetical order. If a nested directory contains variables files as well as directories, Ansible reads the directories first. Below is an example of a ``vars/main`` directory:

.. code-block:: text

  roles/
      common/          # this hierarchy represents a "role"
          vars/
              main/    #  <-- variables associated with this role
                  first_nested_directory/
                      first_variables_file.yml
                  second_nested_directory/
                      second_variables_file.yml
                  third_variables_file.yml

.. _role_search_path:

Storing and finding roles
=========================

By default, Ansible looks for roles in the following locations:

- in collections, if you are using them
- in a directory called ``roles/``, relative to the playbook file
- in the configured :ref:`roles_path <DEFAULT_ROLES_PATH>`. The default search path is ``~/.ansible/roles:/usr/share/ansible/roles:/etc/ansible/roles``.
- in the directory where the playbook file is located

If you store your roles in a different location, set the :ref:`roles_path <DEFAULT_ROLES_PATH>` configuration option so Ansible can find your roles. Checking shared roles into a single location makes them easier to use in multiple playbooks. See :ref:`intro_configuration` for details about managing settings in ``ansible.cfg``.

Alternatively, you can call a role with a fully qualified path:

.. code-block:: yaml

    ---
    - hosts: webservers
      roles:
        - role: '/path/to/my/roles/common'

Using roles
===========

You can use roles in the following ways:

- at the play level with the ``roles`` option: This is the classic way of using roles in a play.
- at the tasks level with ``include_role``: You can reuse roles dynamically anywhere in the ``tasks`` section of a play using ``include_role``.
- at the tasks level with ``import_role``: You can reuse roles statically anywhere in the ``tasks`` section of a play using ``import_role``.
- as a dependency of another role (see the ``dependencies`` keyword in ``meta/main.yml`` in this same page).

.. _roles_keyword:

Using roles at the play level
-----------------------------

The classic (original) way to use roles is with the ``roles`` option for a given play:

.. code-block:: yaml

    ---
    - hosts: webservers
      roles:
        - common
        - webservers

When you use the ``roles`` option at the play level, each role 'x' looks for a ``main.yml`` (also ``main.yaml`` and ``main``) in the following directories:

- ``roles/x/tasks/``
- ``roles/x/handlers/``
- ``roles/x/vars/``
- ``roles/x/defaults/``
- ``roles/x/meta/``
- Any copy, script, template or include tasks (in the role) can reference files in roles/x/{files,templates,tasks}/ (dir depends on task) without having to path them relatively or absolutely.

.. note::
    ``vars`` and ``defaults`` can also match to a directory of the same name and Ansible will process all the files contained in that directory. See :ref:`Role directory structure <role_directory_structure>` for more details.

.. note::
    If you use ``include_role/import_role``, you can specify a custom file name instead of ``main``. The ``meta`` directory is an exception because it does not allow for customization.

When you use the ``roles`` option at the play level, Ansible treats the roles as static imports and processes them during playbook parsing. Ansible executes each play in this order:

- Any ``pre_tasks`` defined in the play.
- Any handlers triggered by pre_tasks.
- Each role listed in ``roles:``, in the order listed. Any role dependencies defined in the role's ``meta/main.yml`` run first, subject to tag filtering and conditionals. See :ref:`role_dependencies` for more details.
- Any ``tasks`` defined in the play.
- Any handlers triggered by the roles or tasks.
- Any ``post_tasks`` defined in the play.
- Any handlers triggered by post_tasks.

.. note::
   If using tags with tasks in a role, be sure to also tag your pre_tasks, post_tasks, and role dependencies and pass those along as well, especially if the pre/post tasks and role dependencies are used for monitoring outage window control or load balancing. See :ref:`tags` for details on adding and using tags.

You can pass other keywords to the ``roles`` option:

.. code-block:: yaml

    ---
    - hosts: webservers
      roles:
        - common
        - role: foo_app_instance
          vars:
            dir: '/opt/a'
            app_port: 5000
          tags: typeA
        - role: foo_app_instance
          vars:
            dir: '/opt/b'
            app_port: 5001
          tags: typeB

When you add a tag to the ``role`` option, Ansible applies the tag to ALL tasks within the role.

.. note::

   Prior to ``ansible-core`` 2.15, ``vars:`` within the ``roles:`` section of a playbook are added to the play variables, making them available to all tasks within the play before and after the role. This behavior can be changed by :ref:`DEFAULT_PRIVATE_ROLE_VARS`. On more recent versions, ``vars:`` do not leak into the play's variable scope.

Including roles: dynamic reuse
------------------------------

You can reuse roles dynamically anywhere in the ``tasks`` section of a play using ``include_role``. While roles added in a ``roles`` section run before any other tasks in a play, included roles run in the order they are defined. If there are other tasks before an ``include_role`` task, the other tasks will run first.

To include a role:

.. code-block:: yaml

    ---
    - hosts: webservers
      tasks:
        - name: Print a message
          ansible.builtin.debug:
            msg: "this task runs before the example role"

        - name: Include the example role
          include_role:
            name: example

        - name: Print a message
          ansible.builtin.debug:
            msg: "this task runs after the example role"

You can pass other keywords, including variables and tags, when including roles:

.. code-block:: yaml

    ---
    - hosts: webservers
      tasks:
        - name: Include the foo_app_instance role
          include_role:
            name: foo_app_instance
          vars:
            dir: '/opt/a'
            app_port: 5000
          tags: typeA
      # ...

When you add a :ref:`tag <tags>` to an ``include_role`` task, Ansible applies the tag **only** to the include itself. This means you can pass ``--tags`` to run only selected tasks from the role, if those tasks themselves have the same tag as the include statement. See :ref:`selective_reuse` for details.

You can conditionally include a role:

.. code-block:: yaml

    ---
    - hosts: webservers
      tasks:
        - name: Include the some_role role
          include_role:
            name: some_role
          when: "ansible_facts['os_family'] == 'RedHat'"

Importing roles: static reuse
-----------------------------

You can reuse roles statically anywhere in the ``tasks`` section of a play using ``import_role``. The behavior is the same as using the ``roles`` keyword. For example:

.. code-block:: yaml

    ---
    - hosts: webservers
      tasks:
        - name: Print a message
          ansible.builtin.debug:
            msg: "before we run our role"

        - name: Import the example role
          import_role:
            name: example

        - name: Print a message
          ansible.builtin.debug:
            msg: "after we ran our role"

You can pass other keywords, including variables and tags when importing roles:

.. code-block:: yaml

    ---
    - hosts: webservers
      tasks:
        - name: Import the foo_app_instance role
          import_role:
            name: foo_app_instance
          vars:
            dir: '/opt/a'
            app_port: 5000
      # ...

When you add a tag to an ``import_role`` statement, Ansible applies the tag to **all** tasks within the role. See :ref:`tag_inheritance` for details.

.. _role_argument_spec:

Role argument validation
========================

Beginning with version 2.11, you may choose to enable role argument validation based on an argument
specification. This specification is defined in the ``meta/argument_specs.yml`` file (or with the ``.yaml``
file extension). When this argument specification is defined, a new task is inserted at the beginning of role execution
that will validate the parameters supplied for the role against the specification. If the parameters fail
validation, the role will fail execution.

.. note::

    Ansible also supports role specifications defined in the role ``meta/main.yml`` file, as well. However,
    any role that defines the specs within this file will not work on versions below 2.11. For this reason,
    we recommend using the ``meta/argument_specs.yml`` file to maintain backward compatibility.

.. note::

    When role argument validation is used on a role that has defined :ref:`dependencies <role_dependencies>`,
    then validation on those dependencies will run before the dependent role, even if argument validation fails
    for the dependent role.

.. note::

    Ansible tags the inserted role argument validation task with :ref:`always <special_tags>`.
    If the role is :ref:`statically imported <dynamic_vs_static>` this task runs unless you use the ``--skip-tags`` flag.

Specification format
--------------------

The role argument specification must be defined in a top-level ``argument_specs`` block within the
role ``meta/argument_specs.yml`` file. All fields are lowercase.

:entry-point-name:

    * The name of the role entry point.
    * This should be ``main`` in the case of an unspecified entry point.
    * This will be the base name of the tasks file to execute, with no ``.yml`` or ``.yaml`` file extension.

    :short_description:

        * A short, one-line description of the entry point. Ideally, it is a phrase and not a sentence.
        * The ``short_description`` is displayed by ``ansible-doc -t role -l``.
        * It also becomes part of the title for the role page in the documentation.
        * The short description should always be a string and never a list, and should not end in a period.
        * You can use :ref:`Ansible markup <ansible_markup>` in this field.

    :description:

        * A longer description that may contain multiple lines.
        * This can be a single string or a list of strings. In case this is a list of strings, every list
           element is a new paragraph.
        * You can use :ref:`Ansible markup <ansible_markup>` in this field.

    :version_added:

        * The version of the role when the entrypoint was added.
        * This is a string, and not a float, for example, ``version_added: '2.1'``.
        * In collections, this must be the collection version the entrypoint was added to. For example, ``version_added: 1.0.0``.

    :author:

        * Name of the entry point authors.
        * This can be a single string or a list of strings. Use one list entry per author.
          If there is only a single author, use a string or a one-element list.

    :options:

        * Options are often called "parameters" or "arguments". This section defines those options.
        * For each role option (argument), you may include:

        :option-name:

            * The name of the option/argument.

        :description:

            * Detailed explanation of what this option does. It should be written in full sentences.
            * This can be a single string or a list of strings. In case this is a list of strings, every list
              element is a new paragraph.
            * You can use :ref:`Ansible markup <ansible_markup>` in this field.

        :version_added:

            * Only needed if this option was added after the initial role/entry point release. In other words, this is greater than the top level ``version_added`` field.
            * This is a string, and not a float, for example, ``version_added: '2.1'``.
            * In collections, this must be the collection version the option was added to. For example, ``version_added: 1.0.0``.

        :type:

            * The data type of the option. See :ref:`Argument spec <argument_spec>` for allowed values for ``type``. The default is ``str``.
            * If an option is of type ``list``, ``elements`` should be specified.

        :required:

            * Only needed if ``true``.
            * If missing, the option is not required.

        :default:

            * If ``required`` is ``false``/missing, ``default`` may be specified (assumed ``null`` if missing).
            * Ensure that the default value in the docs matches the default value in the code. The actual
              default for the role variable will always come from the role defaults (as defined in :ref:`Role directory structure <role_directory_structure>`).
            * The default field must not be listed as part of the description unless it requires additional information or conditions.
            * If the option is a boolean value, you should use ``true``/``false`` if you want to be compatible with ``ansible-lint``.

        :choices:

            * List of option values.
            * Should be absent if empty.

        :elements:

            * Specifies the data type for list elements when the type is ``list``.

        :options:

            * If this option takes a dict or list of dicts, you can define the structure here.

Sample specification
--------------------

.. code-block:: yaml

  # roles/myapp/meta/argument_specs.yml
  ---
  argument_specs:
    # roles/myapp/tasks/main.yml entry point
    main:
      short_description: Main entry point for the myapp role
      description:
        - This is the main entrypoint for the C(myapp) role.
        - Here we can describe what this entrypoint does in lengthy words.
        - Every new list item is a new paragraph. You can have multiple sentences
          per paragraph.
      author:
        - Daniel Ziegenberg
      options:
        myapp_int:
          type: "int"
          required: false
          default: 42
          description:
            - "The integer value, defaulting to 42."
            - "This is a second paragraph."

        myapp_str:
          type: "str"
          required: true
          description: "The string value"

        myapp_list:
          type: "list"
          elements: "str"
          required: true
          description: "A list of string values."
          version_added: 1.3.0

        myapp_list_with_dicts:
          type: "list"
          elements: "dict"
          required: false
          default:
            - myapp_food_kind: "meat"
              myapp_food_boiling_required: true
              myapp_food_preparation_time: 60
            - myapp_food_kind: "fruits"
              myapp_food_preparation_time: 5
          description: "A list of dicts with a defined structure and with default a value."
          options:
            myapp_food_kind:
              type: "str"
              choices:
                - "vegetables"
                - "fruits"
                - "grains"
                - "meat"
              required: false
              description: "A string value with a limited list of allowed choices."

            myapp_food_boiling_required:
              type: "bool"
              required: false
              default: false
              description: "Whether the kind of food requires boiling before consumption."

            myapp_food_preparation_time:
              type: int
              required: true
              description: "Time to prepare a dish in minutes."

        myapp_dict_with_suboptions:
          type: "dict"
          required: false
          default:
            myapp_host: "bar.foo"
            myapp_exclude_host: true
            myapp_path: "/etc/myapp"
          description: "A dict with a defined structure and default values."
          options:
            myapp_host:
              type: "str"
              choices:
                - "foo.bar"
                - "bar.foo"
                - "ansible.foo.bar"
              required: true
              description: "A string value with a limited list of allowed choices."

            myapp_exclude_host:
              type: "bool"
              required: true
              description: "A boolean value."

            myapp_path:
              type: "path"
              required: true
              description: "A path value."

            original_name:
              type: list
              elements: "str"
              required: false
              description: "An optional list of string values."

    # roles/myapp/tasks/alternate.yml entry point
    alternate:
      short_description: Alternate entry point for the myapp role
      description:
        - This is the alternate entrypoint for the C(myapp) role.
      version_added: 1.2.0
      options:
        myapp_int:
          type: "int"
          required: false
          default: 1024
          description: "The integer value, defaulting to 1024."

.. _run_role_twice:

Running a role multiple times in one play
=========================================

Ansible only executes each role once in a play, even if you define it multiple times unless the parameters defined on the role are different for each definition. For example, Ansible only runs the role ``foo`` once in a play like this:

.. code-block:: yaml

    ---
    - hosts: webservers
      roles:
        - foo
        - bar
        - foo

You have two options to force Ansible to run a role more than once.

Passing different parameters
----------------------------

If you pass different parameters in each role definition, Ansible runs the role more than once. Providing different variable values is not the same as passing different role parameters. You must use the ``roles`` keyword for this behavior, since ``import_role`` and ``include_role`` do not accept role parameters.

This play runs the ``foo`` role twice:

.. code-block:: yaml

    ---
    - hosts: webservers
      roles:
        - { role: foo, message: "first" }
        - { role: foo, message: "second" }

This syntax also runs the ``foo`` role twice;

.. code-block:: yaml

    ---
    - hosts: webservers
      roles:
        - role: foo
          message: "first"
        - role: foo
          message: "second"

In these examples, Ansible runs ``foo`` twice because each role definition has different parameters.

Using ``allow_duplicates: true``
--------------------------------

Add ``allow_duplicates: true`` to the ``meta/main.yml`` file for the role:

.. code-block:: yaml

    # playbook.yml
    ---
    - hosts: webservers
      roles:
        - foo
        - foo

    # roles/foo/meta/main.yml
    ---
    allow_duplicates: true

In this example, Ansible runs ``foo`` twice because we have explicitly enabled it to do so.

.. _role_dependencies:

Using role dependencies
=======================

Role dependencies let you automatically pull in other roles when using a role.

Role dependencies are prerequisites, not true dependencies. The roles do not have a parent/child relationship. Ansible loads all listed roles, runs the roles listed under ``dependencies`` first, then runs the role that lists them. The play object is the parent of all roles, including roles called by a ``dependencies`` list.

Role dependencies are stored in the ``meta/main.yml`` file within the role directory. This file should contain a list of roles and parameters to insert before the specified role. For example:

.. code-block:: yaml

    # roles/myapp/meta/main.yml
    ---
    dependencies:
      - role: common
        vars:
          some_parameter: 3
      - role: apache
        vars:
          apache_port: 80
      - role: postgres
        vars:
          dbname: blarg
          other_parameter: 12

Ansible always executes roles listed in ``dependencies`` before the role that lists them. Ansible executes this pattern recursively when you use the ``roles`` keyword. For example, if you list role ``foo`` under ``roles:``, role ``foo`` lists role ``bar`` under ``dependencies`` in its meta/main.yml file, and role ``bar`` lists role ``baz`` under ``dependencies`` in its meta/main.yml, Ansible executes ``baz``, then ``bar``, then ``foo``.

Running role dependencies multiple times in one play
----------------------------------------------------

Ansible treats duplicate role dependencies like duplicate roles listed under ``roles:``: Ansible only executes role dependencies once, even if defined multiple times, unless the parameters, tags, or when clause defined on the role are different for each definition. If two roles in a play both list a third role as a dependency, Ansible only runs that role dependency once, unless you pass different parameters, tags, when clause, or use ``allow_duplicates: true`` in the role you want to run multiple times. See :ref:`Galaxy role dependencies <galaxy_dependencies>` for more details.

.. note::

    Role deduplication does not consult the invocation signature of parent roles. Additionally, when using ``vars:`` instead of role params, there is a side effect of changing variable scoping. Using ``vars:`` results in those variables being scoped at the play level. In the below example, using ``vars:`` would cause ``n`` to be defined as ``4`` throughout the entire play, including roles called before it.

    In addition to the above, users should be aware that role de-duplication occurs before variable evaluation. This means that :term:`Lazy Evaluation` may make seemingly different role invocations equivalently the same, preventing the role from running more than once.


For example, a role named ``car`` depends on a role named ``wheel`` as follows:

.. code-block:: yaml

    ---
    dependencies:
      - role: wheel
        n: 1
      - role: wheel
        n: 2
      - role: wheel
        n: 3
      - role: wheel
        n: 4

And the ``wheel`` role depends on two roles: ``tire`` and ``brake``. The ``meta/main.yml`` for wheel would then contain the following:

.. code-block:: yaml

    ---
    dependencies:
      - role: tire
      - role: brake

And the ``meta/main.yml`` for ``tire`` and ``brake`` would contain the following:

.. code-block:: yaml

    ---
    allow_duplicates: true

The resulting order of execution would be as follows:

.. code-block:: text

    tire(n=1)
    brake(n=1)
    wheel(n=1)
    tire(n=2)
    brake(n=2)
    wheel(n=2)
    ...
    car

To use ``allow_duplicates: true`` with role dependencies, you must specify it for the role listed under ``dependencies``, not for the role that lists it. In the example above, ``allow_duplicates: true`` appears in the ``meta/main.yml`` of the ``tire`` and ``brake`` roles. The ``wheel`` role does not require ``allow_duplicates: true``, because each instance defined by ``car`` uses different parameter values.

.. note::
   See :ref:`playbooks_variables` for details on how Ansible chooses among variable values defined in different places (variable inheritance and scope).
   Also, deduplication happens ONLY at the play level, so multiple plays in the same playbook may rerun the roles.

.. _embedding_modules_and_plugins_in_roles:

Embedding modules and plugins in roles
======================================

.. note::
    This applies only to standalone roles. Roles in collections do not support plugin embedding; they must use the collection's ``plugins`` structure to distribute plugins.

If you write a custom module (see :ref:`developing_modules`) or a plugin (see :ref:`developing_plugins`), you might wish to distribute it as part of a role. For example, if you write a module that helps configure your company's internal software, and you want other people in your organization to use this module, but do not want to tell everyone how to configure their Ansible library path, you can include the module in your internal_config role.

To add a module or a plugin to a role:
Alongside the 'tasks' and 'handlers' structure of a role, add a directory named 'library' and then include the module directly inside the 'library' directory.

Assuming you had this:

.. code-block:: text

    roles/
        my_custom_modules/
            library/
                module1
                module2

The module will be usable in the role itself, as well as any roles that are called *after* this role, as follows:

.. code-block:: yaml

    ---
    - hosts: webservers
      roles:
        - my_custom_modules
        - some_other_role_using_my_custom_modules
        - yet_another_role_using_my_custom_modules

If necessary, you can also embed a module in a role to modify a module in Ansible's core distribution. For example, you can use the development version of a particular module before it is released in production releases by copying the module and embedding the copy in a role. Use this approach with caution, as API signatures may change in core components, and this workaround is not guaranteed to work.

The same mechanism can be used to embed and distribute plugins in a role, using the same schema. For example, for a filter plugin:

.. code-block:: text

    roles/
        my_custom_filter/
            filter_plugins
                filter1
                filter2

These filters can then be used in a Jinja template in any role called after 'my_custom_filter'.

Sharing roles: Ansible Galaxy
=============================

`Ansible Galaxy <https://galaxy.ansible.com>`_ is a free site for finding, downloading, rating, and reviewing all kinds of community-developed Ansible roles and can be a great way to get a jumpstart on your automation projects.

The client ``ansible-galaxy`` is included in Ansible. The Galaxy client allows you to download roles from Ansible Galaxy and provides an excellent default framework for creating your own roles.

Read the `Ansible Galaxy documentation <https://ansible.readthedocs.io/projects/galaxy-ng/en/latest/>`_ page for more information.

.. seealso::

   :ref:`ansible_galaxy`
       How to create new roles, share roles on Galaxy, role management
   :ref:`yaml_syntax`
       Learn about YAML syntax
   :ref:`working_with_playbooks`
       Review the basic Playbook language features
   :ref:`tips_and_tricks`
       Tips and tricks for playbooks
   :ref:`playbooks_variables`
       Variables in playbooks
   :ref:`playbooks_conditionals`
       Conditionals in playbooks
   :ref:`playbooks_loops`
       Loops in playbooks
   :ref:`tags`
       Using tags to select or skip roles/tasks in long playbooks
   :ref:`list_of_collections`
       Browse existing collections, modules, and plugins
   :ref:`developing_modules`
       Extending Ansible by writing your own modules
   :ref:`Communication<communication>`
       Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide
