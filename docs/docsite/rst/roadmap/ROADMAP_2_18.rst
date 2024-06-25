.. _core_roadmap_2.18:

*****************
Ansible-core 2.18
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

The ``milestone`` branch will be advanced at the start date of each development phase, and the beta 1 release.

- 2024-04-29 Development Phase 1
- 2024-06-24 Development Phase 2
- 2024-08-05 Development Phase 3
- 2024-09-23 Beta 1

Release Phase
^^^^^^^^^^^^^

- 2024-09-16 Feature Freeze (and ``stable-2.18`` branching from ``devel``)
  No new functionality (including modules/plugins) to any code

- 2024-09-23 Beta 1

- 2024-10-14 Release Candidate 1

- 2024-11-04 Release

.. note:: The beta and release candidate schedules allow for up to 3 releases on a weekly schedule depending on the necessity of creating a release.

Release Manager
===============

 Ansible Core Team

Planned work
============

* Drop Python 3.10, and add Python 3.13 for controller code
* Drop Python 3.7, and add Python 3.13 for target code
* Data Tagging
* Add support to ansible-galaxy for new console.redhat.com service account auth
* Finalize task object connection attribute for connection reporting in callbacks
* Add break functionality for task loops
* Add new non-local mount facts
* Evaluate changes to strategy plugins to use the core strategy result processing for meta task results
* Remove deprecated functionality
* Decrease incidental integration tests
* Add controller type hinting for discrete areas of the code
* Decrease testing sanity ignores
* Update ansible-test container images and VMs
* Update ansible-test dependencies


Delayed work
============

The following work has been delayed and retargeted for a future release:

* TBD
