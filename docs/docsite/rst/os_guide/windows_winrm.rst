.. _windows_winrm:

Windows Remote Management
=========================

Unlike Linux/Unix hosts, which use SSH by default, Windows hosts are
configured with WinRM. This topic covers how to configure and use WinRM with Ansible.

.. contents::
   :local:


What is WinRM?
----------------

WinRM is a management protocol used by Windows to remotely communicate with
another server. It is a SOAP-based protocol that communicates over HTTP/HTTPS and is
included in all recent Windows operating systems. Since Windows
Server 2012, WinRM has been enabled by default, but in some cases, extra
configuration is required to use WinRM with Ansible.

Ansible can use WinRM through the :ref:`psrp <psrp_connection>` or :ref:`winrm <winrm_connection>` connection plugins. These plugins have their own Python requirements that are not included in the Ansible package and must be installed separately.

If you chose the ``pipx`` install instructions, you can install those requirements by running the following:

.. code-block:: shell

   pipx inject ansible "pypsrp<=1.0.0"  # for psrp
   pipx inject ansible "pywinrm>=0.4.0"  # for winrm

Or, if you chose the ``pip`` install instructions:

.. code-block:: shell

   pip3 install "pypsrp<=1.0.0"  # for psrp
   pip3 install "pywinrm>=0.4.0"  # for winrm

.. Warning::
     Using the ``winrm`` or ``psrp`` connection plugins in Ansible on MacOS in the latest releases typically fails. This is a known problem that occurs deep within the Python stack and cannot be changed by Ansible. The only workaround today is to set the environment variable ``OBJC_DISABLE_INITIALIZE_FORK_SAFETY=yes``, ``no_proxy=*`` and avoid using Kerberos auth.


WinRM Setup
-----------

Before Ansible can connect using WinRM, the Windows host must have a WinRM listener configured. This listener will listen on the configured port and accept incoming WinRM requests.

While this guide covers more details on how to enumerate, add, and remove listeners, you can run the following PowerShell snippet to setup the HTTP listener with the defaults:

.. code-block:: powershell

    # Enables the WinRM service and sets up the HTTP listener
    Enable-PSRemoting -Force

    # Opens port 5985 for all profiles
    $firewallParams = @{
        Action      = 'Allow'
        Description = 'Inbound rule for Windows Remote Management via WS-Management. [TCP 5985]'
        Direction   = 'Inbound'
        DisplayName = 'Windows Remote Management (HTTP-In)'
        LocalPort   = 5985
        Profile     = 'Any'
        Protocol    = 'TCP'
    }
    New-NetFirewallRule @firewallParams

    # Allows local user accounts to be used with WinRM
    # This can be ignored if using domain accounts
    $tokenFilterParams = @{
        Path         = 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System'
        Name         = 'LocalAccountTokenFilterPolicy'
        Value        = 1
        PropertyType = 'DWORD'
        Force        = $true
    }
    New-ItemProperty @tokenFilterParams

To also add a HTTPS listener with a self signed certificate we can run the following:

.. code-block:: powershell

    # Create self signed certificate
    $certParams = @{
        CertStoreLocation = 'Cert:\LocalMachine\My'
        DnsName           = $env:COMPUTERNAME
        NotAfter          = (Get-Date).AddYears(1)
        Provider          = 'Microsoft Software Key Storage Provider'
        Subject           = "CN=$env:COMPUTERNAME"
    }
    $cert = New-SelfSignedCertificate @certParams

    # Create HTTPS listener
    $httpsParams = @{
        ResourceURI = 'winrm/config/listener'
        SelectorSet = @{
            Transport = "HTTPS"
            Address   = "*"
        }
        ValueSet = @{
            CertificateThumbprint = $cert.Thumbprint
            Enabled               = $true
        }
    }
    New-WSManInstance @httpsParams

    # Opens port 5986 for all profiles
    $firewallParams = @{
        Action      = 'Allow'
        Description = 'Inbound rule for Windows Remote Management via WS-Management. [TCP 5986]'
        Direction   = 'Inbound'
        DisplayName = 'Windows Remote Management (HTTPS-In)'
        LocalPort   = 5986
        Profile     = 'Any'
        Protocol    = 'TCP'
    }
    New-NetFirewallRule @firewallParams

.. warning::
    The above scripts are for demonstration purposes only and should be reviewed before running in a production environment. Some changes, like opening the firewall port for all incoming connections, allowing local accounts to be used with WinRM, self signed certificates, may not be suitable for all environments.


Enumerate Listeners
"""""""""""""""""""

To view the current listeners that are running on the WinRM service:

.. code-block:: powershell

    winrm enumerate winrm/config/Listener

