.. _logging:

**********************
Logging Ansible output
**********************

By default, Ansible sends output about plays, tasks, and module arguments to your screen (STDOUT) on the control node. If you want to capture Ansible output in a log, you have three options:

* To save Ansible output in a single log on the control node, set the ``log_path`` :ref:`configuration file setting <intro_configuration>`. You may also want to set ``display_args_to_stdout``, which helps to differentiate similar tasks by including variable values in the Ansible output.
* To save Ansible output in separate logs, one on each managed node, set the ``no_target_syslog`` and ``syslog_facility`` :ref:`configuration file settings <intro_configuration>`.
* To save Ansible output to a secure database, use AWX or :ref:`Red Hat Ansible Automation Platform <ansible_platform>`. You can then review history based on hosts, projects, and particular inventories over time, using graphs and/or a REST API.

Protecting sensitive data with ``no_log``
=========================================

If you save Ansible output to a log, you expose any secret data in your Ansible output, such as passwords and usernames. To keep sensitive values out of your logs, mark tasks that expose them with the ``no_log: True`` attribute. However, the ``no_log`` attribute does not affect debugging output, so be careful not to debug playbooks in a production environment. See :ref:`keep_secret_data` for an example.

Masking registered secrets
==========================

Starting with ``ansible-core`` 2.22, Ansible also masks known secrets in the output it writes to the screen and to the ``log_path`` log file. Values such as vault-encrypted variables, ``no_log`` module options, prompted passwords, and any value you register with the ``register_secret`` filter are replaced with ``$REDACTED$`` in the log. Masking applies to output that Ansible controls and does not cover every way a secret can reach a log, so it complements ``no_log`` rather than replacing it. In particular, messages that other Python libraries write to ``log_path`` through the standard ``logging`` module are not masked. See :ref:`playbooks_secret_masking` for what is masked, what is registered automatically, and the limitations.
