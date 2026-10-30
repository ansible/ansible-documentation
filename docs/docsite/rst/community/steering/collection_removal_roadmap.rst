..
   THIS DOCUMENT IS OWNED BY THE ANSIBLE COMMUNITY STEERING COMMITTEE. ALL CHANGES MUST BE APPROVED BY THE STEERING COMMITTEE!
   For small changes (fixing typos, language errors, etc.) create a PR and ping @ansible/steering-committee.
   For other changes, create a `community topic <https://forum.ansible.com/new-topic?category=project&tags=community-wg>`_ to discuss them.
   (Creating a draft PR for this file and mentioning it in the community topic is also OK.)

.. _collection_removal_roadmap:

Collection removal roadmap
==========================

This document describes the roadmap for removing collections from the Ansible community package that no longer meet the :ref:`inclusion criteria <steering_inclusion>`.

.. contents:: Topics:

Background
----------

The :ref:`Steering Committee <steering_responsibilities>` tightened the :ref:`collection inclusion criteria <steering_inclusion>` to keep the Ansible community package focused and maintainable. Collections that no longer meet the criteria are scheduled for removal.

The lists below are based on the `ansible.in <https://github.com/ansible-community/ansible-build-data/blob/main/15/ansible.in>`_ file that defines the package contents, excluding collections already scheduled for removal.

All collections listed for removal continue to be available on `Ansible Galaxy <https://galaxy.ansible.com/>`_ and can be installed with ``ansible-galaxy collection install``.

.. _collection_removal_timeline:

Deprecation timeline
--------------------

* **Deprecation announced:** Ansible community package 14 (current release).
* **Removal from package:** Ansible community package 18 (~2 years / 4 major releases later).

The Ansible community package ships approximately two major versions per year, so four major releases correspond to roughly two years.
This period is chosen because:

* These are collections users actively depend on in playbooks and roles.
* Users will have enough time to adjust CI/CD pipelines and add explicit ``ansible-galaxy collection install`` steps.
  * The collections are not disappearing from Galaxy, just from the bundled package — the migration path is straightforward.

.. _collections_to_keep:

Collections to keep (22)
------------------------

Core Ansible infrastructure
^^^^^^^^^^^^^^^^^^^^^^^^^^^

* `ansible.netcommon <https://github.com/ansible-collections/ansible.netcommon>`_ — provides shared plugins and module utilities for automating the management of network, security, and cloud devices.
* `ansible.utils <https://github.com/ansible-collections/ansible.utils>`_ — provides utility plugins for manipulating and validating complex data structures within Ansible playbooks, including network address handling and data format conversion.
* `community.general <https://github.com/ansible-collections/community.general>`_ — provides a broad set of community-maintained modules and plugins for general infrastructure automation tasks not covered by more specialized collections.
* `community.library_inventory_filtering_v1 <https://github.com/ansible-collections/community.library_inventory_filtering>`_ — provides reusable filtering utilities that enable inventory plugins in other Ansible collections to filter hosts using common, standardized methods.

Operating systems
^^^^^^^^^^^^^^^^^

* `ansible.posix <https://github.com/ansible-collections/ansible.posix>`_ — provides modules and plugins for automating POSIX-compliant UNIX/Linux and derivative operating systems.
* `ansible.windows <https://github.com/ansible-collections/ansible.windows>`_ — provides core modules and plugins for managing and automating Windows hosts.
* `community.windows <https://github.com/ansible-collections/community.windows>`_ — provides plugins and modules for automation and management of Windows hosts.

Major cloud providers
^^^^^^^^^^^^^^^^^^^^^

* `amazon.aws <https://github.com/ansible-collections/amazon.aws>`_ — automates the management and deployment of AWS resources and services.
* `community.aws <https://github.com/ansible-collections/community.aws>`_ — provides community-maintained modules for managing AWS services, complementing the core amazon.aws collection.
* `azure.azcollection <https://github.com/ansible-collections/azure>`_ — automates the provisioning and management of Microsoft Azure cloud infrastructure and services.
* `google.cloud <https://github.com/ansible-collections/google.cloud>`_ — automates provisioning, configuration, and management of Google Cloud Platform resources.

