.. _getting_started_index:

############################
Getting started with Ansible
############################

Ansible automates the management of remote systems and controls their desired state.
A basic Ansible environment has three main components:


Control node
   A system on which Ansible is installed.
   You run Ansible commands such as ``ansible`` or ``ansible-inventory`` on a control node.

Managed node
   A remote system, or host, that Ansible controls.

Inventory
   A list of managed nodes that are logically organized.
   You create an inventory on the control node to describe host deployments to Ansible.

.. image:: ../images/ansible_basic.svg
   :width: 400px
   :align: center
   :height: 200px
   :alt: Basic components of an Ansible environment include a control node, an inventory of managed nodes, and a module copied to each managed node.

.. toctree::
   :maxdepth: 1

   introduction
   get_started_ansible
   get_started_inventory
   get_started_playbook
   basic_concepts
