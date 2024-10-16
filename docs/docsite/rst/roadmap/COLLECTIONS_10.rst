..
   THIS DOCUMENT IS OWNED BY THE ANSIBLE COMMUNITY STEERING COMMITTEE. ALL CHANGES MUST BE APPROVED BY THE STEERING COMMITTEE!
   For small changes (fixing typos, language errors, etc.) create a PR and ping @ansible/steering-committee.
   For other changes, create a discussion as described in https://github.com/ansible-community/community-topics/blob/main/community_topics_workflow.md#creating-a-topic
   to discuss the changes.
   (Creating a draft PR for this file and mentioning it in the community topic is also OK.)

.. _ansible_10_roadmap:

====================
Ansible project 10.0
====================

This release schedule includes dates for the `ansible <https://pypi.org/project/ansible/>`_ package, with a few dates for the `ansible-core <https://pypi.org/project/ansible-core/>`_ package as well. All dates are subject to change. See the `ansible-core 2.17 Roadmap <https://docs.ansible.com/ansible-core/devel/roadmap/ROADMAP_2_17.html>`_ for the most recent updates on ``ansible-core``.

.. contents::
   :local:


Release schedule
=================


:2024-04-01: ansible-core feature freeze, stable-2.17 branch created.
:2024-04-08: Start of ansible-core 2.17 betas
:2024-04-09: Ansible-10.0.0 alpha1 [1]_
:2024-04-29: First ansible-core 2.17 release candidate.
:2024-04-30: Ansible-10.0.0 alpha2 [1]_
:2024-05-20: Ansible-core-2.17.0 released.
:2024-05-20: Last day for collections to make backwards incompatible releases that will be accepted into Ansible-10. This includes adding new collections to Ansible 10.0.0; from now on new collections have to wait for 10.1.0 or later.
:2024-05-21: Ansible-10.0.0 beta1 -- feature freeze [2]_ (weekly beta releases; collection owners and interested users should test for bugs).
:2024-05-28: Ansible-10.0.0 rc1 [3]_ [4]_ (weekly release candidates as needed; test and alert us to any blocker bugs). Blocker bugs will slip release.
:2024-05-31: Last day to trigger an Ansible-10.0.0rc2 release because of major defects in Ansible-10.0.0rc1.
:2024-06-04: Ansible-10.0.0rc2 when necessary, otherwise Ansible-10.0.0 release.
:2024-06-11: Ansible-10.0.0 release when Ansible-10.0.0rc2 was necessary.
:2024-06-04 or 2023-06-11: Create the ansible-build-data directory and files for Ansible-11.
:2024-06-17: Release of ansible-core 2.17.1.
:2024-06-18: Release of Ansible-10.1.0 (bugfix + compatible features: every four weeks.)

.. [1] In case there are any additional ansible-core beta releases or release candidates, we will try to do another Ansible-10.0.0 alpha release. This might mean that we will release Ansible-10.0.0 alpha2 earlier (and release Ansible-10.0.0 alpha3 or later on 2024-04-30) and / or release one or more additional alpha after 2024-04-30.

.. [2] No new modules or major features accepted after this date. In practice, this means we will freeze the semver collection versions to compatible release versions. For example, if the version of community.crypto on this date was community.crypto 2.3.0; Ansible-10.0.0 could ship with community.crypto 2.3.1. It would not ship with community.crypto 2.4.0.

.. [3] After this date only changes blocking a release are accepted. Accepted changes require creating a new release candidate and may slip the final release date.

.. [4] Collections will be updated to a new version only if a blocker is approved. Collection owners should discuss any blockers at a community meeting (before this freeze) to decide whether to bump the version of the collection for a fix. See the `creating an Ansible Community Topic workflow <https://github.com/ansible-community/community-topics/blob/main/community_topics_workflow.md#creating-a-topic>`_.

.. note::

  Breaking changes will be introduced in Ansible 10.0.0. We encourage the use of deprecation periods that give advance notice of breaking changes at least one Ansible release before they are introduced. However, deprecation notices are not guaranteed to take place.

.. note::

  In general, it is in the discretion of the release manager to delay a release by 1-2 days for reasons such as personal (schedule) problems, technical problems (CI/infrastructure breakdown), and so on.
  However, in case two releases are planned for the same day, a release of the latest stable version takes precedence. This means that if a stable Ansible 10 release collides with a pre-release of Ansible 11, the latter will be delayed.
  If a Ansible 10 release collides with a stable Ansible 11 release, including 11.0.0, the Ansible 10 release will be delayed.


Planned major changes
=====================

- The netapp.aws collection will be removed as it is unmaintained (https://github.com/ansible-community/ansible-build-data/issues/223).
- The gluster.gluster collection will be removed as it is unmaintained (https://github.com/ansible-community/ansible-build-data/issues/249).
- The community.sap collection will be removed as it is deprecated (https://github.com/ansible-community/ansible-build-data/issues/262).
- The netapp.azure collection will be removed as it is unmaintained (https://github.com/ansible-community/ansible-build-data/issues/272).
- The netapp.elementsw collection will be removed as it is unmaintained (https://github.com/ansible-community/ansible-build-data/issues/276).
- The netapp.um_info collection will be removed as it is unmaintained (https://github.com/ansible-community/ansible-build-data/issues/280).
- The community.azure collection will be removed as it is deprecated (https://github.com/ansible-community/ansible-build-data/issues/283).
- The hpe.nimble collection will be removed as it is unmaintained (https://github.com/ansible-community/ansible-build-data/issues/285).

You can install removed collections manually with ``ansible-galaxy collection install <collection_name>``.


Ansible minor releases
=======================

Ansible 10.x follows ansible-core-2.17.x releases, so releases will occur approximately every four weeks. If ansible-core delays a release for whatever reason, the next Ansible 10.x minor release will be delayed accordingly.

Ansible 10.x minor releases may contain new features (including new collections) but not backwards incompatibilities. In practice, this means we will include new collection versions where either the patch or the minor version number has changed but not when the major number has changed. For example, if Ansible-10.0.0 ships with community.crypto 2.3.0, Ansible-10.1.0 could ship with community.crypto 2.4.0 but not community.crypto 3.0.0.


.. note::

    Minor and patch releases will stop when Ansible-11 is released. See the :ref:`Release and Maintenance Page <release_and_maintenance>` for more information.

.. note::

    We will not provide bugfixes or security fixes for collections that do not
    provide updates for their major release cycle included in Ansible 10.


For more information, reach out on a mailing list or a chat channel - see :ref:`communication` for more details.
