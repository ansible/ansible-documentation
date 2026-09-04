
.. _porting_2.22_guide_core:

*******************************
Ansible-core 2.22 Porting Guide
*******************************

This section discusses the behavioral changes between ``ansible-core`` 2.21 and ``ansible-core`` 2.22.

It is intended to assist in updating your playbooks, plugins,
and other parts of your Ansible infrastructure so they will work with this version of Ansible.

Review this page and the
`ansible-core Changelog for 2.22 <https://github.com/ansible/ansible/blob/stable-2.22/changelogs/CHANGELOG-v2.22.rst>`_
to understand necessary changes.

This document is part of a collection on porting.
The complete list of porting guides can be found at :ref:`porting guides <porting_guides>`.

.. contents:: Topics

.. _2.22_introduction:

Introduction
============

This release adds secret masking. Ansible now registers known secret values, such as decrypted vault content, ``no_log`` module options, and prompted passwords, and replaces them with ``$REDACTED$`` wherever it writes output.
The values themselves are unchanged, so playbooks keep working with the real data and only the rendered output is masked.

Most playbooks need no changes. Content that inspected the ``VALUE_SPECIFIED_IN_NO_LOG_PARAMETER`` placeholder, and modules or plugins that stripped secrets from results by hand, should be reviewed.
Authors of custom callback plugins should update them to declare support for masking, as described in :ref:`2.22_callback_plugins`.

We recommend you test your playbooks, callback plugins, and any tooling that consumes Ansible output in a staging environment with this release.
See :ref:`playbooks_secret_masking` for the user guide and :ref:`developing_secret_masking` for the developer guide.

.. _2.22_playbook:

Playbook
========

Secret masking
--------------

Ansible now masks registered secrets in its output. Values such as decrypted vault content, ``no_log`` module option values, and prompted passwords are replaced with ``$REDACTED$`` on the screen, in the ``log_path`` log file, in callback output, and in module logs on the managed node. The values themselves are unchanged and remain usable by tasks. Use the new ``register_secret`` filter to register your own values and the ``mask_secrets`` filter to redact registered secrets from a string. See :ref:`playbooks_secret_masking` for details, including the minimum secret length and the limitations of masking.

Module options marked with ``no_log: true`` are no longer replaced with the literal ``VALUE_SPECIFIED_IN_NO_LOG_PARAMETER`` in the module result. The real value is kept in the result and registered as a secret so it is masked in output. Playbooks that compared a result value against ``VALUE_SPECIFIED_IN_NO_LOG_PARAMETER`` should be updated.

.. _2.22_engine:

Engine
======

Secret masking
--------------

Masking is applied at the points where data leaves Ansible rather than to the data itself:

* All ``Display`` output, including the screen, the ``log_path`` log file, warnings, deprecation messages, errors, and tracebacks.
* Task results passed to callback plugins that do not declare ``ANSIBLE_SUPPORTS_MASKING``.
* Module logging to syslog and the Windows Event Log, including the module invocation entry.

Secrets registered in a worker process or inside a module on a managed node are sent back to the controller and registered there, so a value discovered by one task is masked in every later task.
Registered secrets that appear in a module's arguments are passed to the module so module-side logging can mask them.

Values shorter than 4 characters are never masked. Values of 4 to 6 characters are only masked when they appear as a whole word. Values longer than 1024 characters are matched on their first 1024 characters.
Masking only matches the exact registered string, so an encoded or hashed copy of a secret is not masked unless it is registered as well.
Masking also only covers messages Ansible writes through ``Display``. Messages that other Python libraries emit with the standard ``logging`` module share the ``log_path`` file and are not masked.

.. _2.22_plugin_api:

Plugin API
==========

Secret masking API
------------------

* The ``ansible.module_utils.secrets`` module is a new public API providing ``register_secret()``, ``register_secrets()``, and ``mask_secrets()``. See :ref:`developing_secret_masking`.
* The ``Ansible.Secrets`` C# module util provides the same API for PowerShell modules through ``[Ansible.Secrets.SecretMasker]``.
* Plugin configuration options can set ``secret: true`` to register the resolved value as a secret regardless of the source that set it.
* ``AnsibleModule`` no longer strips ``no_log`` values from module results.

Values registered through the secrets API are masked in ``Display`` output, callback output, and module logs.
Any plugin or module that discovers a sensitive value at runtime, such as a token returned by an API, should register it as soon as it is known.