This will output something like:

.. code-block:: powershell

    Listener
        Address = *
        Transport = HTTP
        Port = 5985
        Hostname
        Enabled = true
        URLPrefix = wsman
        CertificateThumbprint
        ListeningOn = 10.0.2.15, 127.0.0.1, 192.168.56.155, ::1, fe80::5efe:10.0.2.15%6, fe80::5efe:192.168.56.155%8, fe80::
    ffff:ffff:fffe%2, fe80::203d:7d97:c2ed:ec78%3, fe80::e8ea:d765:2c69:7756%7

    Listener
        Address = *
        Transport = HTTPS
        Port = 5986
        Hostname = SERVER2016
        Enabled = true
        URLPrefix = wsman
        CertificateThumbprint = E6CDAA82EEAF2ECE8546E05DB7F3E01AA47D76CE
        ListeningOn = 10.0.2.15, 127.0.0.1, 192.168.56.155, ::1, fe80::5efe:10.0.2.15%6, fe80::5efe:192.168.56.155%8, fe80::
    ffff:ffff:fffe%2, fe80::203d:7d97:c2ed:ec78%3, fe80::e8ea:d765:2c69:7756%7

In the example above there are two WinRM listeners configured. One is listening on port 5985 over HTTP and the other is listening on port 5986 over HTTPS. Some of the key options that are useful to understand are:

* ``Transport``: Whether the listener is run over HTTP or HTTPS
* ``Port``: The port the to listen on, default for HTTP is ``5985`` and HTTPS is ``5986``
* ``CertificateThumbprint``: For HTTPS, this is the thumbprint of the certificate used for the TLS connection

To view the certificate details that is specified by the ``CertificateThumbprint`` you can run the following PowerShell command:

.. code-block:: powershell

    $thumbprint = "E6CDAA82EEAF2ECE8546E05DB7F3E01AA47D76CE"
    Get-Item -Path "Cert:\LocalMachine\My\$thumbprint" | Select-Object *


Create Listener
"""""""""""""""

Creating a HTTP listener can be done through the ``Enable-PSRemoting`` cmdlet but you can also use the following PowerShell code to manually create the HTTP listener.

.. code-block:: powershell

    $listenerParams = @{
        ResourceURI = 'winrm/config/listener'
        SelectorSet = @{
            Transport = "HTTP"
            Address   = "*"
        }
        ValueSet    = @{
            Enabled = $true
            Port    = 5985
        }
    }
    New-WSManInstance @listenerParams

Creating a HTTPS listener is similar but the ``Port`` is now ``5986`` and the ``CertificateThumbprint`` value must be set. The certificate can either be a self signed certificate or a certificate from a certificate authority. How to generate a certificate is outside the scope of this section.

.. code-block:: powershell

    $listenerParams = @{
        ResourceURI = 'winrm/config/listener'
        SelectorSet = @{
            Transport = "HTTPS"
            Address   = "*"
        }
        ValueSet    = @{
            CertificateThumbprint = 'E6CDAA82EEAF2ECE8546E05DB7F3E01AA47D76CE'
            Enabled               = $true
            Port                  = 5986
        }
    }
    New-WSManInstance @listenerParams

The ``CertificateThumbprint`` value must be set to the thumbprint of a certificate that is installed in the ``LocalMachine\My`` certificate store.

The ``Address`` selector value can be set to one of three values:

* ``*`` - binds to all addresses
* ``IP:...`` - binds to the IPv4 or IPv6 address specified by ``...``
* ``MAC:32-a3-58-90-be-cc`` - binds to the adapter with the MAC address specified


Remove Listener
"""""""""""""""

The following code can remove all listeners or a specific one:

.. code-block:: powershell

   # Removes all listeners
   Remove-Item -Path WSMan:\localhost\Listener\* -Recurse -Force

   # Removes only HTTP listeners
   Get-ChildItem -Path WSMan:\localhost\Listener |
       Where-Object Keys -contains "Transport=HTTP" |
       Remove-Item -Recurse -Force

  # Removes only HTTPS listeners
   Get-ChildItem -Path WSMan:\localhost\Listener |
       Where-Object Keys -contains "Transport=HTTPS" |
       Remove-Item -Recurse -Force


WinRM Authentication
--------------------

WinRM has several different authentication options that can be used to authenticate a user with a Windows host. Each option has their own advantages and disadvantages so it is important to understand when to use each one and when to not.

The following matrix is a high-level overview of the options:

+-------------+----------------+---------------------------+-----------------------+-----------------+
| Option      | Local Accounts | Active Directory Accounts | Credential Delegation | HTTP Encryption |
+=============+================+===========================+=======================+=================+
| Basic       | Yes            | No                        | No                    | No              |
+-------------+----------------+---------------------------+-----------------------+-----------------+
| Certificate | Yes            | No                        | No                    | No              |
+-------------+----------------+---------------------------+-----------------------+-----------------+
| Kerberos    | No             | Yes                       | Yes                   | Yes             |
+-------------+----------------+---------------------------+-----------------------+-----------------+
| NTLM        | Yes            | Yes                       | No                    | Yes             |
+-------------+----------------+---------------------------+-----------------------+-----------------+
| CredSSP     | Yes            | Yes                       | Yes                   | Yes             |
+-------------+----------------+---------------------------+-----------------------+-----------------+

The ``Basic`` and ``NTLM`` authentication options should not be used over a HTTP listener as they either offer no encryption or very weak encryption. The ``psrp`` connection plugin also offers the ``Negotiate`` authentication option which will attempt to use ``Kerberos`` before falling back to ``NTLM``. The ``winrm`` connection plugin must either specify ``kerberos`` or ``ntlm``.

To specify the authentication protocol you can use the following variables:

.. code-block:: yaml+jinja

    # For psrp
    ansible_psrp_auth: basic|certificate|negotiate|kerberos|ntlm|credssp

    # For winrm
    ansible_winrm_transport: basic|certificate|kerberos|ntlm|credssp

The recommendations for WinRM would be to use Kerberos auth over HTTP if in a domain environment or Basic/NTLM over HTTPS for local accounts. CredSSP should only be used when absolutely necessary as it can be a security risk due to its use of unconstrained delegation.


Basic
"""""

Basic authentication is one of the simplest authentication options to use but is
also the most insecure. This is because the username and password are simply
base64 encoded, and if a secure channel is not in use (eg, HTTPS) then it can be
decoded by anyone. Basic authentication can only be used for local accounts (not domain accounts).

The following example shows host vars configured for basic authentication:

.. code-block:: yaml+jinja

    ansible_user: LocalUsername
    ansible_password: Password

    # psrp
    ansible_connection: psrp
    ansible_psrp_auth: basic

    # winrm
    ansible_connection: winrm
    ansible_winrm_transport: basic

Basic authentication is not enabled by default on a Windows host but can be
enabled by running the following in PowerShell:

.. code-block:: powershell

    Set-Item -Path WSMan:\localhost\Service\Auth\Basic -Value $true


Certificate
"""""""""""

See :ref:`windows_winrm_certificate` for more information on how to configure and use certificate authentication.


NTLM
""""

NTLM is an older authentication mechanism used by Microsoft that can support
both local and domain accounts. NTLM is enabled by default on the WinRM
service, so no setup is required before using it.

NTLM is the easiest authentication protocol to use and is more secure than
``Basic`` authentication. If running in a domain environment, ``Kerberos`` should be used
instead of NTLM.

Kerberos has several advantages over using NTLM:

* NTLM is an older protocol and does not support newer encryption
  protocols.
* NTLM is slower to authenticate because it requires more round trips to the host in
  the authentication stage.
* Unlike Kerberos, NTLM does not allow credential delegation.

This example shows host variables configured to use NTLM authentication:

.. code-block:: yaml+jinja

    ansible_user: LocalUsername
    ansible_password: Password

    # psrp
    ansible_connection: psrp
    ansible_psrp_auth: negotiate  # or ntlm to only use NTLM

    # winrm
    ansible_connection: winrm
    ansible_winrm_transport: ntlm


Kerberos and Negotiate
""""""""""""""""""""""

Kerberos is the recommended authentication option to use when running in a
domain environment. Kerberos supports features like credential delegation and
message encryption over HTTP and is one of the more secure options that
is available through WinRM.

Kerberos does require some additional setup work on the Ansible host before it can be used properly. See :ref:`windows_winrm_kerberos` for more information on how to configure, use, and troubleshoot Kerberos authentication.

The following example shows host vars configured for Kerberos authentication:

.. code-block:: yaml+jinja

    ansible_user: username@MY.DOMAIN.COM
    ansible_password: Password

    # psrp
    ansible_connection: psrp
    ansible_psrp_auth: negotiate  # or kerberos to disable ntlm fallback

    # winrm
    ansible_connection: winrm
    ansible_winrm_transport: kerberos


CredSSP
"""""""

CredSSP authentication is a newer authentication protocol that allows
credential delegation. This is achieved by encrypting the username and password
after authentication has succeeded and sending that to the server using the
CredSSP protocol.

Because the username and password are sent to the server to be used for double
hop authentication, ensure that the hosts that the Windows host communicates with are
not compromised and are trusted.

