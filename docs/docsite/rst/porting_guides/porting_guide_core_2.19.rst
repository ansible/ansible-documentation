
.. _porting_2.19_guide_core:

*******************************
Ansible-core 2.19 Porting Guide
*******************************

This section discusses the behavioral changes between ``ansible-core`` 2.18 and ``ansible-core`` 2.19.

It is intended to assist in updating your playbooks, plugins,
and other parts of your Ansible infrastructure so they will work with this version of Ansible.

Review this page and the
`ansible-core Changelog for 2.19 <https://github.com/ansible/ansible/blob/stable-2.19/changelogs/CHANGELOG-v2.19.rst>`_
to understand necessary changes.

This document is part of a collection on porting.
The complete list of porting guides can be found at :ref:`porting guides <porting_guides>`.

.. contents:: Topics

Introduction
============

This release includes an overhaul of the templating system and a new feature dubbed Data Tagging.
These changes enable reporting of numerous problematic behaviors that went undetected in previous releases,
with wide-ranging positive effects on security, performance, and user experience.

Backward compatibility has been preserved where practical, but some breaking changes were necessary.
This guide describes some common problem scenarios with example content, error messsages, and suggested solutions.

We recommend you test your playbooks and roles in a staging environment with this release to determine where you may need to make changes.

Playbook
========

Broken Conditionals
-------------------

Broken conditionals occur when the input expression or template is not a string, or the result is not a boolean.
Python and Jinja provide implicit "truthy" evaluation of most non-empty non-boolean values in conditional expressions.
While sometimes desirable for brevity, truthy conditional evaluation often masks serious logic errors in playbooks that
could not be reliably detected by previous versions of ``ansible-core``.

Changes to templating in this release detects non-boolean conditionals during expression evaluation and reports an error
by default. The error can be temporarily reduced to a warning with the ``ALLOW_BROKEN_CONDITIONALS`` config setting.

The following examples are derived from broken conditionals that masked logic errors in actual playbooks.


Example - implicit boolean conversion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This expression relies on an implicit truthy evaluation of ``inventory_hostname``.
An explicit predicate with a boolean result, such as ``| length > 0`` or ``is truthy``, should be used instead.

.. code-block:: yaml+jinja

    - assert:
        that: inventory_hostname

The error reported is:

.. code-block:: text

    Conditional result was 'localhost' of type 'str', which evaluates to True. Conditionals must have a boolean result.


This can be resolved by using an explicit boolean conversion:

.. code-block:: yaml+jinja

    - assert:
        that: inventory_hostname | length > 0


Example - unintentional truthy conditional
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The second part of this conditional is erroneously quoted.
The quoted part becomes the expression result (evaluated as truthy), so the expression can never be ``False``.

.. code-block:: yaml+jinja

    - assert:
        that: inventory_hostname is defined and 'inventory_hostname | length > 0'


The error reported is:

.. code-block:: text

    Conditional result was 'inventory_hostname | length > 0' of type 'str', which evaluates to True. Conditionals must have a boolean result.


This can be resolved by removing the erroneous quotes:

.. code-block:: yaml+jinja

    - assert:
        that: inventory_hostname is defined and inventory_hostname | length > 0


Example - expression syntax error
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Previous Ansible releases could mask some expression syntax errors as a truthy result.

.. code-block:: yaml+jinja

    - assert:
        that: 1 == 2,
    #               ^ invalid comma


The error reported is:

.. code-block:: text

     Syntax error in expression: chunk after expression


This can be resolved by removing the invalid comma after the expression.


Example - Jinja order of operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This expression uses the ``~`` concatenation operator, which is evaluated after the ``contains`` test.
The result is always a non-empty string, which is truthy.

.. code-block:: yaml+jinja

    - assert:
        that: inventory_hostname is contains "local" ~ "host"


The error reported is:

.. code-block:: text

    Conditional result was 'Truehost' of type 'str', which evaluates to True. Conditionals must have a boolean result.


This can be resolved by inserting parentheses to resolve the concatenation operation before the ``contains`` test:

.. code-block:: yaml+jinja

    - assert:
        that: inventory_hostname is contains("local" ~ "host")


Example - dictionary as conditional
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This conditional should have been quoted.
In a YAML list element, an unquoted string with a space after a colon is interpreted by the YAML parser as a mapping.
Non-empty mappings are always truthy.

