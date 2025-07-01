..
   THIS DOCUMENT IS OWNED BY THE ANSIBLE COMMUNITY STEERING COMMITTEE. ALL CHANGES MUST BE APPROVED BY THE STEERING COMMITTEE!
   For small changes (fixing typos, language errors, etc.) create a PR and ping @ansible/steering-committee.
   For other changes, create a discussion as described in https://github.com/ansible-community/community-topics/blob/main/community_topics_workflow.md#creating-a-topic
   to discuss the changes.
   (Creating a draft PR for this file and mentioning it in the community topic is also OK.)

.. _ansible_11_roadmap:

====================
Ansible project 11.0
====================

This release schedule includes dates for the `ansible <https://pypi.org/project/ansible/>`_ package, with a few dates for the `ansible-core <https://pypi.org/project/ansible-core/>`_ package as well. All dates are subject to change. See the `ansible-core 2.18 Roadmap <https://docs.ansible.com/ansible-core/devel/roadmap/ROADMAP_2_18.html>`_ for the most recent updates on ``ansible-core``.

.. contents::
   :local:


Release schedule
=================


:2024-09-16: ansible-core feature freeze, stable-2.18 branch created.
:2024-09-23: Start of ansible-core 2.18 betas
:2024-09-24: Ansible-11.0.0 alpha1 [1]_
:2024-10-14: First ansible-core 2.18 release candidate.
:2024-10-15: Ansible-11.0.0 alpha2 [1]_
:2024-11-04: Ansible-core-2.18.0 released.
:2024-11-04: Last day for collections to make backwards incompatible releases that will be accepted into Ansible-11. This includes adding new collections to Ansible 11.0.0; from now on new collections have to wait for 11.1.0 or later.
:2024-11-05: Ansible-11.0.0 beta1 -- feature freeze [2]_ (weekly beta releases; collection owners and interested users should test for bugs).
:2024-11-12: Ansible-11.0.0 rc1 [3]_ [4]_ (weekly release candidates as needed; test and alert us to any blocker bugs). Blocker bugs will slip release.
:2024-11-15: Last day to trigger an Ansible-11.0.0rc2 release because of major defects in Ansible-11.0.0rc1.
:2024-11-19: Ansible-11.0.0rc2 when necessary, otherwise Ansible-11.0.0 release.
:2024-11-26: Ansible-11.0.0 release when Ansible-11.0.0rc2 was necessary.
:2024-11-19 or 2023-11-26: Create the ansible-build-data directory and files for Ansible-12.
:2024-12-02: Release of ansible-core 2.18.1.
:2024-12-03: Release of Ansible-11.1.0 (bugfix + compatible features: every four weeks.)

.. [1] In case there are any additional ansible-core beta releases or release candidates, we will try to do another Ansible-11.0.0 alpha release. This might mean that we will release Ansible-11.0.0 alpha2 earlier (and release Ansible-11.0.0 alpha3 or later on 2024-10-15) and / or release one or more additional alpha after 2024-10-15.

.. [2] No new modules or major features accepted after this date. In practice, this means we will freeze the semver collection versions to compatible release versions. For example, if the version of community.crypto on this date was community.crypto 2.3.0; Ansible-11.0.0 could ship with community.crypto 2.3.1. It would not ship with community.crypto 2.4.0.

.. [3] After this date only changes blocking a release are accepted. Accepted changes require creating a new release candidate and may slip the final release date.

.. [4] Collections will be updated to a new version only if a blocker is approved. Collection owners should discuss any blockers at a community meeting (before this freeze) to decide whether to bump the version of the collection for a fix. See the `creating an Ansible Community Topic workflow <https://github.com/ansible-community/community-topics/blob/main/community_topics_workflow.md#creating-a-topic>`_.

.. note::

  Breaking changes will be introduced in Ansible 11.0.0. We encourage the use of deprecation periods that give advance notice of breaking changes at least one Ansible release before they are introduced. However, deprecation notices are not guaranteed to take place.

.. note::

  In general, it is in the discretion of the release manager to delay a release by 1-2 days for reasons such as personal (schedule) problems, technical problems (CI/infrastructure breakdown), and so on.
  However, in case two releases are planned for the same day, a release of the latest stable version takes precedence. This means that if a stable Ansible 11 release collides with a pre-release of Ansible 12, the latter will be delayed.
  If a Ansible 11 release collides with a stable Ansible 12 release, including 12.0.0, the Ansible 11 release will be delayed.


Planned major changes
=====================

- The inspur.sm collection will be removed as it is unmaintained (https://github.com/ansible-community/ansible-build-data/issues/424).
- The netapp.storagegrid collection will be removed as it is unmaintained (https://github.com/ansible-community/ansible-build-data/issues/434).
- The frr.frr collection will be removed as it is unmaintained (https://github.com/ansible-community/ansible-build-data/issues/437).
- The openvswitch.openvswitch collection will be removed as it is unmaintained (https://github.com/ansible-community/ansible-build-data/issues/437).

You can install removed collections manually with ``ansible-galaxy collection install <collection_name>``.


Ansible minor releases
=======================

Ansible 11.x follows ansible-core-2.18.x releases, so releases will occur approximately every four weeks. If ansible-core delays a release for whatever reason, the next Ansible 11.x minor release will be delayed accordingly.

Ansible 11.x minor releases may contain new features (including new collections) but not backwards incompatibilities. In practice, this means we will include new collection versions where either the patch or the minor version number has changed but not when the major number has changed. For example, if Ansible-11.0.0 ships with community.crypto 2.3.0, Ansible-11.1.0 could ship with community.crypto 2.4.0 but not community.crypto 3.0.0.


.. note::

    Minor and patch releases will stop when Ansible-13 is released.
    This will likely be in November 2025, at the end of the Ansible Core 2.18 critical bugfix support lifecycle.
    This is approximately six months longer than regular Ansible releases.
    See the :ref:`Release and Maintenance Page <release_and_maintenance>` for more information.

.. note::

    We will not provide bugfixes or security fixes for collections that do not
    provide updates for their major release cycle included in Ansible 11.

Communication
=============

You can submit feedback on the current roadmap by creating a :ref:`community topic<creating_community_topic>`.

Visit the :ref:`Ansible communication guide<communication>` for details on how to join and use Ansible communication platforms.