CredSSP can be used for both local and domain accounts and also supports
message encryption over HTTP.

To use CredSSP authentication, the host vars are configured like so:

.. code-block:: yaml+jinja

    ansible_user: Username
    ansible_password: Password

    # psrp
    ansible_connection: psrp
    ansible_psrp_auth: credssp

    # winrm
    ansible_connection: winrm
    ansible_winrm_transport: credssp

CredSSP authentication is not enabled by default on a Windows host, but can
be enabled by running the following in PowerShell:

.. code-block:: powershell

    Enable-WSManCredSSP -Role Server -Force

CredSSP requires optional Python libraries to be installed and can be done with pipx:

.. code-block:: shell

   pipx inject "pypsrp[credssp]<=1.0.0"  # for psrp
   pipx inject "pywinrm[credssp]>=0.4.0"  # for winrm

Or, if you chose the ``pip`` install instructions:

.. code-block:: shell

   pip3 install "pypsrp[credssp]<=1.0.0"  # for psrp
   pip3 install "pywinrm[credssp]>=0.4.0"  # for winrm

CredSSP works by using a TLS connection to wrap the authentication tokens and subsequent messages sent over the connection. By default it will use a self-signed certificate automatically generated by Windows. While using CredSSP over a HTTPS connection will still need to validate the HTTPS certificate used by the WinRM listener, there is no validation done on the CredSSP certificate. It is possible to configure CredSSP to use a different certificate by setting the ``CertificateThumbprint`` option under the WinRM service configuration.

.. code-block:: powershell

    # Note the value $thumprint will be different in each situation, this needs
    # to be set based on the cert that is used.
    $thumbprint = "7C8DCBD5427AFEE6560F4AF524E325915F51172C"

    # Set the thumbprint value
    Set-Item -Path WSMan:\localhost\Service\CertificateThumbprint -Value $thumbprint


Non-Administrator Accounts
---------------------------

WinRM is configured by default to only allow connections from accounts in the local
``Administrators`` group. This can be changed by running:

.. code-block:: powershell

    winrm configSDDL default

This will display an ACL editor, where new users or groups may be added. To run commands
over WinRM, users and groups must have at least the ``Read`` and ``Execute`` permissions
enabled.

While non-administrative accounts can be used with WinRM, most typical server administration
tasks require some level of administrative access, so the utility is usually limited.


WinRM Encryption
-----------------

By default, WinRM will fail to work when running over an unencrypted channel.
The WinRM protocol considers the channel to be encrypted if using TLS over HTTP
(HTTPS) or using message-level encryption. Using WinRM with TLS is the
recommended option as it works with all authentication options, but requires
a certificate to be created and used on the WinRM listener.

If in a domain environment, ADCS can create a certificate for the host that
is issued by the domain itself.

If using HTTPS is not an option, then HTTP can be used when the authentication
option is ``NTLM``, ``Kerberos`` or ``CredSSP``. These protocols will encrypt
the WinRM payload with their own encryption method before sending it to the
server. The message-level encryption is not used when running over HTTPS because the
encryption uses the more secure TLS protocol instead. If both transport and
message encryption is required, the following hostvars can be set:

.. code-block:: yaml+jinja

    # psrp
    ansible_psrp_message_encryption: always

    # winrm
    ansible_winrm_message_encryption: always

.. Note:: Message encryption over HTTP requires pywinrm>=0.3.0.

A last resort is to disable the encryption requirement on the Windows host. This
should only be used for development and debugging purposes, as anything sent
from Ansible can be viewed or manipulated, and the remote session can
be completely taken over by anyone on the same network. To disable the encryption
requirement:

.. code-block:: powershell

    Set-Item -Path WSMan:\localhost\Service\AllowUnencrypted -Value $true

.. Note:: Do not disable the encryption check unless it is
    absolutely required. Doing so could allow sensitive information like
    credentials and files to be intercepted by others on the network.


.. _windows_winrm_cert_validation:

HTTPS Certificate Validation
-----------------------------

As part of the TLS protocol, the certificate is validated to ensure the host matches the subject and the client trusts the issuer of the server certificate. If using a self-signed certificate, the certificate will not be trusted by the client and the connection will fail. To bypass this, set the following hostvars depending on the connection plugin used:

* ``ansible_psrp_cert_validation: ignore``
* ``ansible_winrm_server_cert_validation: ignore``

One of the more common ways of setting up an HTTPS listener in a domain
environment is to use Active Directory Certificate Service (AD CS). AD CS is
used to generate signed certificates from a Certificate Signing Request (CSR).
If the WinRM HTTPS listener is using a certificate that has been signed by
another authority, like AD CS, then Ansible can be set up to trust that
issuer as part of the TLS handshake.

