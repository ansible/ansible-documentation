.. _core_roadmap_2.19:

*****************
Ansible-core 2.19
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

- 2024-10-14 Development Phase 1
- 2024-12-16 Development Phase 2
- 2025-02-17 Development Phase 3
- 2025-04-14 Beta 1

Release Phase
^^^^^^^^^^^^^

- 2025-04-14 Feature Freeze (and ``stable-2.19`` branching from ``devel``)
  No new functionality (including modules/plugins) to any code

- 2025-04-14 Beta 1

- 2025-05-26 Release Candidate 1

- 2025-06-16 Release

.. note:: The beta schedule allows for up to 6 releases and release candidate schedules allow for up to 3 releases on a weekly schedule depending on the necessity of creating a release.

Release Manager
===============

 Ansible Core Team

Planned work
============

* Data Tagging
* No longer allow forks to inherit stdio
* ``ansible-galaxy`` CLI improvements
   * Support relative ``download_url`` in galaxy API responses
   * Add support to ansible-galaxy for new console.redhat.com service account auth
* Evaluate pre-fork loop processing in strategy plugins
* Add alternative to ``sshpass`` to the ``ssh`` connection plugin
* Evaluate inclusion of ``ssh-agent`` handling
* Deprecate ``paramiko`` connection plugin
* Remove deprecated functionality
* Decrease incidental integration tests
* Add controller type hinting for discrete areas of the code
* Decrease testing sanity ignores
* Update ansible-test container images and VMs
* Update ansible-test dependencies

Delayed work
============

The following work has been delayed and retargeted for a future release:

* Register Projections
* ``ansible-galaxy`` CLI improvements
   * Denote preferred collection
   * Add ``uninstall`` command
   * Support rollback on upgrade failures
   * Utilize ``requires_ansible`` during installs/upgrades
* Move environment variable handling for modules out of shell plugins, to support private environment variables
