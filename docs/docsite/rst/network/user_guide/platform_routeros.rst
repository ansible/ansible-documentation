.. _routeros_platform_options:

***************************************
RouterOS Platform Options
***************************************

RouterOS is part of the `community.network <https://galaxy.ansible.com/ui/repo/published/community/network>`_ collection and only supports CLI connections and direct API access.
This page offers details on how to use ``ansible.netcommon.network_cli`` on RouterOS in Ansible.
Further information can be found in :ref:`the community.routeros collection's SSH guide
<ansible_collections.community.routeros.docsite.ssh-guide>`.

Information on how to use the RouterOS API can be found in :ref:`the community.routeros collection's API guide
<ansible_collections.community.routeros.docsite.api-guide>`.


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

    Connection Settings   ``ansible_connection: ansible.network.network_cli``

    |enable_mode|         not supported by RouterOS

    Returned Data Format  ``stdout[0].``
    ====================  ==========================================

.. |enable_mode| replace:: Enable Mode |br| (Privilege Escalation)


The RouterOS SSH modules do not support ``ansible_connection: local``. You must use ``ansible_connection: ansible.netcommon.network_cli``.

The RouterOS API modules require ``ansible_connection: local``. See the :ref:`the community.routeros collection's API guide
<ansible_collections.community.routeros.docsite.api-guide>` for more information.


Using CLI in Ansible
====================

Example CLI ``group_vars/routeros.yml``
---------------------------------------

.. code-block:: yaml

   ansible_connection: ansible.netcommon.network_cli
   ansible_network_os: community.network.routeros
   ansible_user: myuser
   ansible_password: !vault...
   ansible_become: true
   ansible_become_method: enable
   ansible_become_password: !vault...
   ansible_paramiko_proxy_command: '-o ProxyCommand="ssh -W %h:%p -q bastion01"'


- If you are using SSH keys (including an ssh-agent) you can remove the ``ansible_password`` configuration.
- If you are accessing your host directly (not through a bastion/jump host) you can remove the ``ansible_paramiko_proxy_command`` configuration.
- If you are accessing your host through a bastion/jump host, you cannot include your SSH password in the ``ProxyCommand`` directive. To prevent secrets from leaking out (for example in ``ps`` output), SSH does not support providing passwords through environment variables.
- If you are getting timeout errors you may want to add ``+cet1024w`` suffix to your username which will disable console colors, enable "dumb" mode, tell RouterOS not to try detecting terminal capabilities and set terminal width to 1024 columns. See article `Console login process <https://wiki.mikrotik.com/wiki/Manual:Console_login_process>`_ in MikroTik wiki for more information.
- More notes can be found in the :ref:`the community.routeros collection's SSH guide <ansible_collections.community.routeros.docsite.ssh-guide>`.

Example CLI task
----------------

.. code-block:: yaml

   - name: Display resource statistics (routeros)
     community.network.routeros_command:
       commands: /system resource print
     register: routeros_resources
     when: ansible_network_os == 'community.network.routeros'

.. include:: shared_snippets/SSH_warning.txt

.. seealso::

       :ref:`timeout_options`
