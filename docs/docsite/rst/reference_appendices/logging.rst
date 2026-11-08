.. _logging:

**********************
Logging Ansible output
**********************

By default, Ansible sends output about plays, tasks, and module arguments to your screen (STDOUT) on the control node. If you want to capture Ansible output in a log, you have three options:

* To save Ansible output in a single log on the control node, set the ``log_path`` :ref:`configuration file setting <intro_configuration>`. You may also want to set ``display_args_to_stdout``, which helps to differentiate similar tasks by including variable values in the Ansible output.
* To save Ansible output in separate logs, one on each managed node, set the ``no_target_syslog`` and ``syslog_facility`` :ref:`configuration file settings <intro_configuration>`.
* To save Ansible output to a secure database, use AWX or :ref:`Red Hat Ansible Automation Platform <ansible_platform>`. You can then review history based on hosts, projects, and particular inventories over time, using graphs and/or a REST API.

Color output
============

Ansible uses ANSI escape sequences to colorize command-line output. You can customize colors through the color-related configuration settings.

Named colors
------------

You can configure colors in ``ansible.cfg``:

.. code-block:: ini

   [colors]
   changed = bright green

Alternatively, use the corresponding environment variable:

.. code-block:: shell

   export ANSIBLE_COLOR_CHANGED="bright green"


Ansible supports these predefined color names:

* ``black``
* ``bright gray``
* ``blue``
* ``white``
* ``green``
* ``bright blue``
* ``cyan``
* ``bright green``
* ``red``
* ``bright cyan``
* ``purple``
* ``bright red``
* ``yellow``
* ``bright purple``
* ``dark gray``
* ``bright yellow``
* ``magenta``
* ``bright magenta``
* ``normal``

Some names produce the same ANSI color code:

* ``purple`` and ``magenta``
* ``bright purple`` and ``bright magenta``

256-color formats
-----------------

Ansible also supports the following formats:

* ``colorNNN`` specifies a color using a 256-color palette index. For example, ``color196``.
* ``rgbXYZ`` specifies a color using the RGB color cube. Each digit must be between ``0`` and ``5``. For example, ``rgb500``.
* ``grayNN`` specifies a grayscale color. For example, ``gray10``.

Examples:

* ``rgb000`` maps to palette index ``16``.
* ``rgb555`` maps to palette index ``231``.
* ``color196`` and ``rgb500`` refer to the same palette index.
* ``color231`` and ``rgb555`` refer to the same palette index.
* ``gray0`` maps to palette index ``232``.
* ``gray23`` maps to palette index ``255``.

The parser does not explicitly validate the numeric ranges for ``colorNNN`` or ``grayNN``. Use conventional palette indices from ``0`` to ``255`` and grayscale values from ``0`` to ``23``.

Terminal compatibility
----------------------

Color rendering depends on terminal emulator support for ANSI color sequences. The appearance of colors can vary between terminal implementations.


Protecting sensitive data with ``no_log``
=========================================

If you save Ansible output to a log, you expose any secret data in your Ansible output, such as passwords and usernames. To keep sensitive values out of your logs, mark tasks that expose them with the ``no_log: True`` attribute. However, the ``no_log`` attribute does not affect debugging output, so be careful not to debug playbooks in a production environment. See :ref:`keep_secret_data` for an example.

Masking registered secrets
==========================

Starting with ``ansible-core`` 2.22, Ansible also masks known secrets in the output it writes to the screen and to the ``log_path`` log file. Values such as vault-encrypted variables, ``no_log`` module options, prompted passwords, and any value you register with the ``register_secret`` filter are replaced with ``$REDACTED$`` in the log. Masking applies to output that Ansible controls and does not cover every way a secret can reach a log, so it complements ``no_log`` rather than replacing it. In particular, messages that other Python libraries write to ``log_path`` through the standard ``logging`` module are not masked. See :ref:`playbooks_secret_masking` for what is masked, what is registered automatically, and the limitations.