Containerization
^^^^^^^^^^^^^^^^

* `community.docker <https://github.com/ansible-collections/community.docker>`_ — automates Docker container, image, network, volume, Docker Compose, and Docker Swarm management.
* `containers.podman <https://github.com/containers/ansible-podman-collections>`_ — automates the management of Podman containers, images, pods, networks, volumes, and secrets through idempotent modules and connection plugins.
* `kubernetes.core <https://github.com/ansible-collections/kubernetes.core>`_ — automates the management of applications and cluster provisioning in Kubernetes and OpenShift environments.

Cryptography
^^^^^^^^^^^^

* `community.crypto <https://github.com/ansible-collections/community.crypto>`_ — provides modules for cryptographic operations and certificate management, including OpenSSL certificates, keys, CSRs, and ACME protocol support.

DNS
^^^

* `community.dns <https://github.com/ansible-collections/community.dns>`_ — automates DNS record management across multiple providers and provides DNS lookup plugins and filters.

Virtualization
^^^^^^^^^^^^^^^

* `community.libvirt <https://github.com/ansible-collections/community.libvirt>`_ — automates the management of virtual machines and containers through the libvirt API.
* `community.vmware <https://github.com/ansible-collections/community.vmware>`_ — automates the management of VMware infrastructure, including vCenter and ESXi environments.
* `vmware.vmware <https://github.com/ansible-collections/vmware.vmware>`_ — automates the management of VMware vSphere resources and operator tasks like VM deployment, cluster configuration, and resource information gathering.
* `vmware.vmware_rest <https://github.com/ansible-collections/vmware.vmware_rest>`_ — automates VMware vSphere resource management and operator tasks using the vSphere REST API without requiring VMware SDKs.

Private cloud
^^^^^^^^^^^^^

* `openstack.cloud <https://opendev.org/openstack/ansible-collections-openstack>`_ — provides modules and plugins for automating the management of OpenStack cloud infrastructure and services.

Enterprise directory services
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* `microsoft.ad <https://github.com/ansible-collections/microsoft.ad>`_ — automates Active Directory management tasks through plugins and modules for Microsoft infrastructure administration.

.. _collections_to_remove:

Collections to remove (65)
--------------------------

Vendor-specific networking
^^^^^^^^^^^^^^^^^^^^^^^^^^

* `arista.eos <https://github.com/ansible-collections/arista.eos>`_ — automates the management and configuration of Arista EOS network devices including interfaces, routing protocols, and VLANs.
* `check_point.mgmt <https://github.com/CheckPointSW/CheckPointAnsibleMgmtCollection>`_ — automates the management and configuration of Check Point security appliances and firewalls via their web-services APIs.
* `cisco.aci <https://github.com/CiscoDevNet/ansible-aci>`_ — automates management and configuration of Cisco Application Centric Infrastructure (ACI) environments.
* `cisco.intersight <https://github.com/CiscoDevNet/intersight-ansible>`_ — automates management and configuration of Cisco Intersight infrastructure including server policies, profiles, and firmware updates.
* `cisco.ios <https://github.com/ansible-collections/cisco.ios>`_ — automates the management of Cisco IOS and IOS XE network devices including interfaces, routing, and security configuration.
* `cisco.iosxr <https://github.com/ansible-collections/cisco.iosxr>`_ — automates the management and configuration of Cisco IOS-XR network devices, including interfaces, routing protocols, security policies, and system settings.
* `cisco.meraki <https://github.com/meraki/dashboard-api-ansible>`_ — automates management of Cisco Meraki cloud-managed networking infrastructure, including devices, networks, VPNs, and wireless settings.
* `cisco.mso <https://github.com/CiscoDevNet/ansible-mso>`_ — automates management and configuration of Cisco ACI Multi-Site and Nexus Dashboard Orchestrator environments.
* `cisco.nxos <https://github.com/ansible-collections/cisco.nxos>`_ — automates the management and configuration of Cisco NX-OS network devices through resource modules and connection plugins.
* `community.ciscosmb <https://github.com/ansible-collections/community.ciscosmb>`_ — automates management and configuration of Cisco Small Business switches such as the SG250, SG300, SG500, and CBS350 series.
* `community.routeros <https://github.com/ansible-collections/community.routeros>`_ — automates management of MikroTik RouterOS network devices through SSH or HTTP/HTTPS API.
* `dellemc.enterprise_sonic <https://github.com/ansible-collections/dellemc.enterprise_sonic>`_ — automates configuration and management of Dell EMC PowerSwitch platforms running Enterprise SONiC Distribution.
* `f5networks.f5_modules <https://github.com/F5Networks/f5-ansible-f5modules>`_ — automates configuration, deployment, and management tasks for F5 BIG-IP and BIG-IQ devices.
* `vyos.vyos <https://github.com/ansible-collections/vyos.vyos>`_ — automates the management and configuration of VyOS network appliances, including routing, firewall, interfaces, and other network services.

