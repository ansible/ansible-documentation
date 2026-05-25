.. _windows_pwsh:

PowerShell 7 Support
====================

.. contents::
   :local:

Starting with ``ansible-core`` version 2.21, Ansible supports PowerShell 7 (``pwsh``) as an alternative to Windows PowerShell 5.1 for executing PowerShell modules. This enables cross-platform PowerShell module execution on both Windows and non-Windows systems as well as access to the latest PowerShell features and improvements.


Interpreter Configuration
-------------------------

The ``ansible_pwsh_interpreter`` variable specifies which PowerShell executable to use when running PowerShell modules.

**Path requirements:**

* **Windows**: Supports both absolute paths (``C:\Program Files\PowerShell\7\pwsh.exe``) and relative paths/executable names (``pwsh``, which searches PATH)
* **Linux/macOS**: Requires absolute paths only (``/usr/bin/pwsh``, ``/opt/microsoft/powershell/7/pwsh``)

**Default behavior:**

The default interpreter is determined by the module's shebang line and target platform:

* **Windows**:

  * Modules with ``#!powershell`` shebang → ``C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`` (Windows PowerShell 5.1)
  * Modules with ``#!/usr/bin/pwsh`` shebang → ``pwsh`` (PowerShell 7, searches PATH)
  * This ensures backwards compatibility with existing modules while allowing opt-in to PowerShell 7

* **Linux/macOS**:

  * All modules default to ``/usr/bin/pwsh`` (PowerShell 7) regardless of shebang

**Examples:**

The variable can be set per play, or task like the below:

.. code-block:: yaml

   # Use PowerShell 7 on Windows (relative path)
   - hosts: windows_servers
     vars:
       ansible_pwsh_interpreter: pwsh

   # Use PowerShell 7 on Windows (absolute path)
   - hosts: windows_servers
     vars:
       ansible_pwsh_interpreter: C:\Program Files\PowerShell\7\pwsh.exe

   # Use PowerShell 7 on Linux (absolute path required)
   - hosts: linux_servers
     vars:
       ansible_pwsh_interpreter: /usr/bin/pwsh

   # Use custom PowerShell installation on Linux
   - hosts: linux_servers
     vars:
       ansible_pwsh_interpreter: /opt/microsoft/powershell/7/pwsh

   # Use Windows PowerShell 5.1 explicitly on Windows
   - hosts: windows_legacy
     vars:
       ansible_pwsh_interpreter: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe

When setting the variable in an ini inventory file, the value should be quoted if it contains whitespace and is part of a host declaration but should be unquoted when set by itself. For example:

.. code-block:: ini

    [windows]
    # Quotes required for host variable since it contains spaces
    win-host  ansible_pwsh_interpreter="C:\Program Files\PowerShell\7\pwsh.exe"

    [windows:vars]
    # Quotes not required for group variable since it is the only variable on the line
    ansible_pwsh_interpreter=C:\Program Files\PowerShell\7\pwsh.exe


Module Shebang Support
----------------------

PowerShell modules specify their interpreter using shebang lines, which determines the default PowerShell version when ``ansible_pwsh_interpreter`` is not set. The two shebang formats officially supported for PowerShell based modules are:

.. code-block:: powershell

   #!powershell
   #!/usr/bin/pwsh

* **``#!powershell``**: Targets Windows PowerShell 5.1 compatibility

  * Windows: Uses ``powershell.exe`` (5.1) by default
  * Linux/macOS: Still uses ``/usr/bin/pwsh`` (cross-platform PowerShell 7)
  * Use for modules that need to work on older Windows systems without PowerShell 7

* **``#!/usr/bin/pwsh``**: Targets PowerShell 7

  * Windows: Uses ``pwsh.exe`` (PowerShell 7) by default
  * Linux/macOS: Uses ``/usr/bin/pwsh`` (PowerShell 7)
  * Use for modules requiring PowerShell 7+ features or cross-platform compatibility

It is possible to use a custom shebang line for PowerShell modules on non-Windows platforms as long as the filename specified by the shebang is ``pwsh`` but this is not officially supported and thoroughly tested. It is recommended to use ``#!/usr/bin/pwsh`` and control the interpreter used through the ``ansible_pwsh`_interpreter`` variable when running on non-Windows platforms to ensure consistent behavior.


Cross-Platform PowerShell Modules
---------------------------------

As PowerShell modules can run on either Windows or non-Windows platforms, there are a few tricks that make it easier to write cross-platform compatible modules that work well with both Windows PowerShell 5.1 and PowerShell 7:

**Use platform checks:**

.. code-block:: powershell

   #!powershell

   #AnsibleRequires -CSharpUtil Ansible.Basic

   $spec = @{
       options = @{
           path = @{ type = "str"; required = $true }
       }
   }

   $module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

   # Set $IsWindows for PowerShell 5.1 to simplify future platform checks.
   if (-not (Get-Variable -Name IsWindows -ErrorAction Ignore)) {
       $IsWindows = $true
   }

   # Check platform using PowerShell 7 automatic variables
   if ($IsWindows) {
       # Windows-specific logic
   } elseif ($IsLinux) {
       # Linux-specific logic
   } elseif ($IsMacOS) {
       # macOS-specific logic
   }

   # Check if running on WinPS or Pwsh 7
   if ($IsCoreCLR) {
       # PowerShell 7 specific logic
   } else {
       # Windows PowerShell 5.1 specific logic
   }

   if ($PSVersionTable.PSVersion -lt '6.0') {
       # Windows PowerShell 5.1 specific logic
   } else {
       # PowerShell 7 specific logic
   }

**Avoid Windows-specific cmdlets and APIs:**

* Many Windows cmdlets (like ``Get-WmiObject``, ``Get-ComputerInfo``) are not available on non-Windows platforms
* Use cross-platform alternatives when possible
* Rely on .NET APIs that are supported in targeted platforms
* Test on multiple platforms
* Document platform requirements clearly in module documentation
* Use platform checks to conditionally execute platform-specific code paths when necessary


Verifying Configuration
-----------------------

The simplest way to check which PowerShell version Ansible is using is to run ``ansible.windows.win_powershell`` to output ``$PSVersionTable.PSVersion`` variable:

.. code-block:: yaml

   - name: Display PowerShell version info
     ansible.windows.win_powershell:
       script: $PSVersionTable.PSVersion.ToString()
     register:
       ps_version: _task.result.output[0]

   - debug:
       var: ps_version


The ``ansible.windows.win_powershell`` module by default runs in the same interpreter context as other PowerShell modules, so it can be used to verify any PowerShell details about the target node's PowerShell environment, such as installed modules, available cmdlets, and more.


PSRP Configuration Name
-----------------------

When using the ``ansible.builtin.psrp`` connection plugin, aligning the PSRemoting session configuration with your desired PowerShell interpreter improves performance significantly.

If the PSRemoting session configuration does not match the PowerShell interpreter specified by ``ansible_pwsh_interpreter``, PSRP must launch a new PowerShell process for each task. This creates extra overhead and slows down playbook execution. By matching the session configuration to your interpreter, modules execute directly in the correct PowerShell environment without process spawning.

**Configuration:**

Use the ``ansible_psrp_configuration_name`` variable to specify which PowerShell session configuration to use:

* **``Microsoft.PowerShell``** (default): Uses Windows PowerShell 5.1
* **``PowerShell.7``**: Uses PowerShell 7

PowerShell 7 typically registers the ``PowerShell.7`` session configuration during installation when the option is selected, or when ``Enable-PSRemoting`` is run from within the PowerShell 7 interpreter.

**Example for PowerShell 7:**

.. code-block:: ini

   [windows:vars]
   ansible_connection=psrp
   ansible_pwsh_interpreter=C:\Program Files\PowerShell\7\pwsh.exe
   ansible_psrp_configuration_name=PowerShell.7

**Verifying session configurations:**

To see available session configurations on a Windows host:

.. code-block:: powershell

   Get-PSSessionConfiguration | Select-Object Name, PSVersion


See Also
========

* :ref:`target_node_windows_support` - PowerShell lifecycle and support policy
* :ref:`windows_setup` - Setting up Windows hosts
* :ref:`windows_usage` - Using Ansible with Windows
* :ref:`developing_modules_general_windows` - Developing Windows modules
* `PowerShell 7 Documentation <https://learn.microsoft.com/powershell/scripting/whats-new/what-s-new-in-powershell-7>`_
