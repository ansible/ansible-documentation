
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

One consequence of this change is that a ``no_log`` option value shorter than 4 characters is no longer hidden at all. The placeholder used to replace the value regardless of its length, but masking is subject to the :ref:`minimum secret length <secret_masking_length_rules>`, so such a value is now shown in the output as is. Values of 4 to 6 characters are only masked when they appear as a whole word. If a module option must hold a value this short, set the ``no_log`` task keyword on the task to hide its whole result, or better, use a longer value where the system accepting it allows.

The ``register_secret`` filter fails on a value that is not a string or is shorter than 4 characters after leading and trailing whitespace is stripped, because such a value cannot be masked. Set the filter's ``validation_action`` option to ``warn`` or ``ignore`` to return the value unregistered instead of failing.

Using the ``debug`` module with ``msg`` or ``var`` to show a password or other sensitive value on the screen no longer works. The ``debug`` module writes through ``Display``, so a registered secret is shown as ``$REDACTED$`` wherever it appears, including inside a larger variable and at any verbosity level. There is no option to disable masking for a single task.

If you need to see the real value, for example to confirm that a vault variable decrypts to what you expect, write it to a file instead of displaying it. A file written by a module is not an output boundary, so the file contains the unmasked value:

.. code-block:: yaml+jinja

    - name: Write the secret to a file for inspection
      ansible.builtin.copy:
        content: "{{ db_password }}"
        dest: /tmp/db_password.txt
        mode: "0600"
      delegate_to: localhost

Read the file outside of Ansible and delete it when you are done.

.. _2.22_engine:

Engine
======

Secret masking
--------------

Masking is applied at the points where data leaves Ansible rather than to the data itself:

* All ``Display`` output, including the screen, the ``log_path`` log file, warnings, deprecation messages, errors, and tracebacks.
* The ``result`` mapping of every task result passed to a callback plugin.
* Module logging to syslog and the Windows Event Log, including the module invocation entry.

Secrets registered in a worker process or inside a module on a managed node are sent back to the controller and registered there, so a value discovered by one task is masked in every later task.
Registered secrets that appear in a module's arguments are passed to the module so module-side logging can mask them.

Values shorter than 4 characters are never masked. Values of 4 to 6 characters are only masked when they appear as a whole word. Values longer than 65536 characters are matched on their first 65536 characters. Overlapping and adjacent secrets are replaced with a single placeholder. See :ref:`secret_masking_length_rules` for the details.
Leading and trailing whitespace is stripped from a value before it is registered, so a secret read from a file with a trailing newline is masked with or without that newline.
Masking only matches the exact registered string, so an encoded or hashed copy of a secret is not masked unless it is registered as well. The JSON-escaped form of a secret is the one exception and is always masked.
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

The ``result`` mapping of every task result passed to a callback plugin is now masked before the callback receives it.
Every string value and every string dictionary key in ``result.result`` is masked at any depth of nesting, including inside loop results.
Existing callbacks keep working without changes and no longer see the real value of any registered secret in the result.
Masking also changes some values that are not strings:

* An ``int`` or ``float`` whose text form is a registered secret is replaced with the placeholder string. A callback that expects a number in a result must handle receiving the string ``$REDACTED$`` instead when that number was registered as a secret.
* When two dictionary keys mask to the same placeholder, the second is renamed with a numeric suffix such as ``$REDACTED$ (2)`` so that no entry is lost.
* ``stdout_lines`` and ``stderr_lines`` are rebuilt from the masked ``stdout`` and ``stderr`` so that a secret spanning several lines is masked in the lines as well.

Only ``result.result`` is masked.
Task and play names, the ``warnings``, ``deprecations``, and ``exception`` attributes of the result, the statistics passed to ``v2_playbook_on_stats()``, and anything a callback derives itself are masked only when written through ``Display()``.
A callback that writes such data to a file, socket, HTTP request, database, or any other destination must pass it through ``ansible.module_utils.secrets.mask_secrets()`` first.

To update a custom callback plugin:

#. Audit every place the callback writes data other than through ``Display()``, and mask any data that does not come from ``result.result`` with ``mask_secrets()``.
#. Remove any custom code that stripped ``no_log`` values or checked for ``VALUE_SPECIFIED_IN_NO_LOG_PARAMETER``, as results no longer contain that placeholder.
#. Check any code that relies on the type of a result value, since a number registered as a secret is replaced with a string.

The following example supports both ``ansible-core`` 2.22 and earlier versions.
On versions before 2.22 the ``ansible.module_utils.secrets`` import fails and the result already has ``no_log`` values removed, so ``mask_secrets()`` falls back to returning the text unchanged.
On 2.22 and later the result is already masked and ``mask_secrets()`` covers the task name written alongside it:

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

        def v2_runner_on_ok(self, result):
            # result.result is already masked on 2.22+, but the task name is not, so mask
            # the serialized form before writing it.
            entry = {'task': result.task_name, 'result': result.result}
            entry_json = mask_secrets(json.dumps(entry, default=str))

            with open('/var/log/ansible-results.jsonl', 'a') as fd:
                fd.write(entry_json + '\n')

The ``junit`` and ``tree`` callbacks shipped with ``ansible-core`` are examples of callbacks that write to files and mask everything they write.
The task ``no_log`` keyword continues to censor the entire result regardless of masking as it affects the ``result`` value provided.
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

* The ``password`` lookup registers the generated plaintext password as a secret. The ``unvault`` lookup registers the entire decrypted content of each file as a single secret. The ``vault`` and ``unvault`` filters register the vault password passed to them, and also register the plaintext being encrypted or decrypted as a single secret.
* Vault-encrypted files loaded as variables are parsed and each value is registered individually, so values inside them are masked wherever they appear on their own.
* The ``pause`` action registers user input as a secret when ``echo: false`` is set.
* Connection plugin authors should audit any code that displays the raw standard output or standard error of a module invocation. Secrets that a module registers during its run are returned in the raw JSON result and are not masked until the controller processes it. The connection plugins shipped with ``ansible-core`` only display raw module output when ``ANSIBLE_DEBUG`` is enabled.
* Callback plugins receive task results with registered secrets already masked. The ``junit`` and ``tree`` callbacks pass everything they write to a file through ``mask_secrets()`` so that task and play names and other data not taken from the result are masked as well. See :ref:`2.22_callback_plugins`.

Porting custom scripts
======================

No notable changes

Networking
==========

Secret masking does not apply to the messages logged by the ``persistent_log_messages`` option.
Persistent connections run in a separate ``ansible-connection`` process that does not receive the secrets registered by the controller, so passwords and other sensitive configuration sent over the connection are written to the log in plain text.
Only enable this option while debugging and treat the resulting log as sensitive.
