
.. _porting_2.19_guide_core:

*******************************
Ansible-core 2.19 Porting Guide
*******************************

This section discusses the behavioral changes between ``ansible-core`` 2.18 and ``ansible-core`` 2.19.

It is intended to assist in updating your playbooks, plugins and other parts of your Ansible infrastructure so they will work with this version of Ansible.

We suggest you read this page along with `ansible-core Changelog for 2.19 <https://github.com/ansible/ansible/blob/stable-2.19/changelogs/CHANGELOG-v2.19.rst>`_ to understand what updates you may need to make.

This document is part of a collection on porting. The complete list of porting guides can be found at :ref:`porting guides <porting_guides>`.

.. contents:: Topics


Playbook
========

* Timeout waiting on privilege escalation (``become``) is now an unreachable error instead of a task error. Existing playbooks should be changed to replace ``ignore_errors`` with ``ignore_unreachable`` on tasks where timeout on ``become`` should be ignored.

  .. error::
    Timeout (12s) waiting for privilege escalation prompt:

Command Line
============

No notable changes


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

* The ``ssh`` connection plugin now supports using ``SSH_ASKPASS`` to supply passwords
  for authentication as an alternative to the ``sshpass`` program. The default is to use
  ``SSH_ASKPASS`` instead of ``sshpass``. This is controlled by the ``password_mechanism``
  configuration for the ``ssh`` connection plugin. To switch back to using ``sshpass``
  make one of the following changes:

  To your ``ansible.cfg`` file:

  .. code-block:: ini

     [ssh_connection]
     password_mechanism = sshpass

  By exporting an environment variable:

  .. code-block:: shell

     export ANSIBLE_SSH_PASSWORD_MECHANISM=sshpass

  By setting the following variable:

  .. code-block:: yaml

     ansible_ssh_password_mechanism: sshpass

Porting custom scripts
======================

No notable changes


Networking
==========

No notable changes
