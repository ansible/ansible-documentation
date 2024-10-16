# Update on maintenance of scripts `ConfigureRemotingForAnsible.ps1`

## Important Notice
This is to notify users that the aforementioned script is currently unmaintained and may be removed in the future. Please read this notice carefully before using the script.

### Why Unmaintained ?
The script is designed to check the current WinRM (PS Remoting) configuration and make the necessary changes to allow Ansible to connect, authenticate and execute PowerShell commands. As of now, Ansible can connect to Windows host that has already run `Enable-PSRemoting` in PowerShell already. 

There's really no need to use this script at all as the defaults in Windows are just fine. Also, using the scripts may result in potential security issues.



### Use at Your Own Risk
- The script is provided as-is, without ongoing support or updates.
- Use them at your own risk, and carefully consider the potential consequences. 