.. _installing_distros:

Installing Ansible on specific operating systems
================================================

.. note:: 
   These instructions come from their respective communities. 
   If you encounter bugs or issues, file them with that community to update these instructions. 
   Ansible maintains only the ``pip install`` instructions.

You can always :ref:`install the ansible package from PyPI using pip <intro_installation_guide>` on most systems.
The community also packages and maintains Ansible for various Linux distributions.

This guide shows you how to install Ansible from different distribution package repositories.

Requirements for adding new distributions
-----------------------------------------

Package maintainers who want to add instructions for another distribution to this guide must meet the following requirements:

* Ensure the distribution provides a reasonably up-to-date version of ``ansible``.
* Keep ``ansible-core`` and ``ansible`` versions synchronized to the extent that the build system allows.
* Provide a way to contact the distribution maintainers as part of the instructions.
* Distribution maintainers are also encouraged to join and monitor the `Ansible Packaging <https://matrix.to/#/#packaging:ansible.com>`_ Matrix room.

.. contents::
  :local:

Installing Ansible on Fedora Linux
----------------------------------

Fedora Linux provides both the full Ansible package and the minimal ansible-core package through the standard repositories.

Install the full ``ansible`` package:

.. code-block:: bash

    $ sudo dnf install ansible

Install the minimal ``ansible-core`` package:

.. code-block:: bash

    $ sudo dnf install ansible-core

Fedora repositories include several Ansible collections as standalone packages that you can install alongside ``ansible-core``.
For example, install the ``community.general`` collection:

.. code-block:: bash

   $ sudo dnf install ansible-collection-community-general

See the `Fedora Packages index <https://packages.fedoraproject.org/search?query=ansible-collection>`_
for a complete list of Ansible collections packaged in Fedora.

Contact the package maintainers by `filing a bug <https://bugzilla.redhat.com/enter_bug.cgi>`_ against the ``Fedora`` product in Red Hat Bugzilla.

Installing Ansible from EPEL
----------------------------


If you use CentOS Stream, Almalinux, Rocky Linux, or related distributions, you can install ``ansible`` or Ansible collections from the community-maintained `EPEL <https://docs.fedoraproject.org/en-US/epel/>`_ (Extra Packages for Enterprise Linux) repository:

1. `Enable the EPEL repository <https://docs.fedoraproject.org/en-US/epel/#_quickstart>`_.
2. Use the same ``dnf`` commands as for Fedora Linux.

Contact the package maintainers by `filing a bug <https://bugzilla.redhat.com/enter_bug.cgi>`_ against the ``Fedora EPEL`` product in Red Hat Bugzilla.

Installing Ansible on OpenSUSE Tumbleweed/Leap
----------------------------------------------

OpenSUSE provides Ansible packages through the standard package manager.

.. code-block:: bash

    $ sudo zypper install ansible

See the `OpenSUSE Support Portal <https://en.opensuse.org/Portal:Support>`_ for additional help with Ansible on OpenSUSE.

.. _from_apt:

Installing Ansible on Ubuntu
----------------------------

Ubuntu provides Ansible packages through a Personal Package Archive (PPA) that contains more recent versions than the standard repositories.

Ubuntu builds are available `in a PPA here <https://launchpad.net/~ansible/+archive/ubuntu/ansible>`_.

Configure the PPA on your system and install Ansible:

.. code-block:: bash

    $ sudo apt update
    $ sudo apt install software-properties-common
    $ sudo add-apt-repository --yes --update ppa:ansible/ansible
    $ sudo apt install ansible

.. note:: 
   On older Ubuntu distributions, "software-properties-common" is called "python-software-properties". 
   You may want to use ``apt-get`` rather than ``apt`` in older versions. 
   Also, only newer distributions (18.04, 18.10, and later) have a ``-u`` or ``--update`` flag. 
   Adjust your script as needed.

File any issues in `the PPA's issue tracker <https://github.com/ansible-community/ppa/issues>`_.

Installing Ansible on Debian
----------------------------

Debian users can choose between the standard repository or the Ubuntu PPA for more recent versions.

While Ansible is available from the `main Debian repository <https://packages.debian.org/stable/ansible>`_, this version can be outdated.

For a more recent version, Debian users can use the Ubuntu PPA according to the following table:

.. list-table::
  :header-rows: 1

  * - Debian
    -
    - Ubuntu
    - UBUNTU_CODENAME
  * - Debian 12 (Bookworm)
    - ->
    - Ubuntu 22.04 (Jammy)
    - ``jammy``
  * - Debian 11 (Bullseye)
    - ->
    - Ubuntu 20.04 (Focal)
    - ``focal``
  * - Debian 10 (Buster)
    - ->
    - Ubuntu 18.04 (Bionic)
    - ``bionic``

The following example assumes that you already have ``wget`` and ``gpg`` installed.

Add the repository and install Ansible.
Set ``UBUNTU_CODENAME=...`` based on the table above (we use ``jammy`` in this example):

.. code-block:: bash

    $ UBUNTU_CODENAME=jammy
    $ wget -O- "https://keyserver.ubuntu.com/pks/lookup?fingerprint=on&op=get&search=0x6125E2A8C77F2818FB7BD15B93C4A3FD7BB9C367" | sudo gpg --dearmour -o /usr/share/keyrings/ansible-archive-keyring.gpg
    $ echo "deb [signed-by=/usr/share/keyrings/ansible-archive-keyring.gpg] http://ppa.launchpad.net/ansible/ansible/ubuntu $UBUNTU_CODENAME main" | sudo tee /etc/apt/sources.list.d/ansible.list
    $ sudo apt update && sudo apt install ansible

.. note::
   Use double quotes around the keyserver URL and in the "echo deb" command like in the example above.

These commands download the signing key and add an entry to apt's sources pointing to the PPA.

Previously, you may have used ``apt-key add``.
The ``apt-key add`` approach is now `deprecated <https://askubuntu.com/a/1307181>`_ for security reasons (on Debian, Ubuntu, and elsewhere).

As such, we do NOT add the key to ``/etc/apt/trusted.gpg.d/`` or to ``/etc/apt/trusted.gpg`` where the key would be allowed to sign releases from ANY repository.

Installing Ansible on Arch Linux
--------------------------------

Arch Linux provides both the full Ansible package and ansible-core through the standard package repositories.

Install the full ``ansible`` package:

.. code-block:: bash

    $ sudo pacman -S ansible

Install the minimal ``ansible-core`` package:

.. code-block:: bash

    $ sudo pacman -S ansible-core

Arch Linux repositories include several Ansible ecosystem packages as standalone packages that you can install alongside ``ansible-core``.
See the `Arch Linux Packages index <https://archlinux.org/packages/?sort=&q=ansible>`_ for a complete list of Ansible packages in Arch Linux.

Contact the package maintainers by `opening an issue <https://gitlab.archlinux.org/archlinux/packaging/packages>`_ in the related package GitLab repository.

.. _from_windows:

Installing Ansible on Windows
-----------------------------

You cannot use a Windows system for the Ansible control node. See :ref:`windows_control_node`

.. seealso::

    `Installing Ansible on Arch Linux <https://wiki.archlinux.org/title/Ansible#Installation>`_
       Distro-specific installation on Arch Linux
    `Installing Ansible on Clear Linux <https://clearlinux.org/software/bundle/ansible>`_
       Distro-specific installation on Clear Linux
