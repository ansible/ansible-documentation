.. _windows_app_control:

Windows App Control
===================
`Windows App Control <https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/>`_, formerly known as Windows Defender Application Control (``WDAC``), is a security feature of Windows that can be used to restrict what executables and scripts can be run on a Windows host. In the past, enabling WDAC will cause Ansible to fail when running on the Windows host. Starting with Ansible 2.19 and the ``ansible.windows`` collection at ``3.1.0``, Ansible can now run on Windows hosts with WDAC enabled.

.. admonition:: Experimental functionality

   The App Control implementation is considered an experimental feature and can change in future releases. It is not possible to ensure all PowerShell modules will work with App Control enabled and that a module might enable arbitrary code to run in a way not typically allowed by App Control. It is recommended to test all modules with WDAC enabled before using them in production.

.. contents::
   :local:

Requirements for Ansible to work with App Control
-------------------------------------------------
Ansible requires the target Windows version to be Windows Server 2019 or Windows 10 Build 1803 or later. This is because the ``Dynamic Code Security`` feature added in that Windows version is required to allow Ansible to run tasks on the Windows host.

The first step towards enabling App Control is to create a code signing certificate that will be used to sign the scripts used by Ansible. While this certificate can be self signed, it is recommended that it is issued by a trusted certificate authority used in your organization. How to generate this certificate is outside the scope of this documentation. Once the certificate is setup, the policy file must be generated and applied to the Windows host.

Setting up App Control and configuring policies is not covered under the documentation here. Please read through the Microsoft documentation for `Application Control for Windows <https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/>`_ or `Application Control with PowerShell <https://learn.microsoft.com/en-us/powershell/scripting/security/app-control/how-to-use-app-control?view=powershell-7.5>`_ to understand how to configure App Control and set up policies. The `App Control for Business Wizard <https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/design/appcontrol-wizard>`_ is a tool that can simplify policy generation through a more user friendly GUI.

When setting up a policy it is recommended to configure Ansible as a supplemental policy so it can be easily modified and applied where Ansible will be used. Whether you use a supplemental or just a base policy for trusting the certificate used by Ansible, the base policy must have the following options set:

* User Mode Code Integrity (``0 Enabled:UMCI``) is enabled
* Disable Script Enforcement (``11 Disabled:Script Enforcement``) is not enabled
* Dynamic Code Security (``19 Enabled:Dynamic Code Security``) is enabled

The policy then should then add the certificate as a trusted publisher to the ``User Mode Signing Scenario``, for example this is an example policy configuration that contains a trusted publisher:

.. code-block:: text

   <SiPolicy>
      ...
      <Signers>
         <Signer Name="Some Signer" ID="ID_SIGNER_S_0">
            <CertRoot Type="TBS" Value="1DBF60AFC6313593EDB09B6C6239BE493FF3461D4BD6D0A8C6E1723A12C06438F471BB7F6BAA73BD142D0698CEFF9DBB" />
            <CertPublisher Value="Some Publisher" />
         </Signer>
      </Signers>
      <SigningScenarios>
         <SigningScenario ID="ID_SIGNINGSCENARIO_KMCI" FriendlyName="Kernel Mode Signing Scenario" Value="131">
            <ProductSigners />
         </SigningScenario>
         <SigningScenario ID="ID_SIGNINGSCENARIO_UMCI" FriendlyName="User Mode Signing Scenario" Value="12">
            <ProductSigners>
            <AllowedSigners>
               <AllowedSigner SignerId="ID_SIGNER_S_0" />
            </AllowedSigners>
            </ProductSigners>
         </SigningScenario>
      </SigningScenarios>
      ...
   </SiPolicy>

Once the policy is created and the certificate that will be used to sign the Ansible content is trusted by the Windows host, the policy can be applied.

.. Warning::
     As Ansible typically runs tasks as an Administrator, it is important that the policy is signed and is applied so that Ansible cannot unset the policy through a task like ``win_file`` or ``win_regedit``.

How to Sign Ansible Content
---------------------------
Once the code signing certificate has been generated and trusted by the Windows host, it can be used to sign the scripts that Ansible will run. The PowerShell script `New-AnsiblePowerShellSignature.ps1 <https://raw.githubusercontent.com/ansible/ansible-documentation/refs/heads/devel/examples/scripts/New-AnsiblePowerShellSignature.ps1>`_ can be used to sign both the execution wrapper used by Ansible to invoke modules and any PowerShell modules inside an Ansible collection. It requires the following to run:

* PowerShell 7.4 or later
* The `OpenAuthenticode <https://github.com/jborean93/PowerShell-OpenAuthenticode>`_ PowerShell module
* Python with Ansible and the required collections installed
* Access to the certificate and private key trusted by the App Control policy, typically as a PFX file

.. note::
   The ``New-AnsiblePowerShellSignature`` function is not officially supported and is marked as a tech preview.

