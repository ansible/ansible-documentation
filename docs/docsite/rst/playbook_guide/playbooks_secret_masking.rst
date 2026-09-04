.. _playbooks_secret_masking:
.. _secret_masking:

*********************************
Masking secrets in Ansible output
*********************************

.. versionadded:: 2.22

Ansible can register values as secrets and mask them wherever Ansible writes output.
Once a value is registered, it is replaced with the placeholder ``$REDACTED$`` on the screen, in the ``log_path`` log file, in callback output, and in module logs on the managed node.
The value itself is not changed. Tasks, templates, and modules keep working with the real value, only the output is masked.

This page explains what masking covers, which values Ansible registers automatically, how to register your own secrets in a playbook, and the limits of the feature.
If you are writing modules or plugins, see :ref:`developing_secret_masking` for the developer API.

.. contents::
   :local:

Where masking happens
=====================

Masking happens at an *egress boundary*: a place where data leaves Ansible and could be seen or stored by something else.
Data that stays inside Ansible, such as variables, module arguments, and task results, is never altered.
Ansible masks registered secrets at the following boundaries:

* **Display output**, which covers the screen and the ``log_path`` log file.
* **Callback plugins**, which receive masked task results unless they mask their own output.
* **Module logging**, which covers syslog and the Windows Event Log on the managed node.

Display output includes task banners, ``debug`` messages, warnings, deprecation messages, error messages, tracebacks, and verbose (``-v``) module invocation output.
Everything the ``Display`` object writes is masked, both on the screen and in the file set by the ``log_path`` :ref:`configuration setting <DEFAULT_LOG_PATH>`.

Task results handed to a callback plugin are masked before the plugin sees them, unless the plugin declares that it handles masking itself.
The callback plugins shipped with ``ansible-core``, such as ``default``, ``minimal``, ``oneline``, ``junit``, and ``tree``, declare this and mask their own output.
See :ref:`developing_callbacks_masking` for the details.

Module logging covers messages that a module writes through ``AnsibleModule.log()``, including the module invocation entry.
These are masked on the managed node before they reach syslog or the Event Log.

Because masking is applied at the boundary rather than to the data, a value registered late in a play is still masked in any later output, and the registered value can still be used by its true value in conditionals, templates, and module arguments.

What is registered automatically
================================

Ansible registers the following values as secrets without any action from you:

* **Vault-encrypted content**, once it is decrypted.
* **Vault passwords** supplied by prompt, password file, or password script.
* **Module options marked** ``no_log: true``.
* **Prompted values**, such as passwords entered for ``vars_prompt`` or ``--ask-pass``.
* **Plugin options marked** ``secret: true``, such as connection and become passwords.
* **Generated and decrypted secrets** from the ``password`` and ``unvault`` lookups and the ``vault`` and ``unvault`` filters.

How vault-encrypted content is registered depends on how it is loaded:

* A vault-encrypted file loaded as variables is parsed and each value in it is registered on its own.
* An inline ``!vault`` value is registered as a single string when it is decrypted.
* The ``unvault`` lookup registers the entire decrypted content of each file as a single string.

A vault-encrypted file is loaded as variables through ``vars_files``, ``include_vars``, ``host_vars``, and similar mechanisms.
Ansible walks into lists and dictionaries and registers each nested string, integer, and float value, with numbers registered in their string form.
Dictionary keys are not registered, only the values.

The difference matters when the decrypted text is structured. With a vaulted vars file, a password inside it is masked wherever that password appears on its own. With ``unvault``, only the complete decrypted text is registered, including any newlines. This means a value inside it is masked only when the whole text appears in output. To mask individual values from an ``unvault`` result, parse it and register the values you need with the ``register_secret`` filter.

The value of any option declared with ``no_log`` in a module's argument spec is registered when the module validates its arguments.
This includes values that came from a default, a fallback, or a sub-option.
See :ref:`secret_masking_no_log` for how this changes the ``no_log`` behavior.

Prompted values are registered for a ``vars_prompt`` with ``private: true`` (the default), the ``pause`` module with ``echo: false``, and passwords entered for ``--ask-pass``, ``--ask-become-pass``, and ``--ask-vault-pass``.