Vendor-specific security appliances
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* `fortinet.fortimanager <https://github.com/fortinet-ansible-dev/ansible-galaxy-fortimanager-collection>`_ — automates the configuration of Fortinet FortiManager appliances for managing firewall policies, security profiles, and device administration at scale.
* `fortinet.fortios <https://github.com/fortinet-ansible-dev/ansible-galaxy-fortios-collection>`_ — automates the configuration and management of Fortinet FortiOS and FortiGate firewalls, covering firewall policies, network interfaces, security profiles, and system settings.

Vendor-specific storage
^^^^^^^^^^^^^^^^^^^^^^^

* `dellemc.powerflex <https://github.com/dell/ansible-powerflex>`_ — automates the provisioning and management of Dell PowerFlex storage systems, including volumes, snapshots, storage pools, and SDCs.
* `everpure.flasharray <https://github.com/Everpure-Ansible/FlashArray-Collection>`_ — automates provisioning and management tasks on Everpure FlashArray storage systems, including volumes, hosts, replication, and configuration settings.
* `everpure.flashblade <https://github.com/Everpure-Ansible/FlashBlade-Collection>`_ — automates management and configuration of Everpure FlashBlade storage systems, including filesystem creation, replication, and disaster recovery.
* `hitachivantara.vspone_block <https://github.com/hitachi-vantara/vspone-block-ansible>`_ — automates storage provisioning, configuration, and management for Hitachi VSP block storage systems.
* `hitachivantara.vspone_object <https://github.com/hitachi-vantara/vspone-object-ansible>`_ — automates storage provisioning, configuration, and management for Hitachi VSP One Object storage systems.
* `ibm.storage_virtualize <https://github.com/ansible-collections/ibm.storage_virtualize>`_ — automates provisioning, configuration, and management of IBM Storage Virtualize systems, including IBM FlashSystem.
* `infinidat.infinibox <https://github.com/infinidat/ansible-infinidat-collection>`_ — automates management of Infinidat InfiniBox storage arrays, including volumes, hosts, pools, and filesystems.
* `netapp.ontap <https://github.com/ansible-collections/netapp.ontap>`_ — automates the configuration and management of NetApp ONTAP storage systems through modules supporting both legacy ZAPI and modern REST APIs.
* `netapp.storagegrid <https://github.com/ansible-collections/netapp.storagegrid>`_ — automates the configuration and management of NetApp StorageGrid systems, including storage accounts, buckets, users, groups, and grid settings.
* `netapp_eseries.santricity <https://github.com/netapp-eseries/santricity>`_ — automates configuration and management of NetApp E-Series SANtricity storage arrays.

