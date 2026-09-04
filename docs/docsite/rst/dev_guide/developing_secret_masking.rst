.. _developing_secret_masking:

*******************************************
Handling secrets in modules and plugins
*******************************************

.. versionadded:: 2.22

``ansible-core`` 2.22 adds a secret masking API that modules and plugins can use to register sensitive values.
Any registered value is replaced with ``$REDACTED$`` wherever Ansible writes output, without changing the value itself.
This page describes the API, how registered secrets move between the controller, its worker processes, and the managed node, and what you must do in callback plugins and plugin configuration to take part in masking.

For the user-facing behavior, including which values Ansible registers automatically and the length rules for secrets, see :ref:`playbooks_secret_masking`.

.. contents::
   :local:

How masking works
=================

Ansible keeps a process-wide registry of secret strings. Every place that Ansible writes output, referred to as an *egress boundary*, runs the text through the registry and replaces any registered secret with the placeholder. The boundaries are:

* The ``Display`` object on the controller, which covers the screen, the ``log_path`` log file, warnings, deprecation messages, errors, and tracebacks.
* Task results handed to callback plugins that do not declare ``ANSIBLE_SUPPORTS_MASKING``.
* ``AnsibleModule.log()`` in Python modules and the ``Ansible.Basic`` logging in PowerShell modules, which write to syslog and the Windows Event Log on the managed node.

Registration is append-only and non-destructive. Registering a value does not change it, and code that already holds the value keeps working with it. Secrets are never removed from the registry for the life of the process.

.. note::
   The ``log_path`` log file is a handler on the Python root logger. Only messages that Ansible writes through ``Display`` are masked before they reach it. Messages that a plugin, or a library it imports, emits with the standard ``logging`` module are written to the file unmasked. Pass such messages through ``mask_secrets()`` before logging them, or avoid logging sensitive data with ``logging`` at all.

Secrets registered in a worker process, such as an action, connection, lookup, or filter plugin running inside a forked worker, are sent back to the controller together with the worker's results and registered there. Secrets registered inside a module on the managed node are returned to the controller as part of the module result and registered there as well. In both cases the secret is masked in every later task, not only in the task that registered it.

In the other direction, the controller passes any registered secrets that appear in a module's arguments to the module, so that the module-side masking in ``AnsibleModule.log()`` and ``Ansible.Basic`` also covers them. Secrets that are not present in the module arguments are not sent to the managed node. A module that obtains a sensitive value another way, such as reading it from a file or receiving it from an API, must register the value itself for module-side masking to cover it, even if the controller already knows that value.

Secrets that a module registers during its run are returned inside the module's raw JSON result and are only registered on the controller when that result is processed. Connection plugin authors must audit any code that displays the raw standard output or standard error of a module, since that text contains the new secrets in plain text before the controller knows about them. The connection plugins shipped with ``ansible-core`` only display raw module output when ``ANSIBLE_DEBUG`` is enabled. Gate such output the same way, or do not display it at all.

Propagation from a worker to the controller happens when the worker sends its results, and only workers forked after that point inherit the new secret. Workers that are already running, such as those executing the same task for other hosts, do not see it. If a plugin needs a value masked across every host in the current task, register it on the controller before the task runs, for example in a vars plugin or through the ``register_secret`` filter in an earlier task.

.. note::
   Masking works by searching output for the exact registered string. See :ref:`playbooks_secret_masking` for the minimum and maximum secret lengths and the word boundary rule that applies to short secrets. Register the secret in every form that could appear in output. A base64 encoded or URL encoded copy of a registered secret is a different string and is not masked.

The ``ansible.module_utils.secrets`` API
========================================

The ``ansible.module_utils.secrets`` module is the public API for working with secrets. It is available to modules, module utilities, and all controller-side plugins.

.. code-block:: python

    from ansible.module_utils.secrets import register_secret, register_secrets, mask_secrets