To sign the Ansible PowerShell wrapper scripts, and modules in a collection, the following PowerShell script can be used with the loaded function from above:

.. code-block:: powershell

   $certPassword = Read-Host "Enter the password for the certificate" -AsSecureString
   $cert = [System.Security.Cryptography.X509Certificates.X509Certificate2]::new(
      "wdac-cert.pfx"
      $certPassword)

   $signingParams = @{
      Certificate = $cert

      Collection = @(
         # Includes all the builtin execution wrappers and scripts needed for Ansible
         'ansible.builtin'

         # Add any remaining collections used in the playbook like microsoft.ad, community.windows, etc.
         'ansible.windows'
         'microsoft.ad'
         'microsoft.iis'
         'community.windows'
      )

      # The URL of the Authenticode timestamp server to use for timestamping
      # the signature.
      # https://learn.microsoft.com/en-us/windows/win32/seccrypto/time-stamping-authenticode-signatures
      TimeStampServer = '...'
   }
   New-AnsiblePowerShellSignature @signingParams -Verbose

The ``ansible.builtin`` collection refers to the builtin execution scripts used in Ansible. Any other collection with PowerShell modules used in the playbook should be added to the ``-Collection`` parameter. The script will generate the ``powershell_signatures.psd1`` script signed by the certificate and contains the hashes of all the modules in the collection that should be trusted to run. It will also generate the signature for Ansible's execution wrapper script in the Ansible installation directory so that Ansible can automatically run the script trusted by the App Control policy. The current behavior of ``New-AnsiblePowerShellSignature`` is to sign all the modules in the collection and the Ansible execution wrapper script even if they could include an escape hatch. It is recommended to skip any modules using the ``-Skip`` parameter that are not needed in the playbook, for example:

.. code-block:: powershell

   New-AnsiblePowerShellSignature ... -Skip @(
       'ansible.windows.win_dsc'
       'ansible.windows.win_timezone'
   )

Any PowerShell content that is not part of a collection, like custom scripts or code used in ``ansible.windows.win_powershell``, must be signed manually using the ``Set-AuthenticodeSignature`` cmdlet on Windows or ``Set-OpenAuthenticodeSignature`` through ``OpenAuthenticode`` module on Linux. It is important that these signed scripts are used in a way that will not modify the contents of the script or else the signature will be invalidated. For example the ``ansible.builtin.script`` module will copy the script file to the target host as is leaving the signature intact but using the ``ansible.builtin.file`` lookup will strip any remaining newline characters unless the ``rstrip=False`` option is used.

Known Module Differences
------------------------
When App Control is enabled, some modules may not work, or behave differently, even if signed. Some of the known differences are:

* ``ansible.windows.win_command`` can only execute executables trusted by the App Control policy. If the executable is not trusted, the module will fail
* ``ansible.windows.win_shell`` will run all code in Constrained Language Mode (``CLM``) which is highly restricted and may cause some scripts to fail
* ``ansible.windows.win_powershell`` will run in CLM by default unless the provided script is signed
* ``ansible.builtin.script`` will run in CLM by default unless the provided script is signed
* ``ansible.windows.win_package`` can only run executables trusted by the App Control policy so may or may not work depending on the executable
* ``ansible.windows.win_updates`` is currently not supported and will not work

Other modules that start sub-processes or rely on unsigned PowerShell content will most likely not work with App Control enabled.

If trying to run a PowerShell script with ``ansible.windows.win_powershell`` or ``ansible.builtin.script``, the script itself must be signed or else it will be run in CLM.

.. code-block:: yaml

   - name: Test out LanguageMode
     ansible.windows.win_powershell:
       script: $ExecutionContext.SessionState.LanguageMode

It is important that when referencing a signed script that the script is not modified in any way. This means the line endings and whitespace that were present when it was signed must be the same when Ansible uses the signed script.

.. note::
   Ansible will always load the script with the UTF-8 encoding even if no Byte Order Mark (``BOM``) is present. It is important that the script was encoded with UTF-8 without a BOM when it was signed so that the signature stays valid. If the script was signed with a different encoding, the signature could be invalidated or PowerShell may interpret it with different characters.

When referencing a signed script in Ansible, it is important that it is used in a way that does not modify the contents of the script which would break the signature. For example you should have the signed script in the local ``files`` directory associated with the playbook/tasks and reference in one of the following ways:

.. code-block:: yaml

   - name: Run signed script through the script module
     ansible.builtin.script: signed-script.ps1

   - name: Run signed script through win_powershell as a path
     ansible.windows.win_powershell:
       path: signed-script.ps1

   - name: Run signed script through win_powershell as inline content
     ansible.windows.win_powershell:
       # rstrip=False is important so the last \r\n of the signature is not removed.
       script: "{{ lookup('ansible.builtin.file', 'signed-script.ps1', rstrip=False) }}"
