.. _core_roadmap_2.16:

*****************
Ansible-core 2.16
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

- 2023-05-01 Development Phase 1
- 2023-06-26 Development Phase 2
- 2023-08-07 Development Phase 3

Release Phase
^^^^^^^^^^^^^

- 2023-09-18 Feature Freeze (and ``stable-2.16`` branching from ``devel``)
  No new functionality (including modules/plugins) to any code

- 2023-09-25 Beta 1

- 2023-10-16 Release Candidate 1

- 2023-11-06 Release

.. note:: The beta and release candidate schedules allow for up to 3 releases on a weekly schedule depending on the necessity of creating a release.

Release Manager
===============

 Ansible Core Team

Planned work
============

* Drop Python 3.5 support for module execution
* Drop Python 3.9 support for control node
* Add support to ``ansible-doc`` for collections to declare new plugin types
* Preserve display context when proxying display over the queue
* Update ``TaskExecutor`` to not unnecessarily establish persistent ``ansible-connection`` when not needed
* Remove deprecated functionality
* Decrease incidental integration tests
* Add control node type hinting for discrete areas of the code
* Decrease testing sanity ignores
* Update ansible-test container images and VMs
* Update ansible-test dependencies

Delayed work
============

The following work has been delayed and retargeted for a future release:

* Data Tagging
