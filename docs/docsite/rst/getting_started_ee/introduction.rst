.. _introduction_execution_environment:

**************************************
Introduction to Execution Environments
**************************************

Ansible Execution Environments aim to resolve complexity issues and provide all the benefits you can get from containerization.

Reducing complexity
===================

There are three main areas where EEs can reduce complexity:

* software dependencies
* portability
* content separation

Dependencies
------------

Software applications typically have dependencies, and Ansible is no exception.
These dependencies can include software libraries, configuration files or other services, to name a few.

Traditionally, administrators install application dependencies on top of an operating system using packaging management tools such as RPM or Python-pip.
The major drawback of such an approach is that an application might require versions of dependencies different from those provided by default.
For Ansible, a typical installation consists of `ansible-core` and a set of Ansible collections.
Many of them have dependencies for the plugins, modules, roles and playbooks they provide.

The Ansible collections can depend on the following pieces of software and their versions:

* ``ansible-core``
* Python
* Python packages
* System packages
* Other Ansible collections

The dependencies have to be installed and sometimes can conflict with each other.

One way to **partially** resolve the dependency issue is to use Python virtual environments on Ansible control nodes.
However, applied to Ansible, virtual environments have drawbacks and natural limitations.

Portability
-----------

An Ansible user writes content for Ansible locally and wants to leverage the container technology to make their automation runtimes portable, shareable and easily deployable to testing and production environments.

Content separation
------------------

In situations when there is an Ansible control node or a tool such as Ansible AWX/Controller used by several users, they might want separate
their content to avoid configuration and dependency conflicts.

Ansible tooling for EEs
=======================

Projects in the Ansible ecosystem also provide several tools that you can use with EEs, such as:

* `Ansible Builder <https://ansible-builder.readthedocs.io/en/stable/>`_
* `Ansible Navigator <https://ansible-navigator.readthedocs.io/>`_
* `Ansible AWX <https://ansible.readthedocs.io/projects/awx/en/latest/userguide/execution_environments.html#use-an-execution-environment-in-jobs>`_
* `Ansible Runner <https://ansible-runner.readthedocs.io/en/stable/>`_
* `VS Code Ansible <https://marketplace.visualstudio.com/items?itemName=redhat.ansible>`_
* `Dev Containers extensions <https://code.visualstudio.com/docs/devcontainers/containers>`_

Ready to get started with EEs? Proceed to :ref:`setting_up_ee_environment`.
