.. _get_started_inventory:

*********************
Building an inventory
*********************

Inventories organize managed nodes in centralized files that provide Ansible with system information and network locations.
Using an inventory file, Ansible can manage a large number of hosts with a single command.

To complete the following steps, you will need the IP address or fully qualified domain name (FQDN) of at least one host system.
For demonstration purposes, the host could be running locally in a container or a virtual machine.
You must also ensure that your public SSH key is added to the ``authorized_keys`` file on each host.

Continue getting started with Ansible and build an inventory as follows:

#. Open a terminal window in your ``ansible_quickstart`` directory.
#. Create a file named ``inventory.yaml`` and open it for editing.
#. Add a new ``myhosts`` group and specify the IP address or fully qualified domain name (FQDN) of each host with the ``ansible_host`` field.

   .. literalinclude:: yaml/inventory_example_vms.yaml
      :language: yaml

#. Verify your inventory.

   .. code-block:: bash

      ansible-inventory -i inventory.yaml --list

#. Ping the ``myhosts`` group in your inventory.

   .. code-block:: bash

      ansible myhosts -m ping -i inventory.yaml

   .. note::
      Pass the ``-u`` option with the ``ansible`` command if the username is different on the control node and the managed node(s).

   .. literalinclude:: ansible_output/ping_inventory_output.txt
      :language: text

Congratulations, you have successfully built an inventory.
Continue getting started with Ansible by :ref:`creating a playbook<get_started_playbook>`.

Tips for building inventories
=============================

* Ensure that group names are meaningful and unique. Group names are also case sensitive.
* Avoid spaces, hyphens, and preceding numbers (use ``floor_19``, not ``19th_floor``) in group names.
* Group hosts in your inventory logically according to their **What**, **Where**, and **When**.

  What
     Group hosts according to the topology, for example: db, web, leaf, spine.
  Where
     Group hosts by geographic location, for example: datacenter, region, floor, building.
  When
     Group hosts by stage, for example: development, test, staging, production.

Use metagroups
--------------

Create a metagroup that organizes multiple groups in your inventory with the following syntax:

.. code-block:: yaml

   metagroupname:
     children:

The following inventory illustrates a basic structure for a data center.
This example inventory contains a ``network`` metagroup that includes all network devices and a ``datacenter`` metagroup that includes the ``network`` group and all webservers.

.. literalinclude:: yaml/inventory_group_structure.yaml
   :language: yaml

Create variables
----------------

Variables set values for managed nodes, such as the IP address, FQDN, operating system, and SSH user, so you do not need to pass them when running Ansible commands.

Variables can apply to specific hosts.

.. literalinclude:: yaml/inventory_variables_host.yaml
   :language: yaml

Variables can also apply to all hosts in a group.

.. literalinclude:: yaml/inventory_variables_group.yaml
   :language: yaml

.. seealso::

   :ref:`intro_inventory`
       Learn more about inventories in ``YAML`` or ``INI`` format.
   :ref:`variables_in_inventory`
       Find out more about inventory variables and their syntax.
   :ref:`vault`
       Find out how to encrypt sensitive content in your inventory such as passwords and keys.
