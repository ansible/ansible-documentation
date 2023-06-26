.. _introduction_execution_environments:

######################################
Introduction to execution environments
######################################

Ansible execution environments aim to resolve complexity issues and provide all the benefits you can get from containerization.

Reducing complexity
===================

There are three main areas where EEs can reduce complexity: software dependencies, portability, and content separation.

Dependencies
------------

Software applications typically have dependencies.
It can be software libraries, configuration files or other services, to name a few, and Ansible, being an exceptional automation tool, is not an exception in terms of the mentioned.

Traditionally, application dependencies are installed by administrators on top of an operating system using packaging management tools like RPM or Python-pip.

The major drawback of such approach is that an application might require versions of dependencies different from those provided by default.

In case of Ansible, a typical installation consists of ``ansible-core`` and a set of Ansible collections.

At present, there are more than a hundred collections included in the Ansible package and hundreds more are available on Ansible Galaxy and Automation Hub for manual installation.
Many of them have dependencies for their plugins, modules, roles and playbooks they provide.

The Ansible collections can depend on the following pieces of software and their versions:

* ``ansible-core``
* Python
* Python packages
* system packages
* other Ansible collections

The dependencies have to be installed and sometimes can conflict with each other.

One way to **partially** resolve dependency issue is to use Python virtual environments on Ansible control node.
However, applied to Ansible, it has drawbacks and natural limitations.

Portability
-----------

An Ansible user writes content for Ansible locally and wants to leverage the container technology to make your automation runtimes portable, shareable and easily deployable to testing and production environments.

Content separation
------------------

In situations when there is an Ansible control node or a tool like Ansible AWX/Controller used by several users, they might want their content be separated to avoid configuration and dependency conflicts.

Ansible tooling for EEs
=======================

Projects in the Ansible ecosystem also provide lots of tooling that you can use with EEs, such as:

* `Ansible Builder <https://ansible-builder.readthedocs.io/en/stable/>`_
* `Ansible Navigator <https://ansible-navigator.readthedocs.io/>`_
* `Ansible AWX <https://docs.ansible.com/automation-controller/latest/html/userguide/execution_environments.html#use-an-execution-environment-in-jobs>`_
* `Automation controller <https://docs.ansible.com/automation-controller/latest/html/userguide/execution_environments.html#use-an-execution-environment-in-jobs>`_
* `Ansible Runner <https://ansible-runner.readthedocs.io/en/stable/>`_
* VS Code `Ansible <https://marketplace.visualstudio.com/items?itemName=redhat.ansible>`_ and `Dev Containers <https://code.visualstudio.com/docs/devcontainers/containers>`_ extensions

Ready to get started with EEs?
Proceed to :ref:`Setting up your environment<setting_up_environment>`.