The ``secret`` configuration keyword is only supported for the ``str``, ``string``, and ``list`` types and is not supported on ``suboptions``.
Declaring it on any other type is an error when the plugin configuration is loaded.
The ``ansible-core`` connection and become plugins use it for their password and key options, and plugins that accept a password or token should do the same.

Modules that relied on ``remove_values()`` or ``sanitize_keys()`` to strip ``no_log`` values from their results should remove those calls.
The values are now masked at the output boundary instead, and both helpers are deprecated.

.. _2.22_callback_plugins:

Callback plugins
----------------

Custom callback plugins are the plugins most likely to need changes with this release.

Callback plugins now receive task results in one of two forms, chosen by the new ``ANSIBLE_SUPPORTS_MASKING`` class attribute:

* When the attribute is not set, or is ``False``, every string value in ``result.result`` is masked before the callback sees it, including values nested in lists and dictionaries. Existing callbacks keep working without changes but cannot see the real values.
* When the attribute is ``True``, the callback receives the real values and is responsible for masking anything it writes outside of ``Display()``.

The ``False`` behavior is a compatibility shim, not a complete solution.
It exists only so that existing callback plugins do not break with this release.
It masks the task result as a whole before the callback receives it, so it can only redact secrets that are present in the result at that point and may miss data that only become a secret after it is serialized to a string.
Anything the callback derives from other sources, formats itself, or combines with data from elsewhere is outside its reach, and the walk over every result also carries a performance cost.

Moving to the new mechanism, where the callback masks at each of its own egress points outside of ``Display()``, means the values are masked at the moment they are written and nothing is missed.
This is the supported approach going forward.

The compatibility shim will be deprecated in a future release and then removed.
Removal is tentatively planned for ``ansible-core`` 2.27, but that version is subject to change until an official deprecation warning is added.
Update your callback plugins now so they continue to redact secrets when the shim is removed:

#. Set ``ANSIBLE_SUPPORTS_MASKING = True`` on the callback class.
#. Audit every place the callback writes data. Output sent through ``Display()`` is masked automatically. Output written to a file, socket, HTTP request, database, or any other destination must be passed through ``ansible.module_utils.secrets.mask_secrets()`` first.
#. Remove any custom code that stripped ``no_log`` values or checked for ``VALUE_SPECIFIED_IN_NO_LOG_PARAMETER``, as results no longer contain that placeholder.

The following example supports both ``ansible-core`` 2.22 and earlier versions.
On versions before 2.22 the ``ansible.module_utils.secrets`` import fails, the attribute has no effect, and the result already has ``no_log`` values removed, so ``mask_secrets()`` falls back to returning the text unchanged.
On 2.22 and later the callback receives the real values and masks them itself:

.. code-block:: python

    import json

    from ansible.plugins.callback import CallbackBase

    try:
        from ansible.module_utils.secrets import mask_secrets
    except ImportError:
        # ansible-core < 2.22 has no secret masking API. Results on those versions
        # already have no_log values removed, so there is nothing to mask here.
        def mask_secrets(value):
            return value


    class CallbackModule(CallbackBase):
        CALLBACK_VERSION = 2.0
        CALLBACK_TYPE = 'notification'
        CALLBACK_NAME = 'namespace.collection_name.json_file'
        CALLBACK_NEEDS_ENABLED = True

        # Ignored by ansible-core < 2.22. On 2.22+ this opts in to receiving unmasked results.
        ANSIBLE_SUPPORTS_MASKING = True

        def v2_runner_on_ok(self, result):
            # result.result contains real values on 2.22+, so mask the serialized form before writing it.
            with open('/var/log/ansible-results.jsonl', 'a') as fd:
                result_json = json.dumps(result.result, default=str)
                redacted_json = mask_secrets(result_json)
                fd.write(redacted_json + '\n')

The ``junit`` and ``tree`` callbacks shipped with ``ansible-core`` are examples of callbacks that write to files and mask their own output.
The task ``no_log`` keyword continues to censor the entire result regardless of this attribute as it affects the ``result`` value provided.
See :ref:`developing_callbacks_masking` for more details.

.. _2.22_command_line:

Command Line
============

