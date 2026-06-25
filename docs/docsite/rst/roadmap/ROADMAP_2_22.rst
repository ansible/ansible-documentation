.. _core_roadmap_2.22:

*****************
Ansible-core 2.22
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

- 2026-04-27 Development Phase 1
- 2026-05-25 Development Phase 2
- 2026-06-22 Development Phase 3
- 2026-07-20 Development Phase 4
- 2026-08-17 Development Phase 5

Release Phase
^^^^^^^^^^^^^

- 2026-09-14 Feature Freeze

- 2026-09-21 Beta 1

- 2026-10-12 Release Candidate 1

- 2026-11-02 Release

.. note:: The beta and release candidate schedules allow for up to 3 releases on a weekly schedule depending on the necessity of creating a release.

Release Manager
===============

Ansible Core Team

Planned work
============

* Add Python 3.15 support
* Drop Python 3.12 for controller
* Windows connection resiliency and performance improvements
* Introspection/debugging of running core processes
* Deprecate module/actions returning ``skipped``
* Enable Pipelining by default

Delayed work
============

The following work has been delayed and retargeted for a future release:

* Drop Python 3.9 on target (delayed for 2.23)
