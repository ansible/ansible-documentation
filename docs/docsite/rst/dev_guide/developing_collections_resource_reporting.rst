.. _resource_reporting:

******************
Resource reporting
******************

Ansible modules often interact with external systems such as clouds, hypervisors, and network controllers to manage resources that are not declared in your inventory.
Resource reporting gives you structured visibility into what your automation actually touches, even for resources that never appear in the inventory.

You can add resource reporting to your Ansible collection by creating a lightweight YAML query file that maps module return values to a standardized resource taxonomy.
Each entry uses a ``jq`` expression to extract resource metadata from module output.

.. contents::
   :local:
   :depth: 2

How resource reporting works
============================

Resource reporting uses a query file inside your collection to describe the resources that your modules manage.
When a module runs, the query file tells any consuming tool how to extract three pieces of information from the module return values:

* A human-readable resource name.
* Canonical facts that uniquely identify the resource for deduplication.
* Metadata that categorizes the resource using a standardized taxonomy.

The result is machine-readable documentation about what your modules manage.
For collection developers, resource reporting is like having excellent return value documentation that tools can consume automatically.
For users, it creates a consistent, unified picture of automation activity across different vendors and platforms.

.. _resource_reporting_taxonomy:

The normalized resource taxonomy
================================

The normalized resource taxonomy maps vendor-specific resource types to standard names.
For example, a VMware VM and an AWS EC2 instance are both type ``virtual_machine``.
An Azure load balancer and an F5 BIG-IP VIP are both type ``load_balancer``.

The taxonomy organizes resources into categories and device types.
When you write a query, set the ``facts.device_type`` field to the ``snake_case`` value from the tables below.

Compute
-------

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Resource
     - ``device_type`` value
   * - Virtual machines
     - ``virtual_machine``
   * - Containers (managed)
     - ``container``
   * - Hypervisors
     - ``hypervisor``
   * - Bare metal
     - ``bare_metal``
   * - Serverless functions
     - ``serverless_function``
   * - Auto scaling groups
     - ``auto_scaling_group``

Networking
----------

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Resource
     - ``device_type`` value
   * - Switches
     - ``switch``
   * - Routers
     - ``router``
   * - Firewalls
     - ``firewall``
   * - Load balancers
     - ``load_balancer``
   * - Virtual private clouds
     - ``vpc``
   * - Subnets
     - ``subnet``
   * - VPNs
     - ``vpn``
   * - Gateways
     - ``gateway``
   * - DNS services
     - ``dns_service``
   * - Wireless access points
     - ``wireless_access_point``
   * - SD-WAN
     - ``sd_wan``

Storage
-------

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Resource
     - ``device_type`` value
   * - Object storage
     - ``object_storage``
   * - Block storage
     - ``block_storage``
   * - File storage
     - ``file_storage``
   * - Archive storage
     - ``archive_storage``

Database
--------

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Resource
     - ``device_type`` value
   * - Relational (SQL)
     - ``database_relational``
   * - NoSQL
     - ``database_nosql``
   * - Data warehouse
     - ``data_warehouse``
   * - In-memory or cache
     - ``database_cache``

DevOps and app integration
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Resource
     - ``device_type`` value
   * - CI/CD platforms
     - ``ci_cd_platform``
   * - Container registries
     - ``container_registry``
   * - Message queues
     - ``message_queue``
   * - API endpoints
     - ``api_endpoint``

.. note::

   If your resource does not fit one of these standard types, open a topic on `the Ansible forum <https://forum.ansible.com/>`_ to propose a new device type.

.. _resource_reporting_query_file:

Adding resource reporting to a collection
=========================================

To add resource reporting to your collection, create a query file and write ``jq`` expressions that extract resource metadata from your module return values.

Creating the query file
-----------------------

Create the file ``extensions/audit/event_query.yml`` in your collection root directory.
This is the standard location for embedded query files that ship with your collection.

.. code-block:: text

   my_namespace/my_collection/
   ├── extensions/
   │   └── audit/
   │       └── event_query.yml
   ├── plugins/
   ├── meta/
   └── galaxy.yml

Writing the query
-----------------

