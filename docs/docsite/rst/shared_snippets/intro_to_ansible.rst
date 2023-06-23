Introduction to Ansible
-----------------------

Ansible is an open-source automation platform that allows IT professionals to automate various areas of their domain, for example:

* repetitive tasks
* system configuration
* software deployments
* continuous deployments
* zero downtime rolling updates

Users can write simple, human-readable automation scripts called playbooks. Those playbooks utilize a declarative approach in the form of Ansible modules to describe the desired state of a remote or local system (a managed host) that Ansible should ensure.

Ansible is decentralized in a sense that it relies on your existing OS credentials to control access to remote machines. And if needed, Ansible can easily connect with Kerberos, LDAP, and other centralized authentication management systems.

The following are some of the key strengths of Ansible automation platform:

* agent-less architecture: no need for agents or additional software to be installed on managed hosts. This reduces maintenance overhead.

* simplicity: Ansible features a minimum of moving parts, uses YAML syntax for its playbooks and leverages SSH/WinRM protocols to establish secure connections to execute tasks remotely.

* scalability and flexibility: modular design enables users to quickly and easily scale from one managed host to many. Support for wide range of operating systems, cloud platforms and network devices make Ansible also a very flexible automation platform.

* idempotence and predictability: when the managed host is in the correct state, running the same playbook multiple times does no changes.

Ansible releases a new major release approximately twice a year. The core application (`ansible-core`) evolves somewhat conservatively, valuing simplicity in language design and setup. Contributors develop and change modules and plugins hosted in collections since version 2.10 more quickly.