Plugin authors can mark configuration options with ``secret: true`` so the resolved value is registered no matter which source set it.
In ``ansible-core`` this includes the ``ssh``, ``winrm``, and ``psrp`` connection passwords, the ``ssh`` private key and passphrase, the ``sudo``, ``su``, and ``runas`` become passwords, and the ``url`` lookup password.

The ``password`` lookup registers the plaintext password it generates.
The ``vault`` and ``unvault`` filters register the vault password passed to them, not the data being encrypted or decrypted.

Registering your own secrets
============================

Use the :ansplugin:`ansible.builtin.register_secret#filter` filter to register any string value from a playbook. The filter returns the value unchanged so you can use it inline:

.. code-block:: yaml+jinja

    - name: Fetch an API token from an external system
      ansible.builtin.uri:
        url: https://example.com/token
        return_content: true
      register: token_response
      no_log: true  # Ensures the module response isn't leaked before registration

    - name: Register the token so it is masked from output
      ansible.builtin.set_fact:
        api_token: "{{ token_response.json.token | register_secret }}"

    - name: The token is still usable but does not appear in output
      ansible.builtin.debug:
        msg: "Using token {{ api_token }}"

The last task prints ``Using token $REDACTED$``.

The filter accepts a single string. To register every string in a list, apply the filter in a loop or with ``map``:

.. code-block:: yaml+jinja

    - name: Register several secrets at once
      ansible.builtin.set_fact:
        db_passwords: "{{ raw_passwords | map('register_secret') | list }}"

Use the :ansplugin:`ansible.builtin.mask_secrets#filter` filter to redact registered secrets from a string yourself. This is useful when you write output somewhere Ansible does not control, such as a file on the managed node or a message sent to an external service:

.. code-block:: yaml+jinja

    - name: Write a sanitized copy of a command's output
      ansible.builtin.copy:
        content: "{{ command_result.stdout | mask_secrets }}"
        dest: /var/log/deploy-summary.log

    - name: Use a custom placeholder
      ansible.builtin.debug:
        msg: "{{ 'token=' ~ api_token | mask_secrets(mask_placeholder='***') }}"

.. _secret_masking_no_log:

How masking changes ``no_log``
==============================

Before ``ansible-core`` 2.22, a module option declared with ``no_log: true`` had its value replaced with the string ``VALUE_SPECIFIED_IN_NO_LOG_PARAMETER`` in the module result. This meant that a task could not register the result and use the real value in a later task.

Starting with ``ansible-core`` 2.22, the real value is kept in the module result and is registered as a secret instead.
The value is masked in callback output and module logs, but a registered result still holds the true value:

.. code-block:: yaml+jinja

    - name: Create a user with a generated password
      ansible.builtin.user:
        name: deploy
        password: "{{ generated_hash }}"
      register: user_result

    - name: The password option is masked in output but is intact in the registered result
      ansible.builtin.assert:
        that:
          - user_result.invocation.module_args.password == generated_hash

The ``no_log`` task keyword is unchanged. Setting ``no_log: true`` on a task or play still hides the entire task result from callbacks, and is still the right choice when a task's output could contain secrets in a form that masking cannot recognize.

.. _secret_masking_length_rules:

Secret length rules
===================

Masking works by searching output for the registered strings, so very short values would cause false matches all over the output. Ansible applies the following rules based on the length of the value:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Length
     - Behavior
   * - Fewer than 4 characters
     - Ignored. The value is not registered and is never masked.
   * - 4 to 6 characters
     - Registered, but only masked when the match sits on a word boundary. The character before and after the match must be a non-alphanumeric character, or the match must be at the start or end of the text. For example, a secret of ``abcd`` is masked in ``password=abcd`` but not in ``abcdef``.
   * - 7 to 1024 characters
     - Registered and masked wherever the value appears.
   * - More than 1024 characters
     - Trimmed to the first 1024 characters before registration. Only that leading portion is masked, any remainder of the value is left as is in the output.

