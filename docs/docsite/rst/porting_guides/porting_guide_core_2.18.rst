
.. _porting_2.18_guide_core:

*******************************
Ansible-core 2.18 Porting Guide
*******************************

This section discusses the behavioral changes between ``ansible-core`` 2.17 and ``ansible-core`` 2.18.

It is intended to assist in updating your playbooks, plugins and other parts of your Ansible infrastructure so they will work with this version of Ansible.

We suggest you read this page along with `ansible-core Changelog for 2.18 <https://github.com/ansible/ansible/blob/stable-2.18/changelogs/CHANGELOG-v2.18.rst>`_ to understand what updates you may need to make.

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

* Python 3.10 is a no longer supported control node version. Python 3.11+ is now required for running Ansible.
* Python 3.7 is a no longer supported remote version. Python 3.8+ is now required for target execution.


Deprecated
==========

No notable changes


Modules
=======

No notable changes


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

* The ``ssh`` connection plugin now officially supports targeting Windows hosts. A
  breaking change has been made as part of this official support is the low level command
  execution done by plugins like ``ansible.builtin.raw`` and action plugins calling
  ``_low_level_execute_command`` is no longer wrapped with a ``powershell.exe`` wrapped
  invocation. These commands will now be executed directly on the target host using
  the default shell configuration set on the Windows host. This change is done to
  simplify the configuration required on the Ansible side, make module execution more
  efficient, and to remove the need to decode stderr CLIXML output. A consequence of this
  change is that ``ansible.builtin.raw`` commands are no longer be guaranteed to be
  run through a PowerShell shell and with the output encoding of UTF-8. To run a command
  through PowerShell and with UTF-8 output support, use the ``ansible.windows.win_shell``
  or ``ansible.windows.win_powershell`` module instead.

  .. code-block:: yaml

      - name: Run with win_shell
        ansible.windows.win_shell: Write-Host "Hello, Café"

      - name: Run with win_powershell
        ansible.windows.win_powershell:
          script: Write-Host "Hello, Café"


Porting custom scripts
======================

No notable changes


Networking
==========

No notable changes