.. code-block:: yaml+jinja

    - assert:
        that:
         - result.msg == "some_key: some_value"
    #                             ^^ colon+space == problem

The error reported is:

.. code-block:: text

    Conditional expressions must be strings.


This can be resolved by quoting the entire assertion expression:

.. code-block:: yaml+jinja

    - assert:
        that:
         - 'result.msg == "some_key: some_value"'


Multi-pass templating
---------------------

Embedding templates within other templates or expressions could previously result in untrusted templates being executed.
The overhauled templating engine in this release no longer supports this insecure behavior.


Example - unnecessary template in expression
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This conditional references a variable using a template instead of using the variable directly in the expression.

.. code-block:: yaml+jinja

    - assert:
        that: 1 + {{ value }} == 2
      vars:
        value: 1


The error reported is:

.. code-block:: text

    Syntax error in expression. Template delimiters are not supported in expressions: expected token ':', got '}'


This can be resolved by referencing the variable without a template:

.. code-block:: yaml+jinja

    - assert:
        that: 1 + value == 2
      vars:
        value: 1


Example - dynamic expression construction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This conditional is dynamically created using a template, which is expected to be evaluated as an expression.
Previously, the template was rendered by task argument templating, resulting in a plain string,
which was later evaluated by the ``assert`` action.

.. code-block:: yaml+jinja

    - assert:
        that: inventory_hostname {{ comparison }} 'localhost'
      vars:
        comparison: ==


The error reported is:

.. code-block:: text

    Syntax error in expression. Template delimiters are not supported in expressions: chunk after expression


Dynamic expression construction from playbooks is insecure and unsupported.


.. _untrusted_templates:

Troubleshooting untrusted templates
-----------------------------------

By default, untrusted templates are silently ignored.
Troubleshooting trust issues with templates can be aided by enabling warnings or errors for untrusted templates.
The environment variable ``_ANSIBLE_TEMPLAR_UNTRUSTED_TEMPLATE_BEHAVIOR`` can be used to control this behavior.

Valid options are:

* ``warning`` - A warning will be issued when an untrusted template is encountered.
* ``fail`` - An error will be raised when an untrusted template is encountered.
* ``ignore`` - Untrusted templates are silently ignored and used as-is. This is the default behavior.

.. note::
    This optional warning and failure behavior is experimental and subject to change in future versions.


Loops no longer leak omit placeholders
--------------------------------------

Omit placeholders no longer leak between loop item templating and task templating.

Previously, ``omit`` placeholders could remain embedded in loop items after templating and be used as an ``omit`` for task templating.
Now, values resolving to ``omit`` are dropped immediately when loop items are templated.

To turn missing values into an ``omit`` for task templating, use ``| default(omit)``.
This solution is backward compatible with previous versions of ``ansible-core``.

Example - missing default(omit)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following task tries to pass ``omit`` from a loop to the task, but the value is undefined since it was omitted:

.. code-block:: yaml+jinja

    - debug:
        msg: "{{ item.msg }}"  # 'msg' is undefined
      loop:
       - msg: "{{ omit }}"  # 'msg' will be omitted from the loop item


This updated task uses ``default(omit)`` on the missing value to ensure it is omitted for the task:

.. code-block:: yaml+jinja

    - debug:
        msg: "{{ item.msg | default(omit) }}"  # 'msg' is undefined, use 'default(omit)' to turn it into an omit
      loop:
       - msg: "{{ omit }}"  # passed through in earlier versions, this value is now omitted from the loop item


Privilege escalation timeouts
-----------------------------

Timeout waiting on privilege escalation (``become``) is now an unreachable error instead of a task error.
Existing playbooks should be changed to replace ``ignore_errors`` with ``ignore_unreachable`` on tasks where
timeout on ``become`` should be ignored.


Engine
======

Templating
----------

Template trust model inversion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Previously, ``ansible-core`` implicitly trusted all string values to be rendered as Jinja templates,
but applied an "unsafe" wrapper object around strings obtained from untrusted sources (for example, module results).
Unsafe-wrapped strings were silently ignored by the template engine,
as many templating operations can execute arbitrary code on the control host as the user running ansible-core.
This required any code that operated on strings to correctly propagate the wrapper object,
which resulted in numerous CVE-worthy RCE (remote code execution) vulnerabilities.

