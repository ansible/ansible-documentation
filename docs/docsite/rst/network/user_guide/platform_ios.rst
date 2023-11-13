.. _ios_platform_options:

***************************************
IOS Platform Options
***************************************

The `Cisco IOS <https://galaxy.ansible.com/ui/repo/published/cisco/ios>`_ collection supports Enable Mode (Privilege Escalation). This page offers details on how to use Enable Mode on IOS in Ansible.

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

    |enable_mode|         supported: use ``ansible_become: true`` with
                          ``ansible_become_method: enable`` and ``ansible_become_password:``

    Returned Data Format  ``stdout[0].``
    ====================  ==========================================

.. |enable_mode| replace:: Enable Mode |br| (Privilege Escalation)


The ``ansible_connection: local`` has been deprecated. Please use ``ansible_connection: ansible.netcommon.network_cli`` instead.

Using CLI in Ansible
====================

Example CLI ``group_vars/ios.yml``
----------------------------------

.. code-block:: yaml

   ansible_connection: ansible.netcommon.network_cli
   ansible_network_os: cisco.ios.ios
   ansible_user: myuser
   ansible_password: !vault...
   ansible_become: true
   ansible_become_method: enable
   ansible_become_password: !vault...
   ansible_ssh_common_args: '-o ProxyCommand="ssh -W %h:%p -q bastion01"'


- If you are using SSH keys (including an ssh-agent) you can remove the ``ansible_password`` configuration.
- If you are accessing your host directly (not through a bastion/jump host) you can remove the ``ansible_ssh_common_args`` configuration.
- If you are accessing your host through a bastion/jump host, you cannot include your SSH password in the ``ProxyCommand`` directive. To prevent secrets from leaking out (for example in ``ps`` output), SSH does not support providing passwords through environment variables.

Example CLI task
----------------

.. code-block:: yaml

   - name: Backup current switch config (ios)
     cisco.ios.ios_config:
       backup: yes
     register: backup_ios_location
     when: ansible_network_os == 'cisco.ios.ios'

.. include:: shared_snippets/SSH_warning.txt

.. seealso::

       :ref:`timeout_options`