``register_secret(value)``
  Register a single string as a secret and return it unchanged. The return value makes it convenient to wrap an expression in place, for example ``token = register_secret(response['token'])``.

``register_secrets(values)``
  Register every string in an iterable. Use this when you have several values to register at once.

``mask_secrets(value, *, mask_placeholder='$REDACTED$')``
  Return a copy of ``value`` with every registered secret replaced by ``mask_placeholder``. Use this when you write text to a destination that is not an Ansible egress boundary, such as a file, an external logging system, or a message queue.

All three functions expect Python ``str`` values. Convert bytes with ``to_text()`` before registering them. Values shorter than the minimum secret length are silently ignored by ``register_secret()`` and ``register_secrets()``.

Registering secrets in a module
-------------------------------

Values for options declared with ``no_log: True`` in the ``argument_spec`` are registered automatically when ``AnsibleModule`` validates the arguments. Register any other sensitive value that your module discovers at run time, such as a token returned by an API or a password read from a file on the managed node, as soon as you have it:

.. code-block:: python

    from ansible.module_utils.basic import AnsibleModule
    from ansible.module_utils.secrets import register_secret


    def main():
        module = AnsibleModule(
            argument_spec=dict(
                username=dict(type='str', required=True),
                password=dict(type='str', required=True, no_log=True),  # registered automatically
            ),
        )

        session = login(module.params['username'], module.params['password'])

        # The token is a new secret discovered by the module. Register it so it is masked
        # in the module log, the callback output, and any later task on the controller.
        token = register_secret(session['token'])

        # The real value is still returned so it can be used by later tasks. It is only
        # masked when written to output.
        module.exit_json(changed=False, token=token)


    if __name__ == '__main__':
        main()

There is no need to strip the value from the result. The result keeps the real value, and the controller masks it when a callback or ``Display`` writes it out.

.. note::
   On ``ansible-core`` versions before 2.22, ``no_log`` values are removed from the module result and replaced with ``VALUE_SPECIFIED_IN_NO_LOG_PARAMETER``, and are stripped from module logs. The secrets API is not available on those versions.

The ``AnsibleModule.log()`` method masks its message and the ``log_args`` values before writing to syslog. The module invocation log entry always replaces ``no_log`` options with ``$REDACTED$``, regardless of the value's length, and masks any other registered secret it contains.

Modules that respawn under a different Python interpreter keep the secrets that were passed in from the controller, and any secret registered in the respawned process is returned to the controller as normal.

Registering secrets in a plugin
-------------------------------

The same functions work in every controller-side plugin type. This example is a lookup plugin that reads a credential from an external service and registers it before returning it:

.. code-block:: python

    from ansible.module_utils.secrets import register_secret
    from ansible.plugins.lookup import LookupBase
    from ansible.utils.display import Display

    display = Display()


    class LookupModule(LookupBase):

        def run(self, terms, variables=None, **kwargs):
            self.set_options(var_options=variables, direct=kwargs)

            results = []
            for term in terms:
                value = fetch_credential(term)
                results.append(register_secret(value))

                # Display output is a masked boundary, so this prints the placeholder.
                display.vvv(f"fetched credential for {term}: {value}")

            return results

For plugin options that are always sensitive, prefer marking the option with ``secret: true`` in the plugin documentation instead of registering the value by hand. See :ref:`plugin_config_secret`.

Masking output you write yourself
---------------------------------

Anything you write outside of an egress boundary is not masked. Call ``mask_secrets()`` before writing:

.. code-block:: python

    from ansible.module_utils.secrets import mask_secrets

    with open('/var/log/my_plugin.log', 'a') as fd:
        fd.write(mask_secrets(f"request completed: {response_text}\n"))

Deprecated helpers
------------------

The following helpers are replaced by automatic masking and are deprecated:

