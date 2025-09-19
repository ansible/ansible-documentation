.. _core_roadmap_2.20:

*****************
Ansible-core 2.20
*****************

.. contents::
   :local:

Release Schedule
================

Expected
--------

PRs must be raised sufficiently in advance of the following dates to have a chance of inclusion in this ansible-core release.

.. note:: Dates are subject to change.

Development Phase
^^^^^^^^^^^^^^^^^

The ``milestone`` branch will be advanced at the start date of each development phase and the beta 1 release.

- 2025-08-18 Development Phase 5
- 2025-09-22 Beta 1

Release Phase
^^^^^^^^^^^^^

- 2025-09-15 Feature Freeze

- 2025-09-22 Beta 1

- 2025-10-13 Release Candidate 1

- 2025-11-03 Release

.. note:: The beta and release candidate schedules allow for up to 3 releases on a weekly schedule depending on the necessity of creating a release.

Release Manager
===============

Ansible Core Team

Planned work
============

* Drop Python 3.11 and add Python 3.14 for controller code
* Drop Python 3.8 and add Python 3.14 for target code
* Tech preview of Play argument specs
* Support for 3rd party fact injection plugins
* Register Projections
* Remove deprecated functionality
* Add controller type hinting for discrete areas of the code
* Decrease testing sanity ignores
* Update ansible-test container images and VMs
* Update ansible-test dependencies

Delayed work
============

The following work has been delayed and retargeted for a future release:

* TBD
