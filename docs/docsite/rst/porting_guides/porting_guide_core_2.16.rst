
.. _porting_2.16_guide_core:

*******************************
Ansible-core 2.16 Porting Guide
*******************************

This section discusses the behavioral changes between ``ansible-core`` 2.15 and ``ansible-core`` 2.16.

It is intended to assist in updating your playbooks, plugins and other parts of your Ansible infrastructure so they will work with this version of Ansible.

We suggest you read this page along with `ansible-core Changelog for 2.16 <https://github.com/ansible/ansible/blob/stable-2.16/changelogs/CHANGELOG-v2.16.rst>`_ to understand what updates you may need to make.

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


Deprecated
==========


Modules
=======



Modules removed
---------------



Deprecation notices
-------------------



Noteworthy module changes
-------------------------



Plugins
=======



Porting custom scripts
======================



Networking
==========