* ``ansible.module_utils.basic.heuristic_log_sanitize()`` is deprecated and will be removed in ``ansible-core`` 2.25.
* ``ansible.module_utils.common.parameters.remove_values()`` and ``sanitize_keys()`` are deprecated and will be removed in ``ansible-core`` 2.25.
* The ``live`` argument of ``ansible.utils.cmd_functions.run_cmd()`` is deprecated and will be removed in ``ansible-core`` 2.25.

Modules that called ``remove_values()`` or ``sanitize_keys()`` on their results, or that strip ``no_log`` values from a result before returning it, no longer need to. Remove those calls and return the real values.

The ``live`` argument of ``run_cmd()`` writes subprocess output directly to standard output, which bypasses masking. Run the subprocess yourself if you need to stream its output, and mask it with ``mask_secrets()``.

The heuristics that these helpers applied are gone as well. ``AnsibleModule.log()`` no longer rewrites password-like text such as ``user:password@host`` in URLs, and ``run_command()`` no longer replaces password-like arguments such as ``--password=...`` with ``********`` in the ``cmd`` value of a failure result. Only registered secrets are masked. If your module passes a secret on the command line or embeds one in a URL and that secret is not a ``no_log`` option, register it with ``register_secret()`` before use.

PowerShell and C# modules
=========================

The ``Ansible.Secrets`` C# module utility provides the same API for Windows modules. Import it with ``#AnsibleRequires`` and use the static ``Ansible.Secrets.SecretMasker`` class:

.. code-block:: powershell

    #!powershell

    #AnsibleRequires -CSharpUtil Ansible.Basic
    #AnsibleRequires -CSharpUtil Ansible.Secrets

    $spec = @{
        options = @{
            username = @{ type = 'str'; required = $true }
            password = @{ type = 'str'; required = $true; no_log = $true }  # registered automatically
        }
    }
    $module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

    $session = Connect-MyService -Username $module.Params.username -Password $module.Params.password

    # Register the discovered token so it is masked in the Event Log and on the controller.
    [Ansible.Secrets.SecretMasker]::RegisterSecret($session.Token)

    # Mask a string yourself before writing it somewhere that is not an Ansible boundary.
    $summary = [Ansible.Secrets.SecretMasker]::MaskString("Connected with token $($session.Token)")
    Set-Content -Path C:\logs\my_module.log -Value $summary

    $module.Result.token = $session.Token
    $module.ExitJson()

The ``SecretMasker`` class exposes:

``RegisterSecret(string secret)`` and ``RegisterSecret(SecureString secret)``
  Register a value. Prefer the ``SecureString`` overload when you already hold the value as a ``SecureString``, so the plain text is not exposed to PowerShell AMSI notifications.

``MaskString(string value)`` and ``MaskString(string value, string maskPlaceholder)``
  Return a copy of ``value`` with registered secrets replaced by ``$REDACTED$`` or the placeholder you supply.

The length rules match the Python implementation. ``Ansible.Basic`` registers ``no_log`` option values automatically, masks messages written through its event logging, and returns any newly registered secrets to the controller when the module exits.

.. _plugin_config_secret:

Marking plugin configuration options as secret
==============================================

Plugin configuration options can be marked with ``secret: true``. When a marked option is resolved, its value is registered as a secret regardless of the source that set it: an environment variable, an ``ansible.cfg`` entry, an Ansible variable, a command line option, or a direct argument to the plugin.

.. code-block:: yaml

    options:
      api_token:
        description: Token used to authenticate to the service.
        type: str
        secret: true
        env:
          - name: MYCOLLECTION_API_TOKEN
        vars:
          - name: mycollection_api_token

``secret`` is only supported for options of type ``str``, ``string``, and ``list``. For a ``list`` option, each string element is registered and non-string elements are ignored. Declaring ``secret: true`` on an option of any other type is an error when the plugin's configuration is loaded, so the plugin fails to load rather than silently leaving the value unmasked.

