
.. _porting_2.15_guide_core:

*******************************
Ansible-core 2.15 Porting Guide
*******************************

This section discusses the behavioral changes between ``ansible-core`` 2.14 and ``ansible-core`` 2.15.

It is intended to assist in updating your playbooks, plugins and other parts of your Ansible infrastructure so they will work with this version of Ansible.

We suggest you read this page along with `ansible-core Changelog for 2.15 <https://github.com/ansible/ansible/blob/stable-2.15/changelogs/CHANGELOG-v2.15.rst>`_ to understand what updates you may need to make.

This document is part of a collection on porting. The complete list of porting guides can be found at :ref:`porting guides <porting_guides>`.

.. contents:: Topics


Playbook
========

* Conditionals - due to mitigation of security issue CVE-2023-5764 in ansible-core 2.15.7,
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

Handlers
--------
As documented, if multiple handlers of a specific name have been defined, the last one added into the play is the one that is executed when being notified. Prior to ``ansible-core`` 2.15, this was not the case for handlers included dynamically into the play with the ``include_role`` task. This issue has been addressed in ``ansible-core`` 2.15, and users relying on the ``ansible-core`` 2.14 and older behavior may need to adjust their playbooks accordingly.

  As an example of the behavior change, consider the following:

  .. code-block:: yaml

     - include_role:
         name: foo
       vars:
         invocation: 1

     - block:
        - include_role:
            name: foo
          vars:
            invocation: 2
       when: inventory_hostname == "bar"

     - meta: flush_handlers

.. note::

  The example assumes there is a task within the role ``foo`` that notifies a handler named ``foo_handler`` within the role ``foo``.

.. note::

  The fact that different variables and/or their values are attached to ``include_role`` tasks including the same role makes them distinct roles.

.. note::

  The second invocation of the ``include_role`` task results in including tasks and handlers from the role regardless of the ``when`` conditional evaluation result. The ``when`` conditional is attached to the ``block`` wrapping the ``include_role`` task and as such the ``when`` conditional is applied to all tasks and handlers from the role after they are included into the play.

By the time the ``flush_handlers`` task runs, all hosts notified ``foo_handler`` within the first invocation of ``include_role``. Additionally the host ``bar`` (due to ``when`` restricting all other hosts) notified ``foo_handler`` again during the second invocation of ``include_role``.

On ``ansible-core`` 2.15, the last handler named ``foo_handler`` added into the play is from the second ``include_role`` invocation and therefore has ``when: inventory_hostname == "bar"`` attached to it, resulting in the handler being actually run only on the host ``bar`` and skipped on all other hosts. Consequently the notifications from the host ``bar`` have been de-duplicated.

On ``ansible-core`` 2.14 and older, ``foo_handler`` from the first invocation runs on all hosts. Additionally, ``foo_handler`` from the second invocation is run on the host ``bar`` again.


Command Line
============

* The return code of ``ansible-galaxy search`` is now 0 instead of 1 and the stdout is empty when results are empty to align with other ``ansible-galaxy`` commands.


Deprecated
==========

* Providing a list of dictionaries to ``vars:`` is deprecated in favor of supplying a dictionary.

  Instead of:

  .. code-block:: yaml

     vars:
       - var1: foo
       - var2: bar

  Use:

  .. code-block:: yaml

     vars:
       var1: foo
       var2: bar

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

No notable changes


Porting custom scripts
======================

No notable changes


Networking
==========

No notable changes