This release inverts the previous trust model.
Only strings marked as loaded from a trusted source are eligible to be rendered as templates.
Untrusted values can (as before) be referenced by templates, but the template expression itself must always be trusted.
While this change still requires consideration for propagation of trust markers when manipulating strings,
failure to do so now results in a loss of templating ability instead of a potentially high-severity security issue.

Attempts to render a template appearing in an untrusted string will (as before) return the original string unmodified.
By default, attempting to render an untrusted template fails silently,
though such failures can be elevated to a warning or error via configuration.

Newly-created string results from template operations will never have trust automatically applied,
though templates that return existing trusted string values unmodified will not strip their trust.
It is also possible for plugins to explicitly apply trust.

Backward-compatible template trust behavior is applied automatically in most cases;
for example, templates appearing in playbooks, roles, variable files,
and most built-in inventory plugins will yield trusted template strings.
Custom plugins that source template strings will be required to use new public APIs to apply trust where appropriate.

See :ref:`plugin_api` and :ref:`untrusted_templates` for additional information.


Native Jinja mode required
^^^^^^^^^^^^^^^^^^^^^^^^^^

Previous versions supported templating in two different modes:

* Jinja's original string templating mode converted the result of each templating operation to a string.
* Jinja's native mode *usually* preserved variable types in template results.

In both modes, ``ansible-core`` evaluated the final template string results as Python literals, falling back to the
original string if the evaluation resulted in an error.
Selection of the templating mode was controlled by configuration, defaulting to Jinja's original string templating.

Jinja's native templating mode is now used exclusively.
The configuration option for setting the templating mode is deprecated and no longer has any effect.

Preservation of native types in templating has been improved to correct gaps in the previous implementation,
entirely eliminating the final literal evaluation pass (a frequent source of confusion, errors, and performance issues).
In rare cases where playbooks relied on implicit object conversion from strings,
an explicit conversion will be required.

Some existing templates may unintentionally convert non-strings to strings.
In previous versions this conversion could be masked by the evaluation of strings as Python literals.


