.. _windows_winrm_kerberos:

Kerberos Authentication
=======================

Kerberos authentication is a modern method used in Windows environments for authentication. It allows both the client and server to verify each others identities and supports modern encryption methods like AES.

.. contents::
    :local:


Installing Kerberos
-------------------

Kerberos is provided through a GSSAPI library which is part of a system package. Some distributions install the Kerberos packages by default but others may require manual installation.

To install the Kerberos libraries on a RHEL/Fedora based system:

.. code-block:: bash

    $ sudo dnf install krb5-devel krb5-libs krb5-workstation python3-devel

For a Debian/Ubuntu based system:

.. code-block:: bash

    $ sudo apt-get install krb5-user libkrb5-dev python3-dev

For an Arch Linux based system:

.. code-block:: bash

    $ sudo pacman -S krb5

For a FreeBSD based system:

.. code-block:: bash

    $ sudo pkg install heimdal

.. note::
    The ``python3-devel`` / ``python3-dev`` packages can be ignored if using Kerberos with the ``ssh`` connection plugin. They are only needed if using a WinRM based connection with Kerberos authentication.

Once installed the ``kinit``, ``klist``, and ``krb5-config`` packages will be available. You can test them out with the following command:

.. code-block:: bash

    $ krb5-config --version

    Kerberos 5 release 1.21.3

The ``psrp`` and ``winrm`` connection plugins require extra Python libraries for Kerberos authentication. The following step can be skipped if using Kerberos with the ``ssh`` connection.

If you chose the ``pipx`` install instructions for Ansible, you can install those requirements by running the following:

.. code-block:: shell

   pipx inject "pypsrp[kerberos]<=1.0.0"  # for psrp
   pipx inject "pywinrm[kerberos]>=0.4.0"  # for winrm

Or, if you chose the ``pip`` install instructions:

.. code-block:: shell

   pip3 install "pypsrp[kerberos]<=1.0.0"  # for psrp
   pip3 install "pywinrm[kerberos]>=0.4.0"  # for winrm


Configuring Host Kerberos
-------------------------

Once the dependencies have been installed, Kerberos needs to be configured so that it can communicate with a domain. Most Kerberos implementations can either find a domain using DNS or through manual configuration in the ``/etc/krb5.conf`` file. For details on what can be set in the ``/etc/krb5.conf`` file see `krb5.conf <https://web.mit.edu/kerberos/krb5-latest/doc/admin/conf_files/krb5_conf.html>`_ for more details. A simple ``krb5.conf`` file that uses DNS to lookup the KDC would be:

.. code-block:: ini

    [libdefaults]
        # Not required but helpful if the realm cannot be determined from
        # the hostname
        default_realm = MY.DOMAIN.COM

        # Enabled KDC lookups from DNS SRV records
        dns_lookup_kdc = true

With the above configuration when a Kerberos ticket is requested for the server ``server.my.domain.com`` the Kerberos library will do an SRV lookup for ``_kerberos._udp.my.domain.com`` and ``_kerberos._tcp.my.domain.com`` to find the KDC. If you wish to manually set the KDC realms you can use the following configuration:

.. code-block:: ini

    [libdefaults]
        default_realm = MY.DOMAIN.COM
        dns_lookup_kdc = false

    [realms]
        MY.DOMAIN.COM = {
            kdc = domain-controller1.my.domain.com
            kdc = domain-controller2.my.domain.com
        }

    [domain_realm]
        .my.domain.com = MY.DOMAIN.COM
        my.domain.com = MY.DOMAIN.COM

With this configuration any request for a ticket with the DNS suffix ``.my.domain.com`` and ``my.domain.com`` itself will be sent to the KDC ``domain-controller1.my.domain.com`` with a fallback to ``domain-controller2.my.domain.com``.

More information on how the Kerberos library attempts to find the KDC can be found in the `MIT Kerberos Documentation <https://web.mit.edu/kerberos/krb5-latest/doc/admin/realm_config.html>`_.

.. note::
    The information in this section assumes you are using the MIT Kerberos implementation which is typically the default on most Linux distributions. Some platforms like FreeBSD or macOS use a different GSSAPI implementation called Heimdal which acts in a similar way to MIT Kerberos but some behaviors may be different.


.. _winrm_kerberos_verify_config:

Verifying Kerberos Configuration
--------------------------------

To verify that Kerberos is working correctly, you can use the ``kinit`` command to obtain a ticket for a user in the domain. The following command will request a ticket for the user ``username`` in the domain ``MY.DOMAIN.COM``:

.. code-block:: bash

    $ kinit username@MY.DOMAIN.COM
    Password for username@REALM.COM

If the password is correct, the command will return without any output. To verify that the ticket has been obtained, you can use the ``klist`` command:

.. code-block:: bash

    > klist
    Ticket cache: KCM:1000
    Default principal: username@MY.DOMAIN.COM

    Valid starting     Expires            Service principal
    29/08/24 13:54:51  29/08/24 23:54:51  krbtgt/MY.DOMAIN.COM@MY.DOMAIN.COM
            renew until 05/09/24 13:54:48