``secret`` is not supported on ``suboptions``. Sub-option definitions are documentation only and are not processed by the configuration manager, so there is no point at which their values could be registered. If a sub-option holds a sensitive value, register it in the plugin with ``register_secret()`` after reading the option.

The ``ansible-core`` connection and become plugins use this keyword for their password, private key, and passphrase options. When you write a plugin that accepts a password or token, mark the option as secret instead of relying on callers to add ``no_log`` or use ``register_secret``.

.. _developing_callbacks_masking:

Callback plugins and ``ANSIBLE_SUPPORTS_MASKING``
=================================================

Callback plugins receive task results that may contain registered secrets. To keep callbacks written before ``ansible-core`` 2.22 safe, the task queue manager masks every string in a result before handing it to a callback plugin, unless the plugin declares that it supports masking:

.. code-block:: python

    from ansible.plugins.callback import CallbackBase


    class CallbackModule(CallbackBase):
        CALLBACK_VERSION = 2.0
        CALLBACK_TYPE = 'stdout'
        CALLBACK_NAME = 'namespace.collection_name.my_callback'

        # Opt in to receiving unmasked task results.
        ANSIBLE_SUPPORTS_MASKING = True

Obtain the ``Display`` instance with ``Display()`` from ``ansible.utils.display``. It is a singleton, so every caller shares the same object and gets the same masking.

The attribute changes what ``CallbackTaskResult.result`` contains:

``ANSIBLE_SUPPORTS_MASKING = False`` (the default)
  Every string value in ``result.result``, including values nested in lists and dictionaries, is passed through ``mask_secrets()`` before the callback sees it. The callback cannot leak a registered secret through the result, but it also cannot see the real values.

``ANSIBLE_SUPPORTS_MASKING = True``
  ``result.result`` contains the real values. The callback is responsible for masking. Any output sent through ``Display()`` is masked automatically. Output written anywhere else, such as a file, a socket, or an HTTP request, should be passed through ``mask_secrets()`` first.

A callback that only ever writes through ``Display()`` can set the attribute to ``True`` with no other changes. A callback that serializes results elsewhere should mask them itself. The ``junit`` and ``tree`` callbacks shipped with ``ansible-core`` are examples of callbacks that write to files and call ``mask_secrets()`` on everything they write:

.. code-block:: python

    import json

    from ansible.module_utils.secrets import mask_secrets
    from ansible.plugins.callback import CallbackBase


    class CallbackModule(CallbackBase):
        CALLBACK_VERSION = 2.0
        CALLBACK_TYPE = 'notification'
        CALLBACK_NAME = 'namespace.collection_name.json_file'
        CALLBACK_NEEDS_ENABLED = True

        ANSIBLE_SUPPORTS_MASKING = True

        def v2_runner_on_ok(self, result):
            # The result contains real values, so mask the serialized form before writing it.
            with open('/var/log/ansible-results.jsonl', 'a') as fd:
                result_json = json.dumps(result.result, default=str)
                redacted_json = mask_secrets(result_json)
                fd.write(redacted_json + '\n')

The implicit masking of results for callbacks that do not set the attribute is a compatibility shim, kept only so that existing callback plugins do not break. It is not a complete solution. It masks the task result as a whole before the callback receives it, so it can only redact secrets present in the result at that point, and cannot cover values the callback derives, formats, or combines from elsewhere. Masking at each of the callback's own egress points outside of ``Display()`` means the values are masked at the moment they are written and nothing is missed.

The shim will be deprecated in a future release and then removed. Removal is tentatively planned for ``ansible-core`` 2.27, but that version is subject to change until an official deprecation warning is added. Update your callback plugins to set the attribute and mask their own output now so they keep redacting secrets when the shim is removed.

.. seealso::

   :ref:`playbooks_secret_masking`
       User guide for secret masking, including the length rules and limitations
   :ref:`developing_plugins`
       Developing plugins
   :ref:`developing_modules_general`
       Developing modules
   :ref:`developing_modules_general_windows`
       Developing Windows modules
