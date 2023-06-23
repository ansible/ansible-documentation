.. _ansible_core_documentation:

..
   This is the index file for ansible-core. It gets symlinked to index.rst by the Makefile

***********************
Introduction to Ansible
***********************

Ansible is an open-source automation platform that allows IT professionals to automate various areas of their domain, for example:

* repetitive tasks
* system configuration
* software deployments
* continuous deployments
* zero downtime rolling updates

Users can write simple, human-readable automation scripts called playbooks. Those playbooks utilize a declarative approach in the form of Ansible modules to describe the desired state of a remote or local system (a managed host) that Ansible should ensure.

Ansible is decentralized is a sense that it relies on your existing OS credentials to control access to remote machines. And if needed, Ansible can easily connect with Kerberos, LDAP, and other centralized authentication management systems.

Ansible core (``ansible-core``) is the main building block and architecture for Ansible automation platform. Therefore you want to install the ``ansible-core`` package on the control node. From there you can manage and orchestrate the automation tasks across your entire infrastructure. Typically, ``ansible-core`` includes:

* ``ansible-playbook``, ``ansible-doc``, ``ansible``, and others CLI utilities
* Runtime engine for automation
* Fundamental set of Ansible modules, which ensure the desired state of your managed hosts
* Configuration files to define Ansible behavior and settings
* The Ansible language that uses YAML to create a set of rules for developing Ansible playbooks and includes functions such as conditionals, blocks, includes, loops, and other Ansible imperatives
* An architectural framework that allows extensions through Ansible collections

Ansible is designed around the following principles:

Agent-less architecture
    No need for agents or additional software to be installed on managed hosts. This reduces maintenance overhead.

Simplicity 
    Ansible features a minimum of moving parts, uses YAML syntax for its playbooks and leverages SSH/WinRM protocols to establish secure connections to execute tasks remotely.

Scalability and flexibility
    Modular design enables users to quickly and easily scale from one managed host to many. Support for wide range of operating systems, cloud platforms and network devices make Ansible also a very flexible automation platform.

Ansible releases a new major release approximately twice a year. The core application (`ansible-core`) evolves somewhat conservatively, valuing simplicity in language design and setup. Contributors develop and change modules and plugins hosted in collections since version 2.10 more quickly.


Ansible core documentation
==========================

This documentation covers the version of Ansible noted in the upper left corner of this page. We maintain multiple versions of Ansible and of the documentation, so please be sure you are using the version of the documentation that covers the version of Ansible you're using. For recent features, we note the version of Ansible where the feature was added.

You can learn more at `AnsibleFest <https://www.ansible.com/ansiblefest>`_, the annual event for all Ansible contributors, users, and customers hosted by Red Hat. AnsibleFest is the place to connect with others, learn new skills, and find a new friend to automate with.


.. toctree::
   :maxdepth: 2
   :caption: Ansible getting started

   getting_started/index

.. toctree::
   :maxdepth: 2
   :caption: Installation, Upgrade & Configuration

   installation_guide/index
   porting_guides/core_porting_guides

.. toctree::
   :maxdepth: 2
   :caption: Using Ansible Core

   inventory_guide/index
   command_guide/index
   playbook_guide/index
   vault_guide/index
   module_plugin_guide/index
   collections_guide/index
   os_guide/index
   tips_tricks/index

.. toctree::
   :maxdepth: 2
   :caption: Contributing to Ansible Core

   community/index
   community/contributions
   community/advanced_index
   dev_guide/style_guide/index

.. toctree::
   :maxdepth: 2
   :caption: Extending Ansible

   dev_guide/index

.. toctree::
   :maxdepth: 2
   :caption: Ansible Galaxy

   galaxy/user_guide.rst
   galaxy/dev_guide.rst

.. toctree::
   :maxdepth: 1
   :caption: Reference & Appendices

   collections/index
   collections/all_plugins
   reference_appendices/playbooks_keywords
   reference_appendices/common_return_values
   reference_appendices/config
   reference_appendices/general_precedence
   reference_appendices/YAMLSyntax
   reference_appendices/python_3_support
   reference_appendices/interpreter_discovery
   reference_appendices/release_and_maintenance
   reference_appendices/test_strategies
   dev_guide/testing/sanity/index
   reference_appendices/faq
   reference_appendices/glossary
   reference_appendices/module_utils
   reference_appendices/special_variables
   reference_appendices/tower
   reference_appendices/automationhub
   reference_appendices/logging

.. toctree::
   :maxdepth: 2
   :caption: Roadmaps

   roadmap/ansible_core_roadmap_index.rst