Vendor-specific server and hardware management
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* `dellemc.openmanage <https://github.com/dell/dellemc-openmanage-ansible-modules>`_ — automates the configuration, deployment, and management of Dell PowerEdge servers and modular infrastructure through iDRAC, OME, and related management platforms.
* `ieisystem.inmanage <https://github.com/ieisystem/ieisystem.inmanage>`_ — automates management of IEIT servers through RESTful interfaces, including BMC configuration, firmware upgrades, and BIOS settings.
* `inspur.ispim <https://github.com/ispim/inspur.ispim>`_ — provides management and automation capabilities for Inspur servers through a RESTful interface.
* `kaytus.ksmanage <https://github.com/KSManageOSS/kaytus.ksmanage>`_ — automates management of Kaytus servers through RESTful interfaces, including BMC configuration, firmware upgrades, and BIOS settings.
* `wti.remote <https://github.com/wtinetworkgear/wti-collection>`_ — provides configuration management modules for WTI out-of-band and power distribution unit devices.

Vendor-specific secrets management
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* `cyberark.conjur <https://github.com/cyberark/ansible-conjur-collection>`_ — enables secure retrieval of secrets from CyberArk Conjur or Secrets Manager using lookup plugins and host identity roles.

Niche or regional cloud providers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* `cloudscale_ch.cloud <https://github.com/cloudscale-ch/ansible-collection-cloudscale>`_ — automates provisioning and management of resources on the cloudscale.ch Swiss cloud platform.
* `community.hrobot <https://github.com/ansible-collections/community.hrobot>`_ — automates management of Hetzner Robot infrastructure, including servers, firewalls, failover IPs, storage boxes, and SSH keys.
* `hetzner.hcloud <https://github.com/ansible-collections/hetzner.hcloud>`_ — automates the management and provisioning of cloud infrastructure resources on the Hetzner Cloud platform.
* `ngine_io.cloudstack <https://github.com/ngine-io/ansible-collection-cloudstack>`_ — automates the management and orchestration of Apache CloudStack cloud infrastructure.
* `vultr.cloud <https://github.com/vultr/ansible-collection-vultr>`_ — provides modules and plugins for automating the deployment and management of infrastructure on the Vultr cloud platform.

Vendor-specific virtualization and compute
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* `community.okd <https://github.com/openshift/community.okd>`_ — automates the management of applications in OKD/OpenShift clusters and handles cluster provisioning and maintenance tasks.
* `community.proxmox <https://github.com/ansible-collections/community.proxmox>`_ — automates provisioning and management of Proxmox virtualization infrastructure.
* `kubevirt.core <https://github.com/kubevirt/kubevirt.core>`_ — automates the management of KubeVirt virtual machines and provides an inventory source for integrating them with Ansible.
* `ovirt.ovirt <https://github.com/ovirt/ovirt-ansible-collection>`_ — provides modules and roles for automating oVirt/RHV virtualization infrastructure management.

Databases
^^^^^^^^^

* `ansible.mariadb <https://github.com/ansible-collections/ansible.mariadb>`_ — automates MariaDB database administration tasks such as user management, database creation, replication, and variable configuration.
* `ansible.mysql <https://github.com/ansible-collections/ansible.mysql>`_ — automates MySQL database administration tasks including user management, replication, database operations, and configuration management.
* `community.clickhouse <https://github.com/ansible-collections/community.clickhouse>`_ — automates ClickHouse database management tasks including database creation, server information retrieval, and query execution.
* `community.mongodb <https://github.com/ansible-collections/community.mongodb>`_ — automates the deployment, configuration, and management of MongoDB instances across standalone, replicaset, and sharded cluster architectures.
* `community.postgresql <https://github.com/ansible-collections/community.postgresql>`_ — automates PostgreSQL database management tasks, including database creation, user management, schema administration, and privilege control.
* `lowlydba.sqlserver <https://github.com/LowlyDBA/lowlydba.sqlserver>`_ — automates SQL Server configuration and maintenance across platforms using PowerShell modules like dbatools and dbops.
* `ravendb.ravendb <https://github.com/ravendb/ansible-collection-ravendb>`_ — automates the installation, configuration, and management of RavenDB database clusters, including server deployment, database creation, and index operations.

