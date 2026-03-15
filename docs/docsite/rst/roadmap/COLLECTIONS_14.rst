..
   THIS DOCUMENT IS OWNED BY THE ANSIBLE COMMUNITY STEERING COMMITTEE. ALL CHANGES MUST BE APPROVED BY THE STEERING COMMITTEE!
   For small changes (fixing typos, language errors, etc.) create a PR and ping @ansible/steering-committee.
   For other changes, create a discussion as described in https://docs.ansible.com/projects/ansible/devel/community/steering/community_topics_workflow.html#creating-a-topic
   to discuss the changes.
   (Creating a draft PR for this file and mentioning it in the community topic is also OK.)

.. _ansible_14_roadmap:

====================
Ansible project 14.0
====================

This release schedule includes dates for the `ansible <https://pypi.org/project/ansible/>`_ package, with a few dates for the `ansible-core <https://pypi.org/project/ansible-core/>`_ package as well. All dates are subject to change. See the :ref:`ansible-core 2.21 Roadmap <core_roadmap_2.21>` for the most recent updates on ``ansible-core``.

.. contents::
   :local:


Release schedule
=================

The schedule has been updated to match the :ref:`ansible-core 2.21 release schedule <core_roadmap_2.21>`. If that one gets modified again, the Ansible 14 pre-release and release dates will be shifted accordingly, and potentially more pre-releases will be inserted.

:2026-03-30: ansible-core feature freeze.
:2026-04-06: Start of ansible-core 2.21 betas.
:2026-04-07: Ansible-14.0.0 alpha1; there will be more alpha releases usually following additional ansible-core 2.21 betas.
:2026-04-27: First ansible-core 2.21 release candidate.
:2026-04-28: Ansible-14.0.0 alphaX; there might be more alpha releases following additional ansible-core 2.21 release candidates.
:2026-05-18: Ansible-core-2.21.0 released.
:2026-05-18: Last day for collections to make backwards incompatible releases that will be accepted into Ansible-14. This includes adding new collections to Ansible 14.0.0; from now on new collections have to wait for 14.1.0 or later.
:2026-05-19: Ansible-14.0.0 beta1 -- feature freeze [2]_ (collection owners and interested users should test for bugs).
:2026-05-26: Ansible-14.0.0 rc1 [3]_ [4]_ (weekly release candidates as needed; test and alert us to any blocker bugs). Blocker bugs will slip release.
:2026-05-29: Last day to trigger an Ansible-14.0.0rc2 release because of major defects in Ansible-14.0.0rc1.
:2026-06-02: Ansible-14.0.0rc2 when necessary, otherwise Ansible-14.0.0 release.
:2026-06-09: Ansible-14.0.0 release when Ansible-14.0.0rc2 was necessary.
:2026-06-02 or 2026-06-09: Create the ansible-build-data directory and files for Ansible-15.
:2026-06-15: Release of ansible-core 2.21.1.
:2026-06-16: Release of Ansible-14.1.0 (bugfix + compatible features: every four weeks.)

.. [2] No new modules or major features accepted after this date. In practice, this means we will freeze the semver collection versions to compatible release versions. For example, if the version of community.crypto on this date was community.crypto 3.3.0; Ansible-14.0.0 could ship with community.crypto 3.3.1. It would not ship with community.crypto 3.4.0.

.. [3] After this date only changes blocking a release are accepted. Accepted changes require creating a new release candidate and may slip the final release date.

.. [4] Collections will be updated to a new version only if a blocker is approved. Collection owners should discuss any blockers at a community meeting (before this freeze) to decide whether to bump the version of the collection for a fix. See the :ref:`creating an Ansible Community Topic workflow <creating_community_topic>`.

.. note::

  Breaking changes will be introduced in Ansible 14.0.0. We encourage the use of deprecation periods that give advance notice of breaking changes at least one Ansible release before they are introduced. However, deprecation notices are not guaranteed to take place.

.. note::

  In general, it is in the discretion of the release manager to delay a release by 1-2 days for reasons such as personal (schedule) problems, technical problems (CI/infrastructure breakdown), and so on.
  However, in case two releases are planned for the same day, a release of the latest stable version takes precedence. This means that if a stable Ansible 14 release collides with a pre-release of Ansible 15, the latter will be delayed.
  If an Ansible 14 release collides with a stable Ansible 15 release, including 15.0.0, the Ansible 14 release will be delayed.


Ansible minor releases
=======================

Ansible 14.x follows ansible-core-2.21.x releases, so releases will occur approximately every four weeks. If ansible-core delays a release for whatever reason, the next Ansible 14.x minor release will usually (but not always) be delayed accordingly.

Ansible 14.x minor releases may contain new features (including new collections) but not backwards incompatibilities. In practice, this means we will include new collection versions where either the patch or the minor version number has changed but not when the major number has changed. For example, if Ansible-14.0.0 ships with community.crypto 3.3.0, Ansible-14.1.0 could ship with community.crypto 3.4.0 but not community.crypto 4.0.0.


.. note::

    Minor and patch releases will stop when Ansible-15 is released. See the :ref:`Release and Maintenance Page <release_and_maintenance>` for more information.

.. note::

    We will not provide bugfixes or security fixes for collections that do not
    provide updates for their major release cycle included in Ansible 14.


Communication
=============

You can submit feedback on the current roadmap by creating a :ref:`community topic<creating_community_topic>`.

Visit the :ref:`Ansible communication guide<communication>` for details on how to join and use Ansible communication platforms.
