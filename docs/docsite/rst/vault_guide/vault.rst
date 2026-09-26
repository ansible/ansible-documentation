.. _vault:

*************
Ansible Vault
*************

Ansible Vault encrypts variables and files so you can protect sensitive content such as passwords or keys rather than leaving it visible as plaintext in playbooks or roles.
To use Ansible Vault you need one or more passwords to encrypt and decrypt content.
If you store your vault passwords in a third-party tool such as a secret manager, you need a script to access them.
Use the passwords with the :ref:`ansible-vault` command-line tool to create and view encrypted variables, create encrypted files, encrypt existing files, or edit, re-key, or decrypt files.
You can then place encrypted content under source control and share it more safely.

.. warning::
    * Before Ansible Core version 2.22, encryption with Ansible Vault ONLY protected 'data at rest'.  Once the content was decrypted ('data in use'), play and plugin authors were responsible for avoiding any secret disclosure.
    * After Ansible Core version 2.22, vaulted data is automatically marked as ``secret`` and Ansible will attempt to prevent disclosure. Third party plugins are still responsible for following security conventions.
    * see :ref:`no_log <keep_secret_data>` for details on hiding output and :ref:`vault_securing_editor` for security considerations on editors you use with Ansible Vault.

You can use encrypted variables and files in ad hoc commands and playbooks by supplying the passwords you used to encrypt them.
You can modify your ``ansible.cfg`` file to specify the location of a password file or to always prompt for the password.