Only string values can be registered. Booleans and ``None`` are never registered. Numbers are registered only in the specific cases noted above, such as numeric values in a vault-encrypted file, where they are registered as their string form.

Limitations
===========

Masking is a safety net for output that Ansible controls, not a replacement for handling secrets carefully. Be aware of the following limits:

* **Only exact matches are masked.**
* **Short values are silently ignored.**
* **Output that bypasses Ansible is not masked.**
* **Log messages from other Python libraries are not masked.**
* **Persistent connection logging is not masked.**
* **Callback plugins that opt in to masking are trusted.**
* **Fact and inventory caches are not masked.**
* **Modules only know the secrets in their input.**
* **Secrets are not shared between running workers.**
* **Connection plugins may show raw module output.**

A transformed copy of a secret, such as a base64 encoded, URL encoded, hashed, or upper-cased version, is a different string.
It is not masked unless it is registered as well.

Values shorter than 4 characters are never registered, and this happens without any warning or error.
This applies to values registered implicitly, such as a ``no_log`` module option, a plugin option marked ``secret: true``, or a prompt input, as well as to values passed to the ``register_secret`` filter.
Ansible stays silent so that existing content which sets short values for these options keeps working, but those values are not treated as secrets and appear in output unmasked.
See :ref:`secret_masking_length_rules` for the full length rules.

Anything a module writes to a file on the managed node, a plugin prints directly to standard output, or a task sends to an external service does not pass through a masked boundary.
Use the ``mask_secrets`` filter, or the developer API described in :ref:`developing_secret_masking`, if you need to sanitize such output.

The ``log_path`` log file is configured through the standard Python ``logging`` module on the root logger, so any Python library that Ansible or a plugin imports and that logs at ``INFO`` level or above writes into the same file.
Only the messages that Ansible itself writes through ``Display`` are masked.
Messages logged by other libraries, such as an HTTP client that logs request headers, reach the file unmasked.

The ``persistent_log_messages`` option used by network connection plugins logs every interaction from the separate ``ansible-connection`` process.
That process does not receive the secrets registered by the controller, so passwords and other sensitive configuration sent over the connection are written to the log in plain text.
Only enable this option while debugging and treat the resulting log as sensitive.

A callback plugin that declares ``ANSIBLE_SUPPORTS_MASKING = True`` receives unmasked task results and is responsible for masking any output it writes outside of ``Display``.
Review third-party callbacks that set this attribute before relying on them with sensitive data.

Cache plugins write the real values of facts and cached inventory to disk or an external service, since caching is not an output boundary.
If a secret can end up in a fact, treat the cache location as sensitive or avoid caching that data.

The controller only sends a module the registered secrets that appear in the module's own options.
A module that reads or derives a sensitive value some other way, such as from a file on the managed node or from an API it calls, does not know that value is a secret and does not mask it in its logs, even if the same value has been registered on the controller.
The value is still masked once the result reaches the controller. Module authors can register such values themselves, see :ref:`developing_secret_masking`.

Ansible runs tasks in worker processes forked from the controller.
A secret registered inside a worker, for example by a lookup or an action plugin, is sent back to the controller process only and is only inherited by workers forked after that point.
Workers that are already running for other hosts do not learn about it, so output from those hosts in the same task may still show the value.
Later tasks inherit the secret as expected.

A secret that a module registers during its run travels back to the controller inside the module's raw JSON result, and it is only registered on the controller once that result is processed.
A connection plugin that displays the raw standard output or standard error of the module, for example at high verbosity, shows that JSON before the new secret is known and so shows the value unmasked.
Secrets the module received in its options are already registered and are masked in that output.
The connection plugins shipped with ``ansible-core`` only show raw module output when :envvar:`ANSIBLE_DEBUG` is enabled.
Third-party connection plugins may not have this protection, so check how a plugin handles raw output before relying on masking with it.

.. seealso::

   :ref:`playbooks_vault`
       Encrypting sensitive data at rest with Ansible Vault
   :ref:`keep_secret_data`
       Hiding an entire task result with ``no_log``
   :ref:`logging`
       Logging Ansible output
   :ref:`developing_secret_masking`
       The secret masking API for module and plugin developers
