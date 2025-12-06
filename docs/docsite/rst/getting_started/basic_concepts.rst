Ansible concepts
----------------

These concepts are common to all uses of Ansible. Understanding them will help
you navigate the documentation and build your first automation tasks.

Core concepts
=============

Below are the fundamental ideas behind how Ansible works:

* **Control node** – The machine from which you run Ansible commands and
  playbooks. It connects to managed hosts using SSH or other remote protocols.

* **Managed nodes** – The remote systems you want to configure or automate.
  Ansible does not require any agent to be installed on these machines.

* **Inventory** – A file (usually ``inventory`` or ``hosts``) that lists your
  managed nodes and groups them logically.

* **Modules** – Reusable units of work that Ansible executes on managed nodes.
  Examples include ``ping``, ``copy``, ``package``, and many more.

* **Tasks** – Individual actions executed by Ansible modules. Tasks run in
  the order they are written.

* **Playbooks** – YAML files that contain plays and tasks, describing the
  desired state of your systems.

* **Plays** – Mappings between a group of hosts and the tasks that should run
  on them.

Example
=======

The following simple playbook demonstrates a few of these concepts:

.. code-block:: yaml

   - name: Test connectivity to all servers
     hosts: all
     tasks:
       - name: Ping remote machines
         ansible.builtin.ping:

This example uses:

* an **inventory** containing your hosts,
* a **play** targeting the group ``all``,
* a **task** that uses the ``ping`` **module**.

These concepts form the building blocks of all Ansible automation.
