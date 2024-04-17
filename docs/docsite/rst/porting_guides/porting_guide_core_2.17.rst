
.. _porting_2.17_guide_core:

*******************************
Ansible-core 2.17 Porting Guide
*******************************

This section discusses the behavioral changes between ``ansible-core`` 2.16 and ``ansible-core`` 2.17.

It is intended to assist in updating your playbooks, plugins and other parts of your Ansible infrastructure so they will work with this version of Ansible.

We suggest you read this page along with `ansible-core Changelog for 2.17 <https://github.com/ansible/ansible/blob/stable-2.17/changelogs/CHANGELOG-v2.17.rst>`_ to understand what updates you may need to make.

This document is part of a collection on porting. The complete list of porting guides can be found at :ref:`porting guides <porting_guides>`.

.. contents:: Topics


Playbook
========

No notable changes


Command Line
============

* Python 2.7 and Python 3.6 are no longer supported remote versions. Python 3.7+ is now required for target execution.


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

No notable changes


Porting custom scripts
======================

No notable changes


Networking
==========

No notable changes
