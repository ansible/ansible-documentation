.. _core_roadmap_2.17:

*****************
Ansible-core 2.17
*****************

.. contents::
   :local:

Release Schedule
================

Expected
--------

PRs must be raised well in advance of the dates below to have a chance of being included in this ansible-core release.

.. note:: Dates subject to change.

Development Phase
^^^^^^^^^^^^^^^^^

The ``milestone`` branch will be advanced at the start date of each development phase.

- 2023-10-16 Development Phase 1
- 2023-12-18 Development Phase 2
- 2024-02-19 Development Phase 3

Release Phase
^^^^^^^^^^^^^

- 2024-04-01 Feature Freeze (and ``stable-2.17`` branching from ``devel``)
  No new functionality (including modules/plugins) to any code

- 2024-04-08 Beta 1

- 2024-04-29 Release Candidate 1

- 2024-05-20 Release

.. note:: The beta and release candidate schedules allow for up to 3 releases on a weekly schedule depending on the necessity of creating a release.

Release Manager
===============

 Ansible Core Team

Planned work
============

* Drop Python 2.7 and 3.6 support for module execution
* Remove deprecated functionality
* Decrease incidental integration tests
* Add controller type hinting for discrete areas of the code
* Decrease testing sanity ignores
* Update ansible-test container images and VMs
* Update ansible-test dependencies

Delayed work
============

The following work has been delayed and retargeted for a future release:

* Data Tagging