The query file maps each module to a ``jq`` expression using the Fully Qualified Collection Name (FQCN) as the key.
The ``jq`` expression runs against the module return values and must output a JSON object with the following fields:

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Field
     - Requirement
     - Description
   * - ``name``
     - Required
     - A human-readable display name for the resource, for example a VM name or switch hostname.
   * - ``canonical_facts``
     - Required
     - A dictionary of facts that uniquely identify the resource and deduplicate it across job runs.
   * - ``facts``
     - Optional
     - Metadata for categorization. Must include ``device_type`` when present.

The following example shows a complete query file entry:

.. literalinclude:: yaml/event_query_vmware.yaml
   :language: yaml

.. _resource_reporting_canonical_facts:

Choosing canonical facts
^^^^^^^^^^^^^^^^^^^^^^^^

Select fields that are globally unique and stable for the life of the resource.

* **Recommended:** UUIDs, serial numbers, permanent MAC addresses.
* **Conditional:** Hostnames (if unique in the environment), IP addresses (static only).
* **Avoid:** Dynamic IPs, random session IDs.

.. literalinclude:: json/canonical_facts.json
   :language: json

Setting the device type
^^^^^^^^^^^^^^^^^^^^^^^

Map your resource to a standard ``device_type`` value from the :ref:`normalized resource taxonomy <resource_reporting_taxonomy>`.
You can optionally include a ``platform`` field to indicate the underlying platform, for example ``aws``, ``vmware``, or ``azure``.

.. literalinclude:: json/facts_device_type.json
   :language: json

.. _resource_reporting_examples:

Platform-specific examples
==========================

Different platforms require different querying strategies based on how their APIs return data.

VMware (flat structure)
-----------------------

VMware modules return a flat structure where the top-level key defines the node type.
Map directly to the returned keys.

.. literalinclude:: yaml/event_query_vmware.yaml
   :language: yaml

Azure (hierarchical structure)
------------------------------

Azure resources are hierarchical and use verbose resource IDs.
Because the full Azure resource ID contains the resource type, you can use a ``jq`` regex to dynamically capture and categorize it.

.. literalinclude:: yaml/event_query_azure.yaml
   :language: yaml

In this example, ``Microsoft.Compute`` in the resource ID is captured and lowercased to ``"compute"``.

AWS (implied types)
-------------------

AWS info modules often return a list of resources, so your ``jq`` expression must iterate over them.
The resource type is implied by the module you query rather than included in the resource ID.

.. literalinclude:: yaml/event_query_aws.yaml
   :language: yaml

To manage the mapping from AWS module to resource type, define a mapping dictionary in your expression:

.. literalinclude:: json/aws_type_mapping.json
   :language: json

.. _resource_reporting_module_matching:

Module matching rules
=====================

The query file uses module FQCNs as keys.
You can target modules with exact matches or wildcard patterns.

Exact match
-----------

Target a specific module.

.. literalinclude:: yaml/event_query_exact_match.yaml
   :language: yaml

Wildcard match
--------------

Target all modules in a collection.
Use this carefully because different modules return different data structures.

.. literalinclude:: yaml/event_query_wildcard_match.yaml
   :language: yaml

.. _resource_reporting_testing:

Testing your query
==================

Before publishing your collection, verify your ``jq`` expression against real module output.

1. Run a playbook with your module and capture the JSON output.
   Register the return value or run the module with ``-vvv`` to see the full output.

   .. literalinclude:: yaml/test_playbook_resource_reporting.yaml
      :language: yaml

2. Save the module output to a file and test your ``jq`` expression from the command line.

   .. code-block:: bash

      cat module_output.json | jq '{
        name: .instance.hw_name,
        canonical_facts: {
          uuid: .instance.hw_uuid
        },
        facts: {
          device_type: "virtual_machine"
        }
      }'

3. Validate that the output JSON contains a valid ``name`` string and non-empty ``canonical_facts``.

.. seealso::

   :ref:`developing_collections`
       Learn how to develop Ansible collections
   :ref:`collection_structure`
       Directories and files included in a collection
   `Ansible forum <https://forum.ansible.com/>`_
       Got questions? Need help? Want to share your ideas? Visit the Ansible forum
