Introduction to Ansible core
----------------------------

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
* Runtime engine for Ansible automation platform
* Fundamental set of Ansible modules, which ensure the desired state of your managed hosts
* Configuration files to define Ansible behavior and settings
* The Ansible language that uses YAML to create a set of rules for developing Ansible playbooks and includes functions such as conditionals, blocks, includes, loops, and other Ansible imperatives
* An architectural framework that allows extensions through Ansible collections

The following are some of the key strengths of Ansible automation platform:

* agent-less architecture: no need for agents or additional software to be installed on managed hosts. This reduces maintenance overhead.

* simplicity: Ansible features a minimum of moving parts, uses YAML syntax for its playbooks and leverages SSH/WinRM protocols to establish secure connections to execute tasks remotely.

* scalability and flexibility: modular design enables users to quickly and easily scale from one managed host to many. Support for wide range of operating systems, cloud platforms and network devices make Ansible also a very flexible automation platform.

* idempotence and predictability: when the managed host is in the correct state, running the same playbook multiple times does no changes.

Ansible releases a new major release approximately twice a year. The core application (`ansible-core`) evolves somewhat conservatively, valuing simplicity in language design and setup. Contributors develop and change modules and plugins hosted in collections since version 2.10 more quickly.