Middleware and proxies
^^^^^^^^^^^^^^^^^^^^^^

* `community.proxysql <https://github.com/ansible-collections/community.proxysql>`_ — automates the configuration and management of ProxySQL, a MySQL proxy server for load balancing and query routing.
* `community.rabbitmq <https://github.com/ansible-collections/community.rabbitmq>`_ — automates the management and configuration of RabbitMQ message broker infrastructure.

Monitoring and SIEM
^^^^^^^^^^^^^^^^^^^

* `community.zabbix <https://github.com/ansible-collections/community.zabbix>`_ — automates the deployment and management of Zabbix monitoring infrastructure, including agents, servers, proxies, and web interfaces.
* `splunk.es <https://github.com/ansible-collections/splunk.es>`_ — automates security operations management in Splunk Enterprise Security SIEM, including correlation searches, findings, investigations, and data inputs.
* `telekom_mms.icinga_director <https://github.com/telekom-mms/ansible-collection-icinga-director>`_ — automates the management of Icinga 2 monitoring objects through the Icinga Director API to create, modify, and deploy hosts, services, and commands.

DevOps tools
^^^^^^^^^^^^

* `community.grafana <https://github.com/ansible-collections/grafana>`_ — automates management of Grafana resources including dashboards, datasources, users, teams, and administrative configurations.
* `community.hashi_vault <https://github.com/ansible-collections/community.hashi_vault>`_ — automates managing and retrieving secrets from HashiCorp Vault for use in infrastructure provisioning and configuration management.
* `grafana.grafana <https://github.com/grafana/grafana-ansible-collection>`_ — automates the deployment and configuration of Grafana, Grafana Agent, Alloy, Loki, Mimir, and Promtail observability infrastructure.

Other domain-specific tools and platforms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* `chocolatey.chocolatey <https://github.com/chocolatey/chocolatey-ansible>`_ — automates Windows package management through Chocolatey, handling package installation, updates, and repository configuration.
* `community.sap_libs <https://github.com/sap-linuxlab/community.sap_libs>`_ — automates various low-level activities on SAP systems, enabling infrastructure management for SAP environments.
* `community.sops <https://github.com/ansible-collections/community.sops>`_ — automates encryption and decryption of secret files using Mozilla SOPS with keys like GPG, KMS, or age.
* `graphiant.naas <https://github.com/Graphiant-Inc/graphiant-playbooks>`_ — automates network infrastructure and configuration management for Graphiant's Network-as-a-Service platform.
* `infoblox.nios_modules <https://github.com/infobloxopen/infoblox-ansible>`_ — automates DNS and IPAM management by managing networks, IP addresses, and DNS records in Infoblox NIOS systems.
* `microsoft.iis <https://github.com/ansible-collections/microsoft.iis>`_ — provides plugins and modules to manage Windows hosts running Internet Information Services (IIS).
* `netbox.netbox <https://github.com/netbox-community/ansible_modules>`_ — automates network infrastructure management by providing modules to define network state in NetBox, generate dynamic inventory, and query NetBox data.
* `pcg.alpaca_operator <https://github.com/Public-Cloud-Group/alpaca-operator-ansible>`_ — automates the management of ALPACA Operator infrastructure, including groups, agents, systems, and commands through REST API integration.
* `theforeman.foreman <https://github.com/theforeman/foreman-ansible-modules>`_ — provides modules for automating Foreman server and Katello plugin configuration and management through API interactions.

.. seealso::

  :ref:`steering_inclusion`
     Collection inclusion criteria and process

  :ref:`removal_from_ansible`
     Collection removal from the Ansible package
