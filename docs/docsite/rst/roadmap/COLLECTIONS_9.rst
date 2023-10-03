..
   THIS DOCUMENT IS OWNED BY THE ANSIBLE COMMUNITY STEERING COMMITTEE. ALL CHANGES MUST BE APPROVED BY THE STEERING COMMITTEE!
   For small changes (fixing typos, language errors, etc.) create a PR and ping @ansible/steering-committee.
   For other changes, create a discussion in https://github.com/ansible-community/community-topics/ to discuss the changes.
   (Creating a draft PR for this file and mentioning it in the community topic is also OK.)

.. _ansible_9_roadmap:

===================
Ansible project 9.0
===================

This release schedule includes dates for the `ansible <https://pypi.org/project/ansible/>`_ package, with a few dates for the `ansible-core <https://pypi.org/project/ansible-core/>`_ package as well. All dates are subject to change. See the `ansible-core 2.16 Roadmap <https://docs.ansible.com/ansible-core/devel/roadmap/ROADMAP_2_16.html>`_ for the most recent updates on ``ansible-core``.

.. contents::
   :local:


Release schedule
=================


:2023-09-18: ansible-core feature freeze, stable-2.16 branch created.
:2023-09-25: Start of ansible-core 2.16 betas
:2023-09-26: Ansible-9.0.0 alpha1
:2023-10-16: First ansible-core 2.16 release candidate.
:2023-10-17: Ansible-9.0.0 alpha2
:2023-11-06: Ansible-core-2.16.0 released.
:2023-11-06: Last day for collections to make backwards incompatible releases that will be accepted into Ansible-9. This includes adding new collections to Ansible 9.0.0; from now on new collections have to wait for 9.1.0 or later.
:2023-11-07: Ansible-9.0.0 beta1 -- feature freeze [1]_ (weekly beta releases; collection owners and interested users should test for bugs).
:2023-11-14: Ansible-9.0.0 rc1 [2]_ [3]_ (weekly release candidates as needed; test and alert us to any blocker bugs).  Blocker bugs will slip release.
:2023-11-17: Last day to trigger an Ansible-9.0.0rc2 release because of major defects in Ansible-9.0.0rc1.
:2023-11-21: Ansible-9.0.0rc2 when necessary, otherwise Ansible-9.0.0 release.
:2023-11-28: Ansible-9.0.0 release when Ansible-9.0.0rc2 was necessary.
:2023-11-21 or 2023-11-28: Create the ansible-build-data directory and files for Ansible-10.
:2023-12-04: Release of ansible-core 2.16.1.
:2023-12-05: Release of Ansible-9.1.0 (bugfix + compatible features: every four weeks.)

.. [1] No new modules or major features accepted after this date. In practice, this means we will freeze the semver collection versions to compatible release versions. For example, if the version of community.crypto on this date was community.crypto 2.3.0; Ansible-9.0.0 could ship with community.crypto 2.3.1. It would not ship with community.crypto 2.4.0.

.. [2] After this date only changes blocking a release are accepted. Accepted changes require creating a new release candidate and may slip the final release date.

.. [3] Collections will be updated to a new version only if a blocker is approved. Collection owners should discuss any blockers at a community IRC meeting (before this freeze) to decide whether to bump the version of the collection for a fix. See the `Community IRC meeting agenda <https://github.com/ansible/community/issues/539>`_.

.. note::

  Breaking changes will be introduced in Ansible 9.0.0. We encourage the use of deprecation periods that give advance notice of breaking changes at least one Ansible release before they are introduced. However, deprecation notices are not guaranteed to take place.

.. note::

  In general, it is in the discretion of the release manager to delay a release by 1-2 days for reasons such as personal (schedule) problems, technical problems (CI/infrastructure breakdown), and so on.
  However, in case two releases are planned for the same day, a release of the latest stable version takes precedence. This means that if a stable Ansible 9 release collides with a pre-release of Ansible 10, the latter will be delayed.
  If a Ansible 9 release collides with a stable Ansible 10 release, including 10.0.0, the Ansible 9 release will be delayed.


Planned major changes
=====================

- The cisco.nso collection will be removed as it is unmaintained (https://github.com/ansible-community/ansible-build-data/issues/190).
- The community.fortios collection will be removed as it is unmaintained (https://github.com/ansible-community/ansible-build-data/issues/196).
- The community.google collection will be removed as it is unmaintained (https://github.com/ansible-community/ansible-build-data/issues/198).
- The community.skydive collection will be removed as it is unmaintained (https://github.com/ansible-community/ansible-build-data/issues/199).

You can install removed collections manually with ``ansible-galaxy collection install <collection_name>``.


Ansible minor releases
=======================

Ansible 9.x minor releases will occur approximately every four weeks if changes to collections have been made or to align to a later ansible-core-2.16.x.  Ansible 9.x minor releases may contain new features (including new collections) but not backwards incompatibilities. In practice, this means we will include new collection versions where either the patch or the minor version number has changed but not when the major number has changed. For example, if Ansible-9.0.0 ships with community.crypto 2.3.0; Ansible-9.1.0 could ship with community.crypto 2.4.0 but not community.crypto 3.0.0.


.. note::

    Minor and patch releases will stop when Ansible-10 is released. See the :ref:`Release and Maintenance Page <release_and_maintenance>` for more information.


For more information, reach out on a mailing list or a chat channel - see :ref:`communication` for more details.
