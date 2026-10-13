
.. _porting_2.16_guide_core:

*******************************
Ansible-core 2.16 Porting Guide
*******************************

This section discusses the behavioral changes between ``ansible-core`` 2.15 and ``ansible-core`` 2.16.

It is intended to assist in updating your playbooks, plugins and other parts of your Ansible infrastructure so they will work with this version of Ansible.

We suggest you read this page along with `ansible-core Changelog for 2.16 <https://github.com/ansible/ansible/blob/stable-2.16/changelogs/CHANGELOG-v2.16.rst>`_ to understand what updates you may need to make.

This document is part of a collection on porting. The complete list of porting guides can be found at :ref:`porting guides <porting_guides>`.

.. contents:: Topics


Playbook
========

* Conditionals - due to mitigation of security issue CVE-2023-5764 in ansible-core 2.16.1,
  conditional expressions with embedded template blocks can fail with the message
  "``Conditional is marked as unsafe, and cannot be evaluated.``" when an embedded template
  consults data from untrusted sources like module results or vars marked ``!unsafe``.
  Conditionals with embedded templates can be a source of malicious template injection when
  referencing untrusted data, and can nearly always be rewritten without embedded
  templates. Playbook task conditional keywords such as ``when`` and ``until`` have long
  displayed warnings discouraging use of embedded templates in conditionals; this warning
  has been expanded to non-task conditionals as well, such as the ``assert`` action.

  .. code-block:: yaml

     - name: task with a module result (always untrusted by Ansible)
       shell: echo "hi mom"
       register: untrusted_result

     # don't do it this way...
     # - name: insecure conditional with embedded template consulting untrusted data
     #   assert:
     #     that: '"hi mom" is in {{ untrusted_result.stdout }}'

     - name: securely access untrusted values directly as Jinja variables instead
       assert:
         that: '"hi mom" is in untrusted_result.stdout'

Command Line
============


Deprecated
==========

``ansible-core`` 2.16.20 backports several warnings from versions 2.19 and later, most of them deprecation warnings.
These warnings give you advance notice of upcoming changes if you plan to upgrade across several releases at once.
The following sections describe each warning and how to resolve it. Except where noted, you can disable these
warnings by setting ``deprecation_warnings=False`` in ``ansible.cfg``.

.. DWCODE: invalid_inventory_name

Invalid inventory variables
---------------------------

Setting Ansible inventory variables with invalid names is deprecated. Variables must start with a letter
or underscore character, and contain only letters, numbers and underscores. Variable names must also not
be one of the following Jinja keywords: ``true``, ``True``, ``false``, ``False``, ``none``, ``None``, ``not``.

Example
^^^^^^^

An example inventory with an invalid value:

.. code-block:: text

    localhost ansible_connection=local true=123

will produce the following warning:

.. code-block:: text

    [DEPRECATION WARNING]: Accepting inventory variable with invalid name 'true'. Variable names must be strings
    starting with a letter or underscore character, and contain only letters, numbers and underscores. This feature
    will be removed in version 2.23. Deprecation warnings can be disabled by setting deprecation_warnings=False in
    ansible.cfg.

This can be resolved by renaming the variable to match the requirements.

.. DWCODE: task_args_empty

Empty ``args`` keyword
----------------------

Specifying the task ``args`` keyword without a value is deprecated.

Example
^^^^^^^

The example task below uses an empty ``args``:

.. code-block:: yaml

    - name: Print a message
      ansible.builtin.debug:
        msg: "Hello, World"
      args:

The above task will produce the following warning:

.. code-block:: text

    [DEPRECATION WARNING]: Ignoring empty task `args` keyword. A mapping or template which resolves to a mapping is
    required. This feature will be removed in version 2.23. Deprecation warnings can be disabled by setting
    deprecation_warnings=False in ansible.cfg.

This can be resolved by ensuring that ``args`` is never supplied an empty value.

.. DWCODE: task_action_mapping

Using a mapping for ``action``
------------------------------

Using a mapping for ``action`` is deprecated. Use a string value for ``action``.

Example
^^^^^^^

The example task below uses a mapping for the ``action`` keyword, specifying the module to execute:

.. code-block:: yaml

    - name: Print a message
      action:
        module: "ansible.builtin.debug"
      args:
        msg: "Hello World!"

The above task will produce the following warning:

.. code-block:: text

    [DEPRECATION WARNING]: Using a mapping for `action` is deprecated. Use a string value for `action`. This
    feature will be removed in version 2.23. Deprecation warnings can be disabled by setting
    deprecation_warnings=False in ansible.cfg.

This can be resolved by using a string for the ``action`` value, like so:

.. code-block:: yaml

    - name: Print a message
      action: "ansible.builtin.debug"
      args:
        msg: "Hello World!"

.. DWCODE: task_args_merge

Task argument merging
---------------------

Using ``key=value`` style arguments and the task ``args`` keyword on the same task is deprecated.

Example
^^^^^^^

.. code-block:: yaml

    - name: List home directories
      ansible.builtin.find: paths="/home"
      args:
        file_type: "directory"

The above task will produce the following warning:

.. code-block:: text

    [DEPRECATION WARNING]: Merging legacy k=v args ('paths') into task args. Include all task args in the task
    `args` mapping. This feature will be removed in version 2.23. Deprecation warnings can be disabled by setting
    deprecation_warnings=False in ansible.cfg.

One way to resolve this is by moving the key=value arguments into the ``args`` section. For example:

.. code-block:: yaml

    - name: List home directories
      ansible.builtin.find:
      args:
        paths: "/home"
        file_type: "directory"

Alternatively, for this example, you could also provide the arguments with the normal (and simpler) pattern:

.. code-block:: yaml

    - name: List home directories
      ansible.builtin.find:
        paths: "/home"
        file_type: "directory"

.. DWCODE: bool_filter_invalid_value

Invalid ``bool`` filter values
------------------------------

Support for coercing unrecognized input values (including None) to a boolean using the ``bool`` filter
has been deprecated.

Example
^^^^^^^

.. code-block:: yaml+jinja

    - name: Print a message
      ansible.builtin.debug:
        msg: "{{ [] | bool }}"

The above task will produce the following warning:

.. code-block:: text

    [DEPRECATION WARNING]: The `bool` filter coerced invalid value [] (list) to False. This feature will be removed
    in version 2.23. Deprecation warnings can be disabled by setting deprecation_warnings=False in ansible.cfg.

To resolve this, use an explicit predicate with a boolean result, such as ``| length > 0`` or ``is truthy``.

.. DWCODE: from_yaml_non_string
.. DWCODE: from_yaml_all_non_string

Filters ``from_yaml`` and ``from_yaml_all``
-------------------------------------------

Using the ``from_yaml`` and ``from_yaml_all`` filters with non-string data has been deprecated.

Example
^^^^^^^

.. code-block:: yaml+jinja

    - name: Parse a list
      ansible.builtin.debug:
        msg: "{{ [] | from_yaml }}"

    - name: Parse a mapping
      ansible.builtin.debug:
        msg: "{{ {} | from_yaml_all }}"

The above tasks will produce the following warnings, respectively:

.. code-block:: text

    [DEPRECATION WARNING]: The from_yaml filter ignored non-string input of type <class 'list'>. This feature will be
    removed in version 2.23. Deprecation warnings can be disabled by setting deprecation_warnings=False in ansible.cfg.

    [DEPRECATION WARNING]: The from_yaml_all filter ignored non-string input of type <class 'dict'>. This feature will be
    removed in version 2.23. Deprecation warnings can be disabled by setting deprecation_warnings=False in ansible.cfg.

To resolve these, make sure your inputs are of a string type.

.. DWCODE: templar_available_variables

Accessing ``Templar._available_variables``
------------------------------------------

Direct access to the ``_available_variables`` internal attribute of the ``Templar`` class is deprecated.

Accessing that internal variable will result in the following warning:

.. code-block:: text

    [DEPRECATION WARNING]: Direct access to the `_available_variables` internal attribute is deprecated. This feature
    will be removed from ansible-core version 2.23. Use `available_variables` instead.

To resolve this, use the ``Templar.available_variables`` attribute instead.

.. DWCODE: templar_loader

Accessing ``Templar._loader``
-----------------------------

