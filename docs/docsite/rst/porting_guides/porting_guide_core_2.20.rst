
.. _porting_2.20_guide_core:

*******************************
Ansible-core 2.20 Porting Guide
*******************************

This section discusses the behavioral changes between ``ansible-core`` 2.19 and ``ansible-core`` 2.20.

It is intended to assist in updating your playbooks, plugins,
and other parts of your Ansible infrastructure so they will work with this version of Ansible.

Review this page and the
`ansible-core Changelog for 2.20 <https://github.com/ansible/ansible/blob/stable-2.20/changelogs/CHANGELOG-v2.20.rst>`_
to understand necessary changes.

This document is part of a collection on porting.
The complete list of porting guides can be found at :ref:`porting guides <porting_guides>`.

.. contents:: Topics

.. _2.20_introduction:

Introduction
============

No notable changes

.. _2.20_playbook:

Playbook
========

Removed quote stripping in PowerShell operations
-------------------------------------------------

The PowerShell module utilities no longer attempt to remove quotes from paths when performing Windows operations like copying and fetching files. This should not affect normal playbooks unless a value is quoted too many times. If you have playbooks that rely on this automatic quote removal, you will need to adjust your path formatting.

.. _2.20_engine:

Engine
======

No notable changes

.. _2.20_plugin_api:

Plugin API
==========

Removed Features
----------------

The following previously deprecated features have been removed:

* The ``DEFAULT_TRANSPORT`` configuration option no longer supports the ``smart`` value that selected the default transport as either ``ssh`` or ``paramiko`` based on the underlying platform configuration.
* The ``vault`` and ``unvault`` filters no longer accept the deprecated ``vaultid`` parameter.
* The ``ansible-galaxy`` command no longer supports the v2 Galaxy server API. Galaxy servers hosting collections must support v3.
* The ``dnf`` and ``dnf5`` modules no longer support the deprecated ``install_repoquery`` option.
* The ``encrypt`` module utility no longer includes the deprecated ``passlib_or_crypt`` API.
* The ``paramiko`` connection plugin no longer supports the ``PARAMIKO_HOST_KEY_AUTO_ADD`` and ``PARAMIKO_LOOK_FOR_KEYS`` configuration keys, which were previously deprecated.
* The ``py3compat.environ`` call has been removed.
* Vars plugins that do not inherit from ``BaseVarsPlugin`` and define a ``get_vars`` method can no longer use the deprecated ``get_host_vars`` or ``get_group_vars`` fallback.
* The ``yum_repository`` module no longer supports the deprecated ``keepcache`` option.

Behavioral Changes
------------------

* The ``DataLoader.get_basedir`` method now returns an absolute path instead of a relative path. Plugin code that relies on relative paths may need adjustment.
* Argument spec validation now treats ``None`` values as empty strings for the ``str`` type for better consistency with pre-2.19 templating conversions.
* When using ``failed_when`` to suppress an error, the ``exception`` key in the result is now renamed to ``failed_when_suppressed_exception``. This prevents the error from being displayed by callbacks after being suppressed. If you have playbooks that check for the exception in the result, update them as follows:

.. code-block:: yaml+jinja

    # Before
    - command: /bin/false
      register: result
      failed_when: false

    - debug:
        msg: "Exception was: {{ result.exception }}"
      when: result.exception is defined

    # After
    - command: /bin/false
      register: result
      failed_when: false

    - debug:
        msg: "Exception was: {{ result.failed_when_suppressed_exception }}"
      when: result.failed_when_suppressed_exception is defined

.. _2.20_command_line:

Command Line
============

* Python 3.11 is no longer a supported control node version. Python 3.12+ is now required for running Ansible.
* Python 3.8 is no longer a supported remote version. Python 3.9+ is now required for target execution.

.. _2.20_deprecated:

Deprecated
==========

INJECT_FACTS_AS_VARS
--------------------

The ``INJECT_FACTS_AS_VARS`` configuration currently defaults to ``True``, but this is now deprecated and it will switch to ``False`` in Ansible 2.24.

When enabled, facts are available both inside the ``ansible_facts`` dictionary and as individual variables in the main namespace. In the ``ansible_facts`` dictionary, the ``ansible_`` prefix is removed from fact names.

You will receive deprecation warnings if you are accessing 'injected' facts. To prepare for the future default:

**Update your playbooks to use the ansible_facts dictionary:**

.. code-block:: yaml+jinja

    # Deprecated - will stop working in 2.24
    - debug:
        msg: "OS: {{ ansible_os_distribution }}"

    # Recommended - works in all versions
    - debug:
        msg: "OS: {{ ansible_facts['distribution'] }}"
        # Note: 'ansible_' prefix is removed inside ansible_facts

**Or explicitly enable the current behavior in your configuration:**

In your ``ansible.cfg`` file:

.. code-block:: ini

    [defaults]
    inject_facts_as_vars = True

By exporting an environment variable:

.. code-block:: shell

    export ANSIBLE_INJECT_FACT_VARS=True

Other Deprecations
------------------

* The ``vars`` internal variable cache will be removed in 2.24. This cache, once used internally, exposes variables in inconsistent states. The ``vars`` and ``varnames`` lookups should be used instead.
* Specifying ``ignore_files`` as a string in the ``include_vars`` module is deprecated. Use a list instead:

.. code-block:: yaml

    # Deprecated
    - include_vars:
        dir: vars/
        ignore_files: ".gitkeep"

    # Correct
    - include_vars:
        dir: vars/
        ignore_files: [".gitkeep"]

.. _2.20_modules:

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

* The ``include_vars`` module now raises an error if the ``extensions`` parameter is not specified as a list. Previously, non-list values were silently accepted.
* The ``include_vars`` module now raises an error if the ``ignore_files`` parameter is not specified as a list. Previously, string values were accepted but are now deprecated.
* The ``replace`` module now reads and writes files in text-mode as unicode characters instead of as bytes, and switches regex matching to unicode characters instead of bytes. This may affect playbooks that rely on byte-level operations.

Plugins
=======

Noteworthy plugin changes
-------------------------

No notable changes

Porting custom scripts
======================

No notable changes

Networking
==========

No notable changes