If successful, this validates that the Kerberos configuration is correct and that the user can obtain a Ticket Granting Ticket (``TGT``) from the KDC. If ``kinit`` is unable to find the KDC for the requested realm, verify your Kerberos configuration by ensuring DNS can locate the KDC using the SRV records or that the KDC is manually mapped in the ``krb5.conf``.

On MIT Kerberos based systems, you can use the ``kvno`` command to verify that you are able to retrieve a service ticket for a particular service. For example, if you are using a WinRM based connection to authenticate with ``server.my.domain.com`` you can use the following command to verify that your TGT is able to get a service ticket for the target server:

.. code-block:: bash

    $ kvno http/server.my.domain.com
    http/server2025.domain.test@DOMAIN.TEST: kvno = 2

The ``klist`` command can also be used to verify the ticket was stored in the Kerberos cache:

.. code-block:: bash

    $ klist
    Ticket cache: KCM:1000
    Default principal: username@MY.DOMAIN.COM

    Valid starting     Expires            Service principal
    29/08/24 13:54:51  29/08/24 23:54:51  krbtgt/MY.DOMAIN.COM@MY.DOMAIN.COM
            renew until 05/09/24 13:54:48
    29/08/24 13:55:30  29/08/24 23:55:30  http/server.my.domain.com@MY.DOMAIN.COM
            renew until 05/09/24 13:55:30

In the above example we have the TGT stored under the ``krbtgt`` service principal and our ``http/server.my.domain.com`` under its own service principal.

The ``kdestroy`` command can be used to remove the ticket cache.


Ticket Management
-----------------

For Kerberos authentication to work with Ansible, a Kerberos TGT for a user must be present so that Ansible can request a service ticket for the target server. Some connection plugins like ``ssh`` require the TGT to already be present and accessible to the Ansible control process. Other connection plugins, like ``psrp`` and ``winrm``, can automatically obtain a TGT for the user if the user's password is provided in the inventory.

To retrieve a TGT manually for a user, run the ``kinit`` command with the user's username and domain as shown in :ref:`winrm_kerberos_verify_config`. This TGT will be used automatically when Kerberos authentication is requested by the connection plugin in Ansible.

If you are using the ``psrp`` or ``winrm`` connection plugin and the user's password is provided in the inventory, the connection plugin will automatically obtain a TGT for the user. This is done by running the ``kinit`` command with the user's username and password. The TGT will be stored in a temporary credential cache and will be used for the task.


Delegation
----------

Kerberos delegation allows the credentials to traverse multiple hops. This is useful when you need to authenticate to a server and then have that server authenticate to another server on your behalf. To enable delegation, you must:

* request a forwardable TGT when obtaining a ticket with ``kinit``
* request the connection plugin to allow delegation to the server
* the AD user is not marked as sensitive and cannot be delegated and is not a member of the ``Protected Users`` group
* depending on the ``krb5.conf`` configuration, the target server may need to allow unconstrained delegation through its AD object delegation settings
* the target resource to delegate to must be accessible with Kerberos authentication

To request a forwardable TGT, either add the ``-f`` flag to the ``kinit`` command or set the ``forwardable = true`` option in the ``[libdefaults]`` section of the ``krb5.conf`` file. If you are using the ``psrp`` or ``winrm`` connection plugin to retrieve the TGT from the user's password in the inventory, it will automatically request a forwardable TGT if the connection plugin is configured to use delegation.

To have the connection plugin delegate the credentials it will need to set the following hostvar in the inventory:

.. code-block:: yaml+jinja

    # psrp
    ansible_psrp_negotiate_delegate: true

    # winrm
    ansible_winrm_kerberos_delegation: true

    # ssh
    ansible_ssh_common_args: -o GSSAPIDelegateCredentials=yes

.. note::
    It is also possible to set ``GSSAPIDelegateCredentials yes`` in the ``~/.ssh/config`` file to allow delegation for all SSH connections.

To verify if a user is allowed to delegate their credentials, you can run the following PowerShell script on a Windows host in the same domain:

.. code-block:: powershell

    Function Test-IsDelegatable {
        [CmdletBinding()]
        param (
            [Parameter(Mandatory)]
            [string]
            $UserName
        )

        $NOT_DELEGATED = 0x00100000

        $searcher = [ADSISearcher]"(&(objectClass=user)(objectCategory=person)(sAMAccountName=$UserName))"
        $res = $searcher.FindOne()
        if (-not $res) {
            Write-Error -Message "Failed to find user '$UserName'"
        }
        else {
            $uac = $res.Properties.useraccountcontrol[0]
            $memberOf = @($res.Properties.memberof)

            $isSensitive = [bool]($uac -band $NOT_DELEGATED)
            $isProtectedUser = [bool]($memberOf -like 'CN=Protected Users,*').Count

            -not ($isSensitive -or $isProtectedUser)
        }
    }

    Test-IsDelegatable -UserName username

Newer versions of MIT Kerberos have added a configuration option ``enforce_ok_as_delegate`` in the ``[libdefaults]`` section of the ``krb5.conf`` file. If this option is set to ``true`` delegation will only work if the target server account allows unconstrained delegation. To check or set unconstrained delegation on a Windows computer host, you can use the following PowerShell script:

.. code-block:: powershell

    # Check if the server allows unconstrained delegation
    (Get-ADComputer -Identity WINHOST -Properties TrustedForDelegation).TrustedForDelegation

    # Enable unconstrained delegation
    Set-ADComputer -Identity WINHOST -TrustedForDelegation $true

To verify that delegation is working, you can use the ``klist.exe`` command on the Windows node to verify that the ticket has been forwarded. The output should show the ticket server is for ``krbtgt/MY.DOMAIN.COM @ MY.CDOMAIN.COM`` and the ticket flags contained ``forwarded``.

.. code-block:: shell

    $ ansible WINHOST -m ansible.windows.win_command -a C:/Windows/System32/klist.exe

    WINHOST | CHANGED | rc=0 >>

    Current LogonId is 0:0x82b6977

    Cached Tickets: (1)

    #0>     Client: username @ MY.DOMAIN.COM
            Server: krbtgt/MY.DOMAIN.COM @ MY.DOMAIN.COM
            KerbTicket Encryption Type: AES-256-CTS-HMAC-SHA1-96
            Ticket Flags 0x60a10000 -> forwardable forwarded renewable pre_authent name_canonicalize
            Start Time: 8/30/2024 14:15:18 (local)
            End Time:   8/31/2024 0:12:49 (local)
            Renew Time: 9/6/2024 14:12:49 (local)
            Session Key Type: AES-256-CTS-HMAC-SHA1-96
            Cache Flags: 0x1 -> PRIMARY
            Kdc Called:

If anything goes wrong, the output for ``klist.exe`` will not have the ``forwarded`` flag and the server will be for the target server principal and not ``krbtgt``.

.. code-block:: shell

    $ ansible WINHOST -m ansible.windows.win_command -a C:/Windows/System32/klist.exe

    WINHOST | CHANGED | rc=0 >>

    Current LogonId is 0:0x82c312c

    Cached Tickets: (1)

    #0>     Client: username @ MY.DOMAIN.COM
            Server: http/winhost.my.domain.com @ MY.DOMAIN.COM
            KerbTicket Encryption Type: AES-256-CTS-HMAC-SHA1-96
            Ticket Flags 0x40a10000 -> forwardable renewable pre_authent name_canonicalize
            Start Time: 8/30/2024 14:16:24 (local)
            End Time:   8/31/2024 0:16:12 (local)
            Renew Time: 0
            Session Key Type: AES-256-CTS-HMAC-SHA1-96
            Cache Flags: 0x8 -> ASC
            Kdc Called:

It is also important to ensure that the target resource to delegate to will work with Kerberos authentication. This means that the target server must have a Service Principal Name (``SPN``) registered in Active Directory (``AD``) and that the outbound authentication attempt on Windows uses the hostname and not an IP address/alias. For example, you should access a fileshare using the path ``\\server.fqdn.com\share`` and not ``\\192.168.1.2\share``. To verify that an SPN is registered and the session Ansible runs under can delegate using Kerberos, you can use the following ``klist.exe`` command to request a service ticket for the target server.

.. code-block:: shell

    $ ansible WINHOST -m ansible.windows.win_command -a 'C:/Windows/System32/klist.exe get cifs/fs.my.domain.com'

    WINHOST | CHANGED | rc=0 >>

    Current LogonId is 0:0x225639b
    A ticket to cifs/fs.my.domain.com has been retrieved successfully.

    Cached Tickets: (2)

    ...

    #2>     Client: username @ MY.DOMAIN.COM
            Server: cifs/fs.my.domain.com @ MY.DOMAIN.COM
            KerbTicket Encryption Type: AES-256-CTS-HMAC-SHA1-96
            Ticket Flags 0x60a50000 -> forwardable forwarded renewable pre_authent ok_as_delegate name_canonicalize
            Start Time: 8/30/2024 14:16:24 (local)
            End Time:   8/31/2024 0:16:12 (local)
            Renew Time: 0
            Session Key Type: AES-256-CTS-HMAC-SHA1-96
            Cache Flags: 0x8 -> ASC
            Kdc Called: dc01.my.domain.com

.. note::
    The SPN prefix for the target server depends on the service you are trying to access. The ``cifs`` service if used for file shares, ``http`` for web services, and so on. Make sure to use the correct prefix for testing our Kerberos delegation.

Troubleshooting Kerberos
------------------------

Kerberos is reliant on a properly configured environment to work. Some common issues that can cause Kerberos authentication to fail are:

* The hostname set for the Windows host is an alias or an IP address
* The time on the Ansible control node is not synchronized with the AD domain controller
* The KDC realm is not set correctly in the ``krb5.conf`` file or cannot be resolved through DNS

If using the MIT Kerberos implementation, you can set the environment variable ``KRB5_TRACE=/dev/stdout`` to get more detailed information on what the Kerberos library is doing. This can be useful for debugging issues with the Kerberos library such as the KDC lookup behavior, time sync issues, and server name lookup failures.
