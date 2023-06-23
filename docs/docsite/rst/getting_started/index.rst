.. _getting_started_index:

.. include:: ../shared_snippets/intro_to_ansible.rst

############################
Getting started with Ansible
############################

Ansible automates the management of remote systems and controls their desired state.
A basic Ansible environment has three main components:


Control node
   A system on which Ansible is installed.
   You run Ansible commands such as ``ansible`` or ``ansible-inventory`` on a control node.

Configuration file
   The ``ansible.cfg`` configuration file enables you to customize and set various aspects of Ansible behavior on the control node.

Inventory
   A list of remote systems (managed nodes) that are logically organized and which Ansible brings to the state that you need.
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
