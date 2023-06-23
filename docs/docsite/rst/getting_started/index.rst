.. _getting_started_index:

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

Ansible is decentralized in a sense that it relies on your existing OS credentials to control access to remote machines. And if needed, Ansible can easily connect with Kerberos, LDAP, and other centralized authentication management systems.

Ansible is designed around the following principles:

Agent-less architecture
    No need for agents or additional software to be installed on managed hosts. This reduces maintenance overhead.

Simplicity 
    Ansible features a minimum of moving parts, uses YAML syntax for its playbooks and leverages SSH/WinRM protocols to establish secure connections to execute tasks remotely.

Scalability and flexibility
    Modular design enables users to quickly and easily scale from one managed host to many. Support for wide range of operating systems, cloud platforms and network devices make Ansible also a very flexible automation platform.

Ansible releases a new major release approximately twice a year. The core application (`ansible-core`) evolves somewhat conservatively, valuing simplicity in language design and setup. Contributors develop and change modules and plugins hosted in collections since version 2.10 more quickly.


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