To get Ansible to trust a Certificate Authority (CA) like AD CS, the issuer
certificate of the CA can be exported as a PEM-encoded certificate. This
certificate can then be copied locally to the Ansible control node and used as a
source of certificate validation, otherwise known as a CA chain.

The CA chain can contain a single or multiple issuer certificates and each entry is contained on a new line. To then use the custom CA chain as part of the validation process, set the following hostvar depending on the connection plugin used to the path of the CA PEM formatted file:

* ``ansible_psrp_ca_cert``
* ``ansible_winrm_ca_trust_path``

If this variable is not set, the default CA chain is used instead which is located in the install path of the Python package `certifi <https://github.com/certifi/python-certifi>`_. Some Linux distributions may have configured the underlying Python ``requests`` library that the ``psrp`` and ``winrm`` connection plugins use to use the system's certificate store rather than ``certifi``. If this is the case, the CA chain will be the same as the system's certificate store.


WinRM limitations
------------------
Due to the design of the WinRM protocol, there are a few limitations
when using WinRM which can cause issues when creating playbooks for Ansible.
These include:

* Credentials are not delegated for most authentication types, which causes
  authentication errors when accessing network resources or installing certain
  programs.

* Many calls to the Windows Update API are blocked when running over WinRM.

* Some programs fail to install with WinRM due to no credential delegation or
  because they access forbidden Windows APIs like WUA over WinRM.

* Commands under WinRM are done under a non-interactive session, which can prevent
  certain commands or executables from running.

* You cannot run a process that interacts with ``DPAPI``, which is used by some
  installers (like Microsoft SQL Server).

Some of these limitations can be mitigated by doing one of the following:

* Set the authentication method to use ``credssp`` or ``kerberos`` with credential delegation enabled

* Use ``become`` to bypass all WinRM restrictions and run a command as it would
  locally. Unlike using an authentication transport like ``credssp``, this will
  also remove the non-interactive restriction and API restrictions like WUA and
  DPAPI

* Use a scheduled task to run a command that can be created with the
  ``win_scheduled_task`` module. Like ``become``, this bypasses all WinRM
  restrictions but can only run a command and not modules.


WinRM Troubleshooting
---------------------
WinRM has a wide range of configuration options, which makes its configuration complex. As a result, errors that Ansible displays could in fact be problems with the host setup instead.

To identify a host issue, run the following command from another Windows host to test out a connection to the target Windows host.

* To test HTTP:

.. code-block:: powershell

    # winrm
    winrs -r:http://server:5985/wsman -u:Username -p:Password ipconfig

    # psrp
    Invoke-Command -ComputerName server { ipconfig } -Credential username

* To test HTTPS:

.. code-block:: powershell

    # winrm
    winrs -r:https://server:5986/wsman -u:Username -p:Password -ssl ipconfig

    # psrp
    Invoke-Command -UseSSL -ComputerName server { ipconfig } -Credential username

    # psrp ignoring certs
    $sessionOption = New-PSSessionOption -SkipCACheck -SkipCNCheck -SkipRevocationCheck
    Invoke-Command -UseSSL -ComputerName server { ipconfig } -Credential username -SessionOption $sessionOption

To verify that the target hostname is resolvable on the Ansible control node, run one of the following commands:

.. code-block:: bash

    dig +search server

    # May fail if the Windows firewall is set to block ICMP pings
    # but will show the hostname if resolvable.
    ping server

To verify that the WinRM service is listening and a firewall is not blocking the connection you can use ``nc`` to test the connection over the WinRM port:

.. code-block:: bash

    # HTTP port
    > nc -zv server 5985
    Connection to server port 5985 [tcp/wsman] succeeded!

    # HTTPS port
    > nc -zv server 5986
    Connection to server port 5986 [tcp/wsmans] succeeded!

To verify that WinRM has a HTTPS listener and is working you can use ``openssl s_client`` to test the connection and view the certificate details with:

.. code-block:: bash

    echo '' | openssl s_client -connect server:5986

.. note::
    The ``openssl s_client`` command will use the system trust store to validate the certificate which may not align with the trust store used in Ansible. See :ref:`windows_winrm_cert_validation` for more information.

.. seealso::

   :ref:`playbooks_intro`
       An introduction to playbooks
   :ref:`playbooks_best_practices`
       Tips and tricks for playbooks
   :ref:`List of Windows Modules <windows_modules>`
       Windows-specific module list, all implemented in PowerShell
   :ref:`Communication<communication>`
       Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide
