.. _windows_performance:

Windows performance
===================
This document offers some performance optimizations you might like to apply to
your Windows hosts to speed them up specifically in the context of using Ansible
with them, and generally.

Optimize PowerShell performance to reduce Ansible task overhead
---------------------------------------------------------------
To speed up the startup of PowerShell by around 10x, run the following
PowerShell snippet in an Administrator session. Expect it to take tens of
seconds.

.. note::

    If native images have already been created by the ngen task or service, you
    will observe no difference in performance (but this snippet will at that
    point execute faster than otherwise).

.. code-block:: powershell

    function Optimize-Assemblies {
        param (
            [string]$assemblyFilter = "Microsoft.PowerShell.",
            [string]$activity = "Native Image Installation"
        )
    
        try {
            # Get the path to the ngen executable dynamically
            $ngenPath = [System.IO.Path]::Combine([Runtime.InteropServices.RuntimeEnvironment]::GetRuntimeDirectory(), "ngen.exe")
    
            # Check if ngen.exe exists
            if (-Not (Test-Path $ngenPath)) {
                Write-Host "Ngen.exe not found at $ngenPath. Make sure .NET Framework is installed."
                return
            }
    
            # Get a list of loaded assemblies
            $assemblies = [AppDomain]::CurrentDomain.GetAssemblies()
    
            # Filter assemblies based on the provided filter
            $filteredAssemblies = $assemblies | Where-Object { $_.FullName -ilike "$assemblyFilter*" }
    
            if ($filteredAssemblies.Count -eq 0) {
                Write-Host "No matching assemblies found for optimization."
                return
            }
    
            foreach ($assembly in $filteredAssemblies) {
                # Get the name of the assembly
                $name = [System.IO.Path]::GetFileName($assembly.Location)
    
                # Display progress
                Write-Progress -Activity $activity -Status "Optimizing $name"
    
                # Use Ngen to install the assembly
                Start-Process -FilePath $ngenPath -ArgumentList "install `"$($assembly.Location)`"" -Wait -WindowStyle Hidden
            }
    
            Write-Host "Optimization complete."
        } catch {
            Write-Host "An error occurred: $_"
        }
    }
    
    # Optimize PowerShell assemblies:
    Optimize-Assemblies -assemblyFilter "Microsoft.PowerShell."

PowerShell is used by every Windows Ansible module. This optimization reduces
the time PowerShell takes to start up, removing that overhead from every invocation.

This snippet uses `the native image generator, ngen <https://docs.microsoft.com/en-us/dotnet/framework/tools/ngen-exe-native-image-generator#WhenToUse>`_
to preemptively create native images for the assemblies that PowerShell relies on.

Fix high-CPU-on-boot for VMs/cloud instances
--------------------------------------------
If you are creating golden images to spawn instances from, you can avoid a disruptive
high CPU task near startup through `processing the ngen queue <https://docs.microsoft.com/en-us/dotnet/framework/tools/ngen-exe-native-image-generator#native-image-service>`_
within your golden image creation, if you know the CPU types won't change between
golden image build process and runtime.

Place the following near the end of your playbook, bearing in mind the factors that can cause native images to be invalidated (`see MSDN <https://docs.microsoft.com/en-us/dotnet/framework/tools/ngen-exe-native-image-generator#native-images-and-jit-compilation>`_).

.. code-block:: yaml

    - name: generate native .NET images for CPU
      win_dotnet_ngen:


