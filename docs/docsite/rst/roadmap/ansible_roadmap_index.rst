.. _ansible_roadmaps:

Ansible Roadmap
===============

The Ansible team develops a roadmap for each major and minor Ansible release. The latest roadmap shows current work; older roadmaps provide a history of the project. We don't publish roadmaps for subminor versions. So 2.10 and 2.11 have roadmaps, but 2.10.1 does not.

We incorporate team and community feedback in each roadmap, and aim for further transparency and better inclusion of both community desires and submissions.

Each roadmap offers a *best guess*, based on the Ansible team's experience and on requests and feedback from the community, of what will be included in a given release. However, some items on the roadmap may be dropped due to time constraints, lack of community maintainers, and so on.

Each roadmap is published both as an idea of what is upcoming in Ansible, and as a medium for seeking further feedback from the community.

You can submit feedback on the current roadmap by creating a :ref:`community topic<creating_community_topic>`.

Visit the :ref:`Ansible communication guide<communication>` for details on how to join and use Ansible communication platforms.

.. _ansible_general_major_release_schedule:

General release schedule for a new major Ansible release
--------------------------------------------------------

The release of a new major Ansible version (``X.0.0``) is coupled to a new major ansible-core release (``2.Y.0``). This section describes the general schedule. A more specific schedule will be mentioned on each major version's roadmap page (see below). If ansible-core releases are delayed, the Ansible release schedule is usually updated to adhere to this general release schedule.

The generic release schedule of a new major Ansible version ``X.0.0`` can be split up into three phases:

1. When ansible-core 2.Y.0 **beta** releases are published, there will be one Ansible X.0.0 **alpha** release roughly one day after the corresponding ansible-core beta release.

1. When ansible-core 2.Y.0 **rc (release candidate)** releases are published, there will be one Ansible X.0.0 **alpha** release roughly one day after the corresponding ansible-core rc release.

1. When ansible-core 2.Y.0 is generally made available (usually on a Monday), the following schedule will happen from that day on:

    1. The day of the ansible-core 2.Y.0 day is the last day for collections to make backwards incompatible releases that will be accepted into Ansible X.0.0. This includes adding new collections to Ansible X.0.0; from now on new collections have to wait for X.1.0 or later.

    1. Ansible's feature freeze will happen on the next day (usually Tuesday), and the first (and usually only) Ansible X.0.0 **beta** release (b1) will be made.

    1. One week later (again on Tuesday), the first Ansible X.0.0 **rc (release candidate)** will be released. For this release, only bugfix updates for collections are accepted from the versions included in the Ansible X.0.0 b1.

    1. If no release blockers showed up by Friday of the same week, Ansible X.0.0 will be made generally available on Tuesday of the following week (thus one week after X.0.0 rc1).

    1. If there have been release blockers, a second release candidate release, Ansible X.0.0 rc2, will happen on Tuesday of the following week (one week after X.0.0 rc1), and the general availability will usually happen one week after that (again on a Tuesday).

    1. Four weeks after the ansible-core 2.Y.0 release, and 1-2 weeks after the Ansible X.0.0 release, ansible-core 2.Y.1 will be released on (usually) a Monday, and one day later (usually Tuesday) there will be the Ansible X.1.0 release.

    Note that the schedule might be extended with further Ansible X.0.0 beta or X.0.0 release candidate releases if circumstances require additional time, such as when larger changes in ansible-core require more testing in collections.
    The above schedule (especially with X.0.0 being generally available one week after X.0.0 rc1) is an optimistic schedule, which usually works fine, but might not always provide enough time.


.. toctree::
   :maxdepth: 1
   :glob:
   :caption: Ansible Release Roadmaps
   
   COLLECTIONS_14
   COLLECTIONS_13
   COLLECTIONS_12
   COLLECTIONS_11
   COLLECTIONS_10
   COLLECTIONS_9
   COLLECTIONS_8
   COLLECTIONS_7
   COLLECTIONS_6
   COLLECTIONS_5
   COLLECTIONS_4
   COLLECTIONS_3_0
   COLLECTIONS_2_10
   old_roadmap_index