Example - unintentional string conversion
"""""""""""""""""""""""""""""""""""""""""

This expression erroneously passes a list to the ``replace`` filter, which operates only on strings.
The filter silently converts the list input to a string.
Due to some string results previously parsing as lists, this mistake often went undetected in earlier versions.

.. code-block:: yaml+jinja

    - debug:
        msg: "{{ ['test1', 'test2'] | replace('test', 'prod') }}"


The result of this template becomes a string:

.. code-block:: ansible-output

    ok: [localhost] => {
        "msg": "['prod1', 'prod2']"
    }


This can be resolved by using the ``map`` filter to apply the ``replace`` filter to each list element:

.. code-block:: yaml+jinja

    - debug:
        msg: "{{ ['test1', 'test2'] | map('replace', 'test', 'prod') }}"


The result of the corrected template remains a list:

.. code-block:: ansible-output

    ok: [localhost] => {
        "msg": [
            "prod1",
            "prod2"
        ]
    }


Lazy templating
^^^^^^^^^^^^^^^

Ansible's interface with the Jinja templating engine has been heavily refined,
yielding significant performance improvements for many complex templating operations.
Previously, deeply-nested, recursive,
or self-referential templating operations were always resolved to their full depth and breadth on every access,
including repeated access to the same data within a single templating operation.
This resulted in expensive and repetitive evaluation of the same templates within a single logical template operation,
even for templates deep inside nested data structures that were never directly accessed.
The new template engine lazily defers nearly all recursion and templating until values are accessed,
or known to be exiting the template engine,
and intermediate nested or indirected templated results are cached for the duration of the template operation,
reducing repetitive templating.
These changes have shown exponential performance improvements for many real-world complex templating scenarios.


Error handling
--------------

Contextual warnings and errors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Changes to internal error handling in ``ansible-core`` will be visible in many situations that result in a warning or error.
In most cases, the operational context (what was happening when the error or warning was generated)
and data element(s) involved are captured and included in user-facing messages.
Errors and warnings that occur during task execution are more consistently included in the task result, with the full
details accessible to callbacks and (in the case of errors), a minimal error message in the ``msg`` field of the result.
Due to the standardized nature of this error handling, seemingly redundant elements may appear in some error messages.
These will improve over time as other error handling improvements are made but are currently necessary to ensure proper
context is available in all error situations.
Error message contents are not considered stable, so automation that relies on them should be avoided when possible.


Variable provenance tracking
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The new Data Tagging feature expands provenance tracking on variables to nearly every source.
This allows for much more descriptive error messaging, as the entire chain of execution can be consulted to include
contextual information about what was happening when an error occurred.
In most cases, this includes file path, source lines, and column markers.
Non-file variable sources such as CLI arguments, inventory plugins and environment are also supported.


Deprecation warnings on value access
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

New features allow most ``ansible-core`` variables and values to be tagged as deprecated.
Plugins and modules can apply these tags to augment deprecated elements of their return values with a description and
help text to suggest alternatives, which will be displayed in a runtime warning when the tagged value is accessed by,
for example, a playbook or template.
This allows for easier evolution and removal of module and fact results, and obsolete core behaviors.

For example, accessing the deprecated ``play_hosts`` magic variable will trigger a deprecation warning that suggests
the use of the ``ansible_play_batch`` variable instead.


Improved Ansible module error handling
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ansible modules implemented in Python now have exception handling provided by the AnsiballZ wrapper.
In previous versions of ``ansible-core``, unhandled exceptions in an Ansible module simply printed a traceback and exited
without providing a standard module response, which caused the task result to contain a generic ``MODULE FAILURE``
message and any raw output text produced by the module.

To address this, modules often implemented unnecessary ``try/except`` blocks around most code where specific error
handling was not possible, only to call ``AnsibleModule.fail_json`` with a generic failure message.
This pattern is no longer necessary, as all unhandled exceptions in Ansible Python modules are now captured by the
AnsiballZ wrapper and returned as a structured module result,
with automatic inclusion of traceback information when enabled by the controller.


Improved handling of undefined
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Undefined handling has been improved to avoid situations where a Jinja plugin silently ignores undefined values.

This commonly occurs when a Jinja plugin, such as a filter or test,
checks the type of a variable without accounting for the possibility of an undefined value being present.


Example - missing attribute
"""""""""""""""""""""""""""

This task incorrectly references an undefined ``exists`` attribute from a ``stat`` result in a conditional.
The undefined value was not detected in previous versions because it is passed to the ``false`` Jinja test plugin,
which silently ignores undefined values.
As a result, this conditional could never be ``True`` in earlier versions of ansible-core,
and there was no indication that the ``failed_when`` expression was invalid.

.. code-block:: yaml+jinja

    - stat:
        path: /does-not-exist
      register: result
      failed_when: result.exists is false
      #                   ^ missing reference to stat

In the current release the faulty expression is detected and results in an error.

This can be corrected by adding the missing ``stat`` attribute to the conditional:

.. code-block:: yaml+jinja

    - stat:
        path: /does-not-exist
      register: result
      failed_when: result.stat.exists is false


Displaying tracebacks
^^^^^^^^^^^^^^^^^^^^^

In previous ``ansible-core`` versions, tracebacks from some controller-side errors were available by increasing verbosity
with the ``-vvv`` option, but the availability and behavior was inconsistent.
This feature was also limited to errors.

Handling of errors, warnings and deprecations throughout much of the ``ansible-core`` codebase has now been standardized.
Tracebacks can be optionally collected and displayed for all exceptions, as well as at the call site of errors,
warnings, or deprecations (even in module code) using the ``ANSIBLE_DISPLAY_TRACEBACK`` environment variable.

Valid options are:

* ``always`` - Tracebacks will always be displayed. This option takes precedence over others below.
* ``never`` - Tracebacks will never be displayed. This option takes precedence over others below.
* ``error`` - Tracebacks will be displayed for errors.
* ``warning`` - Tracebacks will be displayed for warnings other than deprecation warnings.
* ``deprecated`` - Tracebacks will be displayed for deprecation warnings.

Multiple options can be combined by separating them with commas.


.. _plugin_api:

Plugin API
==========

Deprecating values
------------------