* Passwords entered for ``--ask-pass``, ``--ask-become-pass``, and ``--ask-vault-pass`` are registered as secrets and masked in output.
* Values entered for a ``vars_prompt`` with ``private: true`` (the default) are registered as secrets and masked in output.

.. _2.22_deprecated:

Deprecated
==========

* ``ansible.module_utils.basic.heuristic_log_sanitize()`` is deprecated and will be removed in ``ansible-core`` 2.25. Secret values are now masked automatically. Use the ``ansible.module_utils.secrets`` API to handle secrets manually.
* ``ansible.module_utils.common.parameters.remove_values()`` and ``sanitize_keys()`` are deprecated and will be removed in ``ansible-core`` 2.25. Secret values are now masked automatically. Use the ``ansible.module_utils.secrets`` API to handle secrets manually.
* The ``live`` argument of ``ansible.utils.cmd_functions.run_cmd()`` is deprecated and will be removed in ``ansible-core`` 2.25 because it bypasses secret masking. Callers that need to stream output live should run the subprocess themselves and mask any secrets in the output.

.. _2.22_modules:

Modules
=======

Modules removed
---------------

The following modules no longer exist:

* No notable changes

Deprecation notices
-------------------

No notable changes

Noteworthy module changes
-------------------------

* Module options marked ``no_log: true`` keep their real value in the module result instead of being replaced with ``VALUE_SPECIFIED_IN_NO_LOG_PARAMETER``. The value is registered as a secret and masked in output. See :ref:`secret_masking_no_log`.
* Values logged by ``AnsibleModule.log()`` and the module invocation log entry now use ``$REDACTED$`` in place of the previous ``NOT_LOGGING_PARAMETER`` and ``NOT_LOGGING_PASSWORD`` placeholders, and any other registered secret in the message is masked.
* ``AnsibleModule.log()`` and the module invocation log no longer apply the ``heuristic_log_sanitize()`` heuristics. For example, ``user:password@host`` in a URL is no longer rewritten unless the password is a registered secret.
* ``AnsibleModule.run_command()`` no longer replaces password-like arguments such as ``--password=...`` with ``********`` in the ``cmd`` value of a failure result, and no longer passes the ``msg`` value through ``heuristic_log_sanitize()``.
* The ``uri`` module no longer rewrites response keys to strip ``no_log`` values. Registered secrets are masked in output instead.

Only registered secrets are masked in the values above.
Modules that pass a secret on the command line or embed one in a URL, where that secret is not a ``no_log`` option, should register it with ``ansible.module_utils.secrets.register_secret()``.

Plugins
=======

Noteworthy plugin changes
-------------------------

* The following plugin options are marked ``secret: true`` and are masked in output:

  * ``ssh`` connection plugin: ``password``, ``private_key``, and ``private_key_passphrase``
  * ``winrm`` connection plugin: ``password``
  * ``psrp`` connection plugin: ``password`` and ``certificate_key_password``
  * ``sudo``, ``su``, and ``runas`` become plugins: ``become_pass``
  * ``url`` lookup plugin: ``password``

* The ``password`` lookup registers the generated plaintext password as a secret. The ``unvault`` lookup registers the entire decrypted content of each file as a single secret, and the ``vault`` and ``unvault`` filters register the vault password passed to them.
* Vault-encrypted files loaded as variables are parsed and each value is registered individually, so values inside them are masked wherever they appear on their own.
* The ``pause`` action registers user input as a secret when ``echo: false`` is set.
* Connection plugin authors should audit any code that displays the raw standard output or standard error of a module invocation. Secrets that a module registers during its run are returned in the raw JSON result and are not masked until the controller processes it. The connection plugins shipped with ``ansible-core`` only display raw module output when ``ANSIBLE_DEBUG`` is enabled.
* The ``default``, ``minimal``, ``oneline``, ``junit``, and ``tree`` callback plugins set ``ANSIBLE_SUPPORTS_MASKING = True`` and mask their own output. The ``junit`` and ``tree`` callbacks pass everything they write to a file through ``mask_secrets()``.

Porting custom scripts
======================

No notable changes

Networking
==========

Secret masking does not apply to the messages logged by the ``persistent_log_messages`` option.
Persistent connections run in a separate ``ansible-connection`` process that does not receive the secrets registered by the controller, so passwords and other sensitive configuration sent over the connection are written to the log in plain text.
Only enable this option while debugging and treat the resulting log as sensitive.
