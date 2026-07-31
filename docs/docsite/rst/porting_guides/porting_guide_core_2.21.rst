
.. _porting_2.21_guide_core:

*******************************
Ansible-core 2.21 Porting Guide
*******************************

This section discusses the behavioral changes between ``ansible-core`` 2.20 and ``ansible-core`` 2.21.

It is intended to assist in updating your playbooks, plugins,
and other parts of your Ansible infrastructure so they will work with this version of Ansible.

Review this page and the
`ansible-core Changelog for 2.21 <https://github.com/ansible/ansible/blob/stable-2.21/changelogs/CHANGELOG-v2.21.rst>`_
to understand necessary changes.

This document is part of a collection on porting.
The complete list of porting guides can be found at :ref:`porting guides <porting_guides>`.

.. contents:: Topics

.. _2.21_introduction:

Introduction
============

No notable changes

.. _2.21_playbook:

Playbook
========

No notable changes

.. _2.21_engine:

Engine
======

No notable changes

.. _2.21_plugin_api:

Plugin API
==========

.. _2.21_command_line:

Command Line
============

No notable changes

.. _2.21_deprecated:

Deprecated
==========

Failure inference from non-zero ``rc``
--------------------------------------

Failure inference for modules and actions that return a non-zero ``rc`` value and no ``failed`` value is deprecated.
Modules and actions may use any logic desired to determine failure (including consulting ``rc``), but failures must be explicitly communicated in the task result by setting ``failed`` true, or via methods that do so implicitly, such as ``fail_json`` or raising an unhandled error.
Runtime deprecation warnings will be issued in release 2.22 when a deprecated failure inference occurs.
When failure inference is removed in future releases, the ``rc`` key will receive no special attention during task result processing.

.. _2.21_modules:

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

No notable changes

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
