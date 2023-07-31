.. _installing_distros:

Installing Ansible on specific operating systems
================================================

.. note:: These instructions are provided by their respective communities. Any bugs/issues should be filed with that community to update these instructions. Ansible maintains only the ``pip install`` instructions.

The ``ansible`` package can always be :ref:`installed from PyPI using pip <intro_installation_guide>` on most systems but it is also packaged and maintained by the community for a variety of Linux distributions.

The following instructions will guide you through installing the ``ansible`` package with your preferred distribution's package manager.

.. note:: For maintainers who wish to add distributions to this guide, installation instructions are included here only for distributions with a reasonably up-to-date version of ``ansible``. The distribution MUST ensure that ``ansible-core`` and ``ansible`` versions are kept in sync to the extent that the distribution build system allows. Maintainers MUST include a way to contact them with their instructions here and are encouraged to join the `Ansible Packaging <https://matrix.to/#/#packaging:ansible.com>`_ Matrix room.

.. contents::
  :local:

Installing Ansible on Fedora Linux
-------------------------------------------------

To install the batteries included ``ansible`` package on Fedora run

.. code-block:: bash

    $ sudo dnf install ansible

If you prefer to install the minimal ``ansible-core`` package run

.. code-block:: bash

    $ sudo dnf install ansible-core

Several Ansible collections are also available from the Fedora repositories as
standalone packages that users can install alongside ``ansible-core``.
For example, to install the ``community.general`` collection run

.. code-block:: bash

   $ sudo dnf install ansible-collection-community-general

See the `Fedora Packages index <https://packages.fedoraproject.org/search?query=ansible-collection>`_
for a full list of Ansible collections packaged in Fedora.


Please `file a bug <https://bugzilla.redhat.com/enter_bug.cgi>`_ against the
``Fedora`` product in Red Hat Bugzilla to reach the package maintainers.

Installing Ansible from EPEL
----------------------------------

Users of CentOS Stream, Almalinux, Rocky Linux, and related distributions
can install ``ansible`` or Ansible collections from the community maintained
`EPEL <https://docs.fedoraproject.org/en-US/epel/>`_
(Extra Packages for Enterprise Linux) repository.

After `enabling the EPEL repository <https://docs.fedoraproject.org/en-US/epel/#_quickstart>`_,
users can use the same ``dnf`` commands as for Fedora Linux.

Please `file a bug <https://bugzilla.redhat.com/enter_bug.cgi>`_ against the
``Fedora EPEL`` product in Red Hat Bugzilla to reach the package maintainers.


Installing Ansible on OpenSUSE Tumbleweed/Leap
----------------------------------------------

.. code-block:: bash

    $ sudo zypper install ansible
    
See `OpenSUSE Support Portal <https://en.opensuse.org/Portal:Support>` for additional help with Ansible on OpenSUSE.

.. _from_apt:

Installing Ansible on Ubuntu
----------------------------

Ubuntu builds are available `in a PPA here <https://launchpad.net/~ansible/+archive/ubuntu/ansible>`_.

To configure the PPA on your system and install Ansible run these commands:

.. code-block:: bash

    $ sudo apt update
    $ sudo apt install software-properties-common
    $ sudo add-apt-repository --yes --update ppa:ansible/ansible
    $ sudo apt install ansible

.. note:: On older Ubuntu distributions, "software-properties-common" is called "python-software-properties". You may want to use ``apt-get`` rather than ``apt`` in older versions. Also, be aware that only newer distributions (that is, 18.04, 18.10, and later) have a ``-u`` or ``--update`` flag. Adjust your script as needed.

Please file issues `here <https://github.com/ansible-community/ppa/issues>`_.


Installing Ansible on Debian
----------------------------

While Ansible is available from the `main Debian repository <https://packages.debian.org/stable/ansible>`_, it can be out-of-date.

To get a more recent version Debian users can use the Ubuntu PPA according to the following table:

.. list-table::
  :header-rows: 1

  * - Debian
    -
    - Ubuntu
    - UBUNTU_CODENAME
  * - Debian 12 (Bookworm)
    - ->
    - Ubuntu 22.04 (Jammy)
    - jammy
  * - Debian 11 (Bullseye)
    - ->
    - Ubuntu 20.04 (Focal)
    - focal
  * - Debian 10 (Buster)
    - ->
    - Ubuntu 18.04 (Bionic)
    - bionic

In the following we assume that you have installed wget and gpg (`sudo apt install wget gpg`).

Run the following commands to add the repository and install Ansible.
Replace the export of UBUNTU_CODENAME as per the table above (in this example we use jammy).

.. code-block:: bash

    $ UBUNTU_CODENAME=jammy
    $ wget -O- "https://keyserver.ubuntu.com/pks/lookup?fingerprint=on&op=get&search=0x6125E2A8C77F2818FB7BD15B93C4A3FD7BB9C367" | sudo gpg --dearmour -o /usr/share/keyrings/ansible-archive-keyring.gpg
    $ echo "deb [signed-by=/usr/share/keyrings/ansible-archive-keyring.gpg] http://ppa.launchpad.net/ansible/ansible/ubuntu $UBUNTU_CODENAME main" | sudo tee /etc/apt/sources.list.d/ansible.list
    $ sudo apt update && sudo apt install ansible

Note: the " " around the keyserver URL are important.
Around the "echo deb" it is important to use " " rather than ' '.

These commands download the signing key and add an entry to apt's sources pointing to the PPA.

Previously you may haved used `apt-key add`.
This is now deprecated for security reasons (on Debian, Ubuntu, and elsewhere).
For more details see `this AskUbuntu post <https://askubuntu.com/a/1307181>`_.
Also note that for security reasons we do NOT add the key to `/etc/apt/trusted.gpg.d/` or `/etc/apt/trusted.gpg` where it would be allowed to sign releases from ANY repository.

.. _from_windows:

Installing Ansible on Windows
------------------------------

You cannot use a Windows system for the Ansible control node. See :ref:`windows_faq_ansible`

.. seealso::

    `Installing Ansible on Arch Linux <https://wiki.archlinux.org/title/Ansible#Installation>`_
       Distro-specific installation on Arch Linux
    `Installing Ansible on Clear Linux <https://clearlinux.org/software/bundle/ansible>`_
       Distro-specific installation on Clear Linux