Plugins and Python modules can tag returned values as deprecated with the new ``deprecate_value`` function from
``ansible.module_utils.datatag``.
A description of the deprecated feature, optional help text, and removal timeframes can be attached to the value,
which will appear in a runtime warning if the deprecated value is referenced in an expression.
The warning message will include information about the module/plugin that applied the deprecation tag and the
location of the expression that accessed it.

.. code-block:: python

    from ansible.module_utils.datatag import deprecate_value

    ...

    module.exit_json(
        color_name=deprecate_value(
            value="blue",
            msg="The `color_name` return value is deprecated.",
            help_text="Use `color_code` instead.",
        ),
        color_code="#0000ff",
    )


When accessing the `color_name` from the module result, the following warning will be shown

.. code-block:: text

    [DEPRECATION WARNING]: The `color_name` return value is deprecated. This feature will be removed from the 'ns.collection.paint' module in a future release.
    Origin: /examples/use_deprecated.yml:8:14

    6
    7     - debug:
    8         var: result.color_name
                   ^ column 14

    Use `color_code` instead.


Applying template trust to individual values
--------------------------------------------

String values are no longer trusted to be rendered as templates by default. Strings loaded from playbooks, vars files,
and other built-in trusted sources are usually marked trusted by default.
Plugins that create new string instances with embedded templates must use the new ``trust_as_template`` function
from ``ansible.template`` to tag those values as originating from a trusted source to allow the templates
to be rendered.

.. warning::
    This section and the associated public API are currently incomplete.


Applying template trust in inventory and vars plugins
-----------------------------------------------------

Inventory plugins can set group and host variables.
In most cases, these variables are static values from external sources and do not require trust.
Values that can contain templates will require explicit trust via ``trust_as_template`` to be allowed to render,
but trust should not be applied to variable values from external sources that could be maliciously altered to include
templates.

.. warning::
    This section and the associated public API are currently incomplete.


Raising exceptions
------------------

When raising exceptions in an exception handler, be sure to use ``raise ... from`` as appropriate.
This supersedes the use of the ``AnsibleError`` arg ``orig_exc`` to represent the cause.
Specifying ``orig_exc`` as the cause is still permitted for backward compatibility.

Failure to use ``raise ... from`` when ``orig_exc`` is set will result in a warning.
Additionally, if the two cause exceptions do not match, a warning will be issued.


Overly-broad exception handling in Jinja plugins
------------------------------------------------

Jinja plugins with overly broad exception handling, such as ``except Exception``,
may behave incorrectly when accessing the contents of variables which are containers (``dict``, ``list``).
This can occur when a templated value from a variable is undefined,
is an undecryptable vaulted value, or another value which triggers lazily reported fault conditions.

Jinja plugins should catch more specific exception types where possible,
and do so around the smallest reasonable portion of code.
Be especially careful to avoid broad exception handling around code which accesses the contents of container variables.


Ansible custom data types
-------------------------

Many variable objects in ``ansible-core`` are represented by custom types.
In previous versions these could be seen as types such as:

* ``AnsibleUnicode`` (a subclass of ``str``)
* ``AnsibleSequence`` (a subclass of ``list``)
* ``AnsibleMapping`` (a subclass of ``dict``)

These types, and more, now have new subclasses derived from their native Python types.
In most cases these types behave indistinguishably from the types they extend, and existing code should function normally.
However, some Python libraries do not handle builtin object subclasses properly.
Custom plugins that interact with such libraries may require changes to convert and pass the native types.

.. warning::
    This section and the associated public API are currently incomplete.


AnsibleVaultEncryptedUnicode replaced by EncryptedString
--------------------------------------------------------

The ``AnsibleVaultEncryptedUnicode`` type has been replaced by ``EncryptedString``.

Plugins which create ``AnsibleVaultEncryptedUnicode`` will now receive ``EncryptedString`` instances instead.
This feature ensures backward compatibility with previous versions of ``ansible-core``.

Plugins which perform ``isinstance`` checks, looking for ``AnsibleVaultEncryptedUnicode``, will no longer encounter these types.
Values formerly represented by that type will now appear as a tagged ``str`` instead.
Special handling in plugins is no longer required to access the contents of these values.


No implicit conversion of non-string dict keys
----------------------------------------------

In previous versions, ``ansible-core`` relied on Python's ``json.dumps`` to implicitly convert ``int``, ``float``, ``bool`` and ``None`` dictionary keys to strings in various scenarios, including returning of module results.
For example, a module was allowed to contain the following code:

.. code-block:: python

    oid = 123
    d = {oid: "value"}
    module.exit_json(return_value=d)

Starting with this release, modules must explicitly convert any non-string keys to strings (for example, by using the ``str()`` Python function) before passing dictionaries to the ``AnsibleModule.exit_json()`` method of ``ansible-core``. The above code must be changed as follows:

.. code-block:: python

    oid = 123
    d = {str(oid): "value"}
    module.exit_json(return_value=d)

If you encounter ``"[ERROR]: Task failed: Module failed: Key of type '<NON-STRING>' is not JSON serializable by the 'module_legacy_m2c' profile.``, it indicates that the module that is used in the task does not perform the required key conversion.


Command Line
============

No notable changes


Deprecated
==========

No notable changes


Modules
=======

* With the changes to the templating system it is no longer possible to use the ``async_status`` module's ``started`` and ``finished`` integer properties as values in conditionals as booleans are required. It is recommended to use ``started`` and ``finished`` test plugins instead, for example:

.. code-block:: yaml+jinja

    - async_status:
        jid: '{{ registered_task_result.ansible_job_id }}'
      register: job_result
      until: job_result is finished
      retries: 5
      delay: 10


Modules removed
---------------

The following modules no longer exist:

* No notable changes


Deprecation notices
-------------------

No notable changes


Noteworthy module changes
-------------------------

No notable changes


Plugins
=======

Noteworthy plugin changes
-------------------------

* The ``ssh`` connection plugin now supports using ``SSH_ASKPASS`` to supply passwords
  for authentication as an alternative to the ``sshpass`` program. The default is to use
  ``SSH_ASKPASS`` instead of ``sshpass``. This is controlled by the ``password_mechanism``
  configuration for the ``ssh`` connection plugin. To switch back to using ``sshpass``
  make one of the following changes:

  To your ``ansible.cfg`` file:

  .. code-block:: ini

     [ssh_connection]
     password_mechanism = sshpass

  By exporting an environment variable:

  .. code-block:: shell

     export ANSIBLE_SSH_PASSWORD_MECHANISM=sshpass

  By setting the following variable:

  .. code-block:: yaml

     ansible_ssh_password_mechanism: sshpass

* Coercing unrecognized input values in the ``bool`` filter is deprecated.
  The ``bool`` filter now returns only ``True`` or ``False``, depending on the input:

  * ``True`` - Returned for ``True``, ``1`` and case-insensitive matches on the strings: "yes", "on", "true", "1"
  * ``False`` - Returned for ``False``, ``0`` and case-insensitive matches on the strings: "no", "off", "false", "0"

  Any other input will result in a deprecation warning. This warning will become an error in ``ansible-core`` 2.23.

  When a deprecation warning is issued, the return value is ``False`` unless the input equals ``1``,
  which can occur when the input is the ``float`` value of ``1.0``.

  This filter now returns ``False`` instead of ``None`` when the input is ``None``.
  The aforementioned deprecation warning is also issued in this case.

* Passing nested non-scalars with embedded templates that may resolve to ``Undefined`` to Jinja2
  filter plugins, such as ``default`` and ``mandatory``, and test plugins including ``defined`` and ``undefined``
  no longer evaluate as they did in previous versions because nested non-scalars with embedded templates are templated
  on use only.
  In 2.19, this assertion passes:

  .. code-block:: yaml

     - assert:
         that:
           # Unlike earlier versions, complex_var is defined even though complex_var.nested is not.
           - complex_var is defined
           # Unlike earlier versions, the default value is not applied because complex_var is defined.
           - (complex_var | default(unused)).nested is undefined
           # Like earlier versions, directly accessing complex_var.nested evaluates as undefined.
           - complex_var.nested is undefined
       vars:
         complex_var:
           # Before 2.19, complex_var.nested is evaluated immediately when complex_var is accessed.
           # In 2.19, complex_var.nested is evaluated only when it is accessed.
           nested: "{{ undefined_variable }}"
         unused:
           # This variable is used only if complex_var is undefined.
           # This only happens in ansible-core before 2.19.
           nested: default


Porting custom scripts
======================

No notable changes


Networking
==========

No notable changes
