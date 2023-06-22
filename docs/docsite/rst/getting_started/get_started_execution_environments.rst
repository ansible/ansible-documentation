.. _getting_started_execution_environments:

###########################################
Getting started with Execution Environments
###########################################

.. contents::
   :local:

.. _terminology:

Terminology
===========

Notions used in this document:

* **ansible-core**: you install it using ``pip install ansible-core``; includes command-line tools such as ``ansible-playbook`` and ``ansible-galaxy``, the Ansible language and a set of `builtin modules and plugins <https://docs.ansible.com/ansible/latest/collections/ansible/builtin/index.html>`_.
* **Ansible collections**: a format in which Ansible content is distributed that can contain playbooks, roles, modules and plugins.
* **Ansible package**: you install it using ``pip install ansible`` or an OS distribution package manager; it provides ansible-core and a big set of Ansible collections in the *batteries included* manner.
* **Ansible**: in the context of this document, is the Ansible package or ``ansible-core`` plus a set of collections installed on the Ansible control node.
* **Ansible control node**: the machine from which you run Ansible.
* **Container Runtime**: it is what you typically use ``podman`` or ``docker`` for running containers.
* **Execution environment**: is a container image providing a runtime environment for Ansible control node.

What is an execution environment?
=================================

Ansible, as a software application, can run in a container, thus, it can benefit from containerization the same as most other applications.

The Ansible automation execution environment (hereinafter, execution environment or EE) is a container image serving as Ansible control node.

The EE image contains:

* ansible-core
* ansible-runner
* none or more Ansible collections
* Python
* Python and system dependencies
* custom user needs

Tools you can use EEs with
--------------------------

You can use EEs with:

* `Ansible Builder <https://ansible-builder.readthedocs.io/en/stable/>`_
* `Ansible Navigator <https://ansible-navigator.readthedocs.io/>`_
* `Ansible AWX <https://docs.ansible.com/automation-controller/latest/html/userguide/execution_environments.html#use-an-execution-environment-in-jobs>`_
* `Automation controller <https://docs.ansible.com/automation-controller/latest/html/userguide/execution_environments.html#use-an-execution-environment-in-jobs>`_
* `Ansible Runner <https://ansible-runner.readthedocs.io/en/stable/>`_
* VS Code `Ansible <https://marketplace.visualstudio.com/items?itemName=redhat.ansible>`_ and `Dev Containers <https://code.visualstudio.com/docs/devcontainers/containers>`_ extensions

.. _ee_rationale:

Why execution environments were introduced
==========================================

The Ansible execution environments were introduced to resolve the following issues
and provide all benefits you can get from using containerization.

Dependencies
------------

Software applications typically have dependencies.
It can be software libraries, configuration files or other services, to name a few, and Ansible,
being an exceptional automation tool, is not an exception in terms of the mentioned.

Traditionally, application dependencies are installed by administrators on top of
an operating system using packaging management tools like RPM or Python-pip.

The major drawback of such approach is that an application might require versions
of dependencies different from those provided by default.

In case of Ansible, a typical installation consists of ansible-core and a set of Ansible collections.

At present, there are more than a hundred collections included in the Ansible package and
hundreds more are available on Ansible Galaxy and Automation Hub for manual installation.
Many of them have dependencies for their plugins, modules, roles and playbooks they provide.

The Ansible collections can depend on the following pieces of software and their versions:

* ansible-core
* Python
* Python packages
* system packages
* other Ansible collections

The dependencies have to be installed and sometimes can conflict with each other.

One way to **partly** resolve dependency issue is
to use Python virtual environments on Ansible control node.
However, applied to Ansible, it has drawbacks and natural limitations.

Portability
-----------

An Ansible user writes content for Ansible locally and wants to leverage the container technology
to make your automation runtimes portable, shareable and easily deployable to testing and production environments.

Content separation
------------------

In situations when there is an Ansible control node or a tool like Ansible AWX/Controller used by several users, they might want their content be separated to avoid configuration and dependency conflicts.

What to read next
=================

.. toctree::
   :maxdepth: 1

   get_started_build_and_test_ee
