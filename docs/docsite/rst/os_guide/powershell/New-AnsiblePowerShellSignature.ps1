#Requires -Module OpenAuthenticode

using namespace System.Collections.Generic
using namespace System.IO
using namespace System.Management.Automation
using namespace System.Management.Automation.Language
using namespace System.Security.Cryptography.X509Certificates

Function New-AnsiblePowerShellSignature {
    <#
    .SYNOPSIS
    Creates and signed Ansible content for WDAC.

    .DESCRIPTION
    This function will generate the powershell_signatures.ps1 manifest and sign
    it. The manifest file includes all PowerShell/C# module_utils and
    PowerShell modules in the collection(s) specified. It will also create the
    '*.authenticode' signature files for any PowerShell scripts found in the
    collections plugins/plugin_utils/powershell directories.

    .PARAMETER Certificate
    The certificate to use for signing the content.

    .PARAMETER Collection
    The collection(s) to sign. This is set to ansible.builtin by default but
    can be overriden to include other collections like ansible.windows.

    .PARAMETER Skip
    A list of plugins to skip by the fully qualified name. Plugins skipped will
    be marked as unsupported in the manifest and will error when being run.
    Scripts skipped are just ignored and will not have its '.authenticode'
    signature file created.

    The values in the list should be the fully qualified name of the plugin as
    referenced in Ansible. The value can also optionally include the extension
    of the file if the FQN is ambigious, e.g. collection util that has both a
    PowerShell and C# util of the same name.

    Here are some examples for the various content types:

        # Ansible Builtin Modules
        'ansible.builtin.module_name'

        # Ansible Builtin ModuleUtil
        'Ansible.ModuleUtils.PowerShellUtil'
        'Ansible.CSharpUtil'

        # Collection Modules
        'namespace.name.module_name'

        # Collection ModuleUtils
        'ansible_collections.namespace.name.plugins.module_utils.PowerShellUtil'
        'ansible_collections.namespace.name.plugins.module_utils.PowerShellUtil.psm1'

        'ansible_collections.namespace.name.plugins.module_utils.CSharpUtil'
        'ansible_collections.namespace.name.plugins.module_utils.CSharpUtil.cs'

        # Collection Scripts
        'ansible_collections.namespace.name.plugins.plugin_utils.powershell.script'

    .PARAMETER TimeStampServer
    Optional authenticode timestamp server to use when signing the content.

    .EXAMPLE
    Signs just the content included in Ansible.

        $cert = [X509Certificate2]::new("wdac-cert.pfx", "password")
        New-AnsiblePowerShellSignature -Certificate $cert

    .EXAMPLE
    Signs just the content include in Ansible and the ansible.windows collection

        $cert = [X509Certificate2]::new("wdac-cert.pfx", "password")
        New-AnsiblePowerShellSignature -Certificate $cert -Collection ansible.builtin, ansible.windows

    .EXAMPLE
    Signs just the content in the ansible.windows collection

        $cert = [X509Certificate2]::new("wdac-cert.pfx", "password")
        New-AnsiblePowerShellSignature -Certificate $cert -Collection ansible.windows

    .EXAMPLE
    Signs content but skips the specified modules and module_utils
        $skip = @(
            # Skips the module specified
            'namespace.name.module'

            # Skips the module_utils specified
            'ansible_collections.namespace.name.plugins.module_utils.PowerShellUtil'
            'ansible_collections.namespace.name.plugins.module_utils.CSharpUtil'

            # Skips signing the file specified
            'ansible_collections.namespace.name.plugins.plugin_utils.powershell.file.ps1'
        )
        $cert = [X509Certificate2]::new("wdac-cert.pfx", "password")
        New-AnsiblePowerShellSignature -Certificate $cert -Collection namespace.name -Skip $skip
    #>
    [CmdletBinding()]
    param (
        [Parameter(
            Mandatory
        )]
        [X509Certificate2]
        $Certificate,

        [Parameter(
            ValueFromPipeline,
            ValueFromPipelineByPropertyName
        )]
        [string[]]
        $Collection = "ansible.builtin",

        [Parameter(
            ValueFromPipelineByPropertyName
        )]
        [string[]]
        $Skip = @(),

        [Parameter()]
        [string]
        $TimeStampServer
    )

    begin {
        Write-Verbose "Attempting to get ansible-config dump"

        $env:ANSIBLE_VERBOSITY = "0"
        $env:ANSIBLE_DEVEL_WARNING = "false"
        $env:ANSIBLE_INVENTORY_UNPARSED_WARNING = "false"
        $env:ANSIBLE_NOCOLOR = "true"
        $configRaw = ansible-config dump --format json --type base 2>&1
        if ($LASTEXITCODE) {
            $err = [ErrorRecord]::new(
                [Exception]::new("Failed to get Ansible configuration, RC: ${LASTEXITCODE} - $configRaw"),
                'FailedToGetAnsibleConfiguration',
                [ErrorCategory]::NotSpecified,
                $null)
            $PSCmdlet.ThrowTerminatingError($err)
        }

        $config = $configRaw | ConvertFrom-Json
        $collectionsPaths = @($config | Where-Object name -EQ 'COLLECTIONS_PATHS' | ForEach-Object value)
        Write-Verbose "Collections paths to be searched: [$($collectionsPaths -join ":")]"

        # FIXME: Don't hardcode this list
        $Skip = @(
            $Skip

            # Known to not work, requires more changes
            'ansible.windows.win_updates'
        )

        $signParams = @{
            Certificate = $Certificate
            HashAlgorithm = 'SHA256'
        }
        if ($TimeStampServer) {
            $signParams.TimeStampServer = $TimeStampServer
        }

        $checked = [HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)

        Function New-HashEntry {
            [OutputType([PSObject])]
            [CmdletBinding()]
            param (
                [Parameter(Mandatory, ValueFromPipeline)]
                [FileInfo]
                $File,

                [Parameter(Mandatory)]
                [AllowEmptyString()]
                [string]
                $PluginBase,

                [Parameter()]
                [AllowEmptyCollection()]
                [string[]]
                $Skip = @()
            )

            process {
                $nameWithoutExt = [string]::IsNullOrEmpty($PluginBase) ? $File.BaseName : "$PluginBase.$($File.BaseName)"
                $nameWithExt = "$nameWithoutExt$($File.Extension)"

                $mode = 'Trusted'
                if ($nameWithoutExt -in $Skip -or $nameWithExt -in $Skip) {
                    Write-Verbose "Marking plugin '$nameWithExt' as unsupported as it is in the supplied skip list"
                    $mode = 'Unsupported'
                }

                Write-Verbose "Hashing plugin '$nameWithExt'"
                $hash = Get-FileHash -LiteralPath $File.FullName -Algorithm SHA256
                [PSCustomObject]@{
                    Name = $nameWithExt
                    Hash = $hash.Hash
                    Mode = $mode
                }
            }
        }
    }

    process {
        foreach ($c in $Collection) {
            try {
                if (-not $checked.Add($c)) {
                    Write-Verbose "Skipping already processed collection $c"
                    continue
                }

                $metaPath = $null
                $pathsToSign = [List[FileInfo]]::new()
                $hashedPaths = [List[PSObject]]::new()

                if ($c -eq 'ansible.builtin') {
                    Write-Verbose "Attempting to get Ansible python path"
                    Write-Verbose "Attempting to get Ansible installation path"

                    $ansiblePython = ansible localhost -m debug -a 'var=ansible_playbook_python'
                    $resultStart = ($ansiblePython -join "").IndexOf('{')
                    if ($LASTEXITCODE -or $resultStart -eq -1) {
                        throw "Failed to find Ansible Python Interpreter path, RC: ${LASTEXITCODE} - $ansiblePython"
                    }
                    $python = (($ansiblePython -join "").Substring($resultStart) | ConvertFrom-Json).ansible_playbook_python

                    $ansiblePath = & $python -c "import ansible; print(ansible.__file__)" 2>&1
                    if ($LASTEXITCODE) {
                        throw "Failed to find Ansible installation path, RC: ${LASTEXITCODE} - $ansiblePath"
                    }

                    $ansibleBase = Split-Path -Path $ansiblePath -Parent
                    $metaPath = [Path]::Combine($ansibleBase, 'config')

                    $execWrapper = Get-Item -LiteralPath ([Path]::Combine($ansibleBase, 'executor', 'powershell', 'exec_wrapper.ps1'))
                    $pathsToSign.Add($execWrapper)

                    $ansiblePwshContent = [PSObject[]]@(
                        # These are needed for Ansible and cannot be skipped
                        Get-ChildItem -Path ([Path]::Combine($ansibleBase, 'executor', 'powershell', '*.ps1')) -Exclude "bootstrap_wrapper.ps1" |
                            New-HashEntry -PluginBase "ansible.executor.powershell"

                        # Builtin utils are special where the filename is their FQN
                        Get-ChildItem -Path ([Path]::Combine($ansibleBase, 'module_utils', 'csharp', '*.cs')) |
                            New-HashEntry -PluginBase "" -Skip $Skip
                        Get-ChildItem -Path ([Path]::Combine($ansibleBase, 'module_utils', 'powershell', '*.psm1')) |
                            New-HashEntry -PluginBase "" -Skip $Skip

                        Get-ChildItem -Path ([Path]::Combine($ansibleBase, 'modules', '*.ps1')) |
                            New-HashEntry -PluginBase $c -Skip $Skip
                    )
                    $hashedPaths.AddRange($ansiblePwshContent)
                }
                else {
                    Write-Verbose "Attempting to get collection path for $c"
                    $namespace, $name, $remaining = $c.ToLowerInvariant() -split '\.'
                    if (-not $name -or $remaining) {
                        throw "Invalid collection name '$c', must be in the format 'namespace.name'"
                    }

                    $foundPath = $null
                    foreach ($path in $collectionsPaths) {
                        $collectionPath = [Path]::Combine($path, 'ansible_collections', $namespace, $name)

                        Write-Verbose "Checking if collection $c exists in '$collectionPath'"
                        if (Test-Path -LiteralPath $collectionPath) {
                            $foundPath = $collectionPath
                            break
                        }
                    }

                    if (-not $foundPath) {
                        throw "Failed to find collection path for $c"
                    }

                    Write-Verbose "Using collection path '$foundPath' for $c"

                    $metaPath = [Path]::Combine($foundPath, 'meta')

                    $pwshUtilsPath = [Path]::Combine($foundPath, 'plugins', 'plugin_utils', 'powershell')
                    if (Test-Path -LiteralPath $pwshUtilsPath) {
                        Get-ChildItem -LiteralPath $pwshUtilsPath | ForEach-Object -Process {
                            if ($_.Extension -ne '.ps1') {
                                return
                            }

                            $nameWithoutExt = "ansible_collections.$c.plugins.plugin_utils.powershell.$($File.BaseName)"
                            $nameWithExt = "$nameWithoutExt$($File.Extension)"
                            if ($nameWithoutExt -in $Skip -or $nameWithExt -in $Skip) {
                                Write-Verbose "Skipping script to sign '$nameWithExt' as it is in the supplied skip list"
                                return
                            }

                            $pathsToSign.Add($_)
                        }
                    }

                    $collectionPwshContent = [PSObject[]]@(
                        $utilPath = [Path]::Combine($foundPath, 'plugins', 'module_utils')
                        if (Test-Path -LiteralPath $utilPath) {
                            Get-ChildItem -LiteralPath $utilPath | Where-Object Extension -In '.cs', '.psm1' |
                                New-HashEntry -PluginBase "ansible_collections.$c.plugins.module_utils" -Skip $Skip
                        }

                        $modulePath = [Path]::Combine($foundPath, 'plugins', 'modules')
                        if (Test-Path -LiteralPath $modulePath) {
                            Get-ChildItem -LiteralPath $modulePath | Where-Object Extension -EQ '.ps1' |
                                New-HashEntry -PluginBase $c -Skip $Skip
                        }
                    )
                    $hashedPaths.AddRange($collectionPwshContent)
                }

                $manifest = @(
                    '#AnsibleVersion 1'
                    ''
                    '@{'
                    '    HashList = @('
                    foreach ($content in $hashedPaths) {
                        # To avoid encoding problems with Authenticode and non-ASCII
                        # characters, we escape them as Unicode code points. We also
                        # escape some ASCII control characters that can cause escaping
                        # problems like newlines.
                        $escapedName = [Regex]::Replace(
                            $content.Name,
                            '([^\u0020-\u007F])',
                            { '\u{0:x4}' -f ([uint16][char]$args[0].Value) })

                        $escapedHash = [CodeGeneration]::EscapeSingleQuotedStringContent($content.Hash)
                        $escapedMode = [CodeGeneration]::EscapeSingleQuotedStringContent($content.Mode)
                        "        # $escapedName"
                        "        @{"
                        "            Hash = '$escapedHash'"
                        "            Mode = '$escapedMode'"
                        "        }"
                    }
                    '    )'
                    '}'
                ) -join "`n"
                $manifestPath = [Path]::Combine($metaPath, 'powershell_signatures.ps1')
                Write-Verbose "Creating and signing manifest for $c at '$manifestPath'"
                Set-Content -LiteralPath $manifestPath -Value $manifest -NoNewline

                Set-OpenAuthenticodeSignature -LiteralPath $manifestPath @signParams

                $pathsToSign | ForEach-Object -Process {
                    $tempPath = Join-Path $_.DirectoryName "$($_.BaseName)_tmp.ps1"
                    $_ | Copy-Item -Destination $tempPath -Force

                    try {
                        Write-Verbose "Signing script '$($_.FullName)'"
                        Set-OpenAuthenticodeSignature -LiteralPath $tempPath @signParams

                        $signedContent = Get-Content -LiteralPath $tempPath -Raw
                        $sigIndex = $signedContent.LastIndexOf("`r`n# SIG # Begin signature block`r`n")
                        if ($sigIndex -eq -1) {
                            throw "Failed to find signature block in $($_.FullName)"
                        }

                        # Ignore the first and last \r\n when extracting the signature
                        $sigIndex += 2
                        $signature = $signedContent.Substring($sigIndex, $signedContent.Length - $sigIndex - 2)
                        $sigPath = Join-Path $_.DirectoryName "$($_.Name).authenticode"

                        Write-Verbose "Creating signature file at '$sigPath'"
                        Set-Content -LiteralPath $sigPath -Value $signature -NoNewline
                    }
                    finally {
                        $tempPath | Remove-Item -Force
                    }
                }
            }
            catch {
                $_.ErrorDetails = "Failed to process collection ${c}: $_"
                $PSCmdlet.WriteError($_)
                continue
            }
        }
    }
}
