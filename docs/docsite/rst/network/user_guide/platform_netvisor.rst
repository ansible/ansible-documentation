.. _netvisor_platform_options:

**********************************
Pluribus NETVISOR Platform Options
**********************************

Pluribus NETVISOR Ansible is part of the `community.network <https://galaxy.ansible.com/ui/repo/published/community/network>`_ collection and only supports CLI connections today. ``httpapi`` modules may be added in future.
This page offers details on how to use ``ansible.netcommon.network_cli`` on NETVISOR in Ansible.

.. contents::
  :local:

Connections available
================================================================================

.. table::
    :class: documentation-table

    ====================  ==========================================
    ..                    CLI
    ====================  ==========================================
    Protocol              SSH

    Credentials           uses SSH keys / SSH-agent if present

                          accepts ``-u myuser -k`` if using password

    Indirect Access       by a bastion (jump host)

    Connection Settings   ``ansible_connection: ansible.netcommon.network_cli``

    |enable_mode|         not supported by NETVISOR

    Returned Data Format  ``stdout[0].``
    ====================  ==========================================

.. |enable_mode| replace:: Enable Mode |br| (Privilege Escalation)

Pluribus NETVISOR does not support ``ansible_connection: local``. You must use ``ansible_connection: ansible.netcommon.network_cli``.

Using CLI in Ansible
====================

Example CLI ``group_vars/netvisor.yml``
---------------------------------------

.. code-block:: yaml

   ansible_connection: ansible.netcommon.network_cli
   ansible_network_os: community.netcommon.netvisor
   ansible_user: myuser
   ansible_password: !vault...
   ansible_ssh_common_args: '-o ProxyCommand="ssh -W %h:%p -q bastion01"'


- If you are using SSH keys (including an ssh-agent) you can remove the ``ansible_password`` configuration.
- If you are accessing your host directly (not through a bastion/jump host) you can remove the ``ansible_ssh_common_args`` configuration.
- If you are accessing your host through a bastion/jump host, you cannot include your SSH password in the ``ProxyCommand`` directive. To prevent secrets from leaking out (for example in ``ps`` output), SSH does not support providing passwords through environment variables.

Example CLI task
----------------

.. code-block:: yaml

   - name: Create access list
     community.network.pn_access_list:
       pn_name: "foo"
       pn_scope: "local"
       state: "present"
     register: acc_list
     when: ansible_network_os == 'community.network.netvisor'


.. include:: shared_snippets/SSH_warning.txt

.. seealso::

       :ref:`timeout_options`
