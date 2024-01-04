# Cautionary Note on ConfigureRemotingForAnsible.ps1
`ConfigureRemotingForAnsible.ps1` is a script designed to check the current WinRM (PS Remoting) configuration and makes the necessary changes to allow Ansible to connect, authenticate and execute PowerShell commands. However, recent user experiences have raised concerns about its reliability and potential for causing issues.


**Warning:**
We strongly advised against using `ConfigureRemotingForAnsible.ps1` due to several potential issues which are:

* It enables Basic authentication:

    * Windows has this disabled by default because it is not secure when running over HTTP.
    * Over HTTP this is an issue because the messages are not encrypted, even the credentials are just base64 encoded
    * Anyone sniffing the network will be able to get your credentials as well as any data that Ansible sends to the remote host and what it receives back.
    * Requires HTTPS to be set up to be secure, even then it's problematic because it only supports local account and not domain accounts.
* It creates a self signed certificate
    * Fine for basic testing but in a domain environment you should be using your own CA issued certificates for the host.
    * Also it creates both a HTTP and HTTPS listener, where only the latter is enabled by default. Not really an issue but some places like to reduce the amount of inbound entrypoints as much as they can.
* It allows WinRM traffic in all network profiles
    * Usually you want to restrict traffic to just the network/profile you will be managing it from.

A lot of these settings are done (Basic auth and HTTPS with self signed certificate) because it was created in a time where the WinRM support on Python was very basic and barebones. There was no *NTLM* or *Kerberos* support, no message encryption over HTTP. This is no longer the case and the Python WinRM library that is used supports the full gauntlet of authentication protocols WinRM supports as well as message encryption when it's run over HTTP. In fact, Ansible has been able to connect to a Windows host that has already run `Enable-PSRemoting` in PowerShell already. There's really no need to use this script at all as the defaults in Windows are just fine.

The reason why we still have this script is simple, people still use it and have their scripts set to download it directly from GitHub. If we were to remove it, or even just some of the default behaviour to be a bit more secure we will be breaking plenty of scripts that still rely on its current behaviour.


**TLDR:** We are trying to discourage users from using the script as much as we can. It was created for a time where Ansible couldn't work with the default WinRM settings. If you do wish to use it then take a copy of the script and only run the parts you need, i.e. self signed certificates and so on.

