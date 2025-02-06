.. _windows_wdac:

Windows App Control
===================
Windows App Control, formerly known as Windows Defender Application Control (``WDAC``), is a security feature of Windows that can be used to restrict what executables and scripts can be run on a Windows host. In the past, enabling WDAC will cause Ansible to fail when running on the Windows host. Starting with Ansible 2.19, Ansible can now run on Windows hosts with WDAC enabled.

.. Warning::
     The App Control implementation is considered a tech preview and can change in future releases. It is not possible to ensure all PowerShell modules will work with App Control enabled and that a module might enable arbitrary code to run in a way not typically allowed by App Control. It is recommended to test all modules with WDAC enabled before using them in production.

.. contents:: Topics
   :local:

Requirements for Ansible to work with App Control
-------------------------------------------------
Ansible requires the target Windows version to be Windows Server 2019 or Windows 10 Build 1803 or later. This is because the ``Dynamic Code Security`` feature added in that Windows version is required to allow Ansible to run tasks on the Windows host.

The first step towards enabling App Control is to create a code signing certificate that will be used to sign the scripts used by Ansible. While this certificate can be self signed, it is recommended that it is issued by a trusted certificate authority used in your organisation. How to generate this certificate is outside the scope of this documentation. Once the certificate is the policy file must be generated and applied to the Windows host.

Setting up App Control and configuring policies is not covered under the documentation here. Please read through the Microsoft documentation for `Application Control for Windows <https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/>`_ or `Application Control with PowerShell <https://learn.microsoft.com/en-us/powershell/scripting/security/app-control/how-to-use-app-control?view=powershell-7.5>`_ to understand how to configure App Control and set up policies. The `App Control for Business Wizard <https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/design/appcontrol-wizard>`_ is a good tool for generating WDAC policies through a more user friendly GUI.

When setting up a policy it is recommended to configure Ansible through a supplemental policy so it can be easily modified and applied where Ansible will be used. While the Ansible configuration should be done in a supplemental policy, the base policy must have the following options set:

* User Mode Code Integrity (``0 Enabled:UMCI``) is enabled
* Disable Script Enforcement (``11 Disabled:Script Enforcement``) is not enabled
* Dynamic Code Security (``19 Enabled:Dynamic Code Security``) is enabled

The supplemental policy then should then add the certificate as a trusted publisher to the supplemental policy and apply that to the Windows host. This is an example policy configuration that contains a trusted publisher:

.. code-block:: xml
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

Once the policy is created and the certificate that will be used to sign the Ansible content is trusted, the policy can be applied to the Windows host.

.. Warning::
     As Ansible typically runs tasks as an Adminstrator, it is important that the policy is signed and is applied so that Ansible cannot unset the policy through a task like ``win_file`` or ``win_regedit``.

How to Sign Scripts
-------------------
Once the code signing certificate has been generated and trusted by the Windows host, it can be used to sign the scripts that Ansible will run. The below PowerShell script can be used to sign both the Ansible internal execution scripts as well as any PowerShell collection content. It requires the following to run:

* PowerShell 7.2 or later
* The `OpenAuthenticode <https://github.com/jborean93/PowerShell-OpenAuthenticode>`_ PowerShell module
* Python with Ansible and the required collections installed
* Access to the certificate private key trusted by the App Control policy

.. literalinclude:: powershell/New-AnsiblePowerShellSignature.ps1
   :language: powershell

To sign the Ansible content, and modules in a collection, the following PowerShell script can be used with the loaded function from above:

.. code-block:: powershell

   $certPassword = Read-Host "Enter the password for the certificate" -AsSecureString
   $cert = [System.Security.Cryptography.X509Certificates.X509Certificate2]::new(
      "wdac-cert.pfx"
      $certPassword)

   $collections = @(
       # Includes all the builtin execution wrappers and scripts needed for Ansible
       'ansible.builtin'

       # Add any remaining collections used in the playbook like microsoft.ad, community.windows, etc.
       'ansible.windows'
   )
   New-AnsiblePowerShellSignature -Certificate $cert -Verbose -Collection $collections

The ``ansible.builtin`` collection refers to the builtin execution scripts used in Ansible. Any other collection used in the playbook should be added to the ``-Collection`` parameter. The script will generate the ``powershell_signatures.ps1`` script signed by the certificate and contains the hashes of all the modules in the collection that should be trusted to run. It will also generate the signature for Ansible's execution wrapper script in the Ansible installation directory so that Ansible can automatically run the script trusted by the App Control policy. The current behaviour of ``New-AnsiblePowerShellSignature`` is to sign all the modules in the collection and the Ansible execution wrapper script even if they could include an escape hatch. It is recommended to skip any modules using the ``-Skip`` parameter that are not needed in the playbook.

.. code-block:: powershell

   New-AnsiblePowerShellSignature ... -Skip @(
       'ansible.windows.win_updates'
       'ansible.windows.win_dsc'
   )

Any PowerShell content that is not part of a collection, like a custom script or code used in ``ansible.windows.win_powershell``, must be signed manually using the ``Set-AuthenticodeSignature`` cmdlet on Windows or ``Set-OpenAuthenticodeSignature`` using the ``OpenAuthenticode`` module on Linux. It is important that these signed scripts are used in a way that will not modify the contents of the script or else the signature will be invalidated. For example the ``ansible.builtin.script`` module will copy the script file to the target host as is an execute it leaving the signature intact. But using the ``ansible.builtin.file`` lookup will strip any remaining newline characters unless the ``rstrip=False`` option is used.

.. note::
   The ``New-AnsiblePowerShellSignature`` function is a tech preview and may change in future releases.

Known Module Differences
------------------------
When App Control is enabled, some modules may not work as expected or at all even if signed. Some of the known differences are:

* ``ansible.windows.win_command`` can only execute executables trusted by the App Control policy. If the executable is not trusted, the module will fail
* ``ansible.windows.win_shell`` will run in Constrained Language Mode (``CLM``) which is highly restricted and may cause some scripts to fail
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

Either the signed script can be placed include in the ``script`` option or the ``ansible.builtin.file`` lookup can be used to read the script from the filesystem. It is important to ensure that the ``file`` lookup is not going to strip any newline characters from the script to keep the signature intact.

.. code-block:: yaml

   - name: Run signed script through script module
     ansible.builtin.script: signed-script.ps1

   - name: Run signed script through win_powershell module
     ansible.windows.win_powershell:
       script: "{{ lookup('ansible.builtin.file', 'signed-script.ps1', rstrip=False) }}"

   - name: Run signed script through win_powershell module with inlined script
     ansible.windows.win_powershell:
       script: |
         $ExecutionContext.SessionState.LanguageMode

         # SIG # Begin signature block
         # MIIFwAYJKoZIhvcNAQcCoIIFsTCCBa0CAQMxDTALBglghkgBZQMEAgEwewYKKwYB
         ...
         # SIG # End signature block

.. note::
   Using the ``win_powershell`` method will read the script file as a UTF-8 encoded script. This may cause signature validation issues if the script is not UTF-8 encoded when signed or was signed with UTF-8 + BOM.
