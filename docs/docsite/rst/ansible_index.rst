.. _ansible_documentation:
..
   This is the index file for Ansible the package. It gets symlinked to index.rst by the Makefile

Ansible Documentation
=====================

Welcome to Ansible community documentation!
This documentation covers the version of Ansible noted in the upper left corner of this page.
We maintain multiple versions of Ansible and of the documentation, so please be sure you are using the version of the documentation that covers the version of Ansible you're using.
For recent features, we note the version of Ansible where the feature was added.

Ansible releases a new major release approximately twice a year.
The core application evolves somewhat conservatively, valuing simplicity in language design and setup.
Contributors develop and change modules and plugins, hosted in collections, much more quickly.

.. toctree::
   :maxdepth: 2
   :caption: Ansible getting started

   getting_started/index
   getting_started_ee/index

.. toctree::
   :maxdepth: 2
   :caption: Installation, Upgrade & Configuration

   installation_guide/index
   porting_guides/porting_guides

.. toctree::
   :maxdepth: 2
   :caption: Using Ansible

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
   :caption: Contributing to Ansible

   community/index
   community/contributions_collections
   community/contributions
   community/advanced_index
   dev_guide/style_guide/index

.. toctree::
   :maxdepth: 2
   :caption: Extending Ansible

   dev_guide/index

.. toctree::
   :glob:
   :maxdepth: 1
   :caption: Common Ansible Scenarios

   scenario_guides/cloud_guides

.. toctree::
   :maxdepth: 2
   :caption: Network Automation

   network/getting_started/index
   network/user_guide/index
   network/dev_guide/index

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

   roadmap/ansible_roadmap_index.rst
   roadmap/ansible_core_roadmap_index.rst