Direct access to the ``_loader`` internal attribute of the ``Templar`` class is deprecated.

Accessing that internal variable will result in the following warning:

.. code-block:: text

    [DEPRECATION WARNING]: Direct access to the `_loader` internal attribute is deprecated. This feature will be
    removed from ansible-core version 2.23. Use `copy_with_new_env` to create a new instance.

Use the ``Templar.copy_with_new_env()`` method if you only need a derived ``Templar`` instance. If you need the
data loader itself, keep a reference to the ``DataLoader`` you created rather than reading it back from the
``Templar``, since the attribute it is stored in is internal and subject to change.

.. DWCODE: templar_environment

Accessing ``Templar.environment``
---------------------------------

Direct access to the ``environment`` attribute of the ``Templar`` class is deprecated.

Accessing that internal variable will result in the following warning:

.. code-block:: text

    [DEPRECATION WARNING]: Direct access to the `environment` attribute is deprecated. This feature will be
    removed from ansible-core version 2.23. Consider using `copy_with_new_env` or passing `overrides` to `template`.

As suggested by the deprecation warning, use the ``Templar.copy_with_new_env()`` method to obtain a new
``Templar`` instance, or use ``Templar.template()`` and set the ``overrides`` parameter.

.. DWCODE: conditional_empty

Empty conditional expressions
-----------------------------

Conditional expressions (such as ``when`` in playbook tasks or ``that`` in the ``assert`` action) which are a
literal ``None`` or an empty string evaluate as True and will issue a deprecation warning.

Example
^^^^^^^

.. code-block:: yaml+jinja

    - name: Print a message
      ansible.builtin.debug:
        msg: "test"
      when: ""

The above task will produce the following warning:

.. code-block:: text

    [DEPRECATION WARNING]: Empty conditional expression was evaluated as True. This feature will be removed in
    version 2.23. Deprecation warnings can be disabled by setting deprecation_warnings=False in ansible.cfg.

Such expressions should be removed or corrected to always ensure a strictly boolean (True or False) result.

.. DWCODE: test_non_boolean

Non-boolean test plugin results
-------------------------------

Test plugins which return a non-boolean result are deprecated; the result is coerced to a boolean for now, but
test plugins must have a boolean result in ansible-core 2.23 and later.

Non-conforming test plugins will see a deprecation message like the following:

.. code-block:: text

    [DEPRECATION WARNING]: The test plugin 'my_test_plugin' returned a non-boolean result of type <class 'NoneType'>.
    Test plugins must have a boolean result. This feature will be removed in version 2.23. Deprecation warnings can be
    disabled by setting deprecation_warnings=False in ansible.cfg.

To resolve this, update the test plugin to return a boolean, for example by wrapping the result in ``bool()``.
Starting with ansible-core 2.23, a non-boolean result is an error rather than a warning.

.. DWCODE: unknown_type_encountered_handler

Templating of unknown types
---------------------------

A warning is now emitted when a type unknown to the templating system is encountered in a finalized template result,
since such types are not guaranteed to behave correctly.

Unlike the other warnings in this section, this is a general warning rather than a deprecation warning. Nothing is
being removed in 2.23, and setting ``deprecation_warnings=False`` in ``ansible.cfg`` does not suppress it.

Pinpointing the location of the use of the unknown type is not possible unless you are using ``ansible-core`` 2.19
or higher, where the origin will be displayed along with the warning. This is a best effort notification, giving the name
of the type that is unknown to the templating system.

Warnings of this type will look similar to the following:

.. code-block:: text

    [WARNING]: Encountered unknown type 'NotAVariableType' during template operation. Use supported types to avoid
    unexpected behavior. To troubleshoot further, please upgrade to Ansible core 2.19 or later to find out more about
    the origin of this type.

Custom data types outside of Ansible will be unsupported. Normal Python data types (for example: ``bool``,
``bytes``, ``dict``, ``list``, etc) and many custom Ansible data types (for example: ``AnsibleMapping``,
``AnsibleSequence``, ``HostVars``, etc) are supported.


Modules
=======



Modules removed
---------------



Deprecation notices
-------------------



Noteworthy module changes
-------------------------



Plugins
=======



Porting custom scripts
======================



Networking
==========
