..
   THIS DOCUMENT IS OWNED BY THE ANSIBLE COMMUNITY STEERING COMMITTEE. ALL CHANGES MUST BE APPROVED BY THE STEERING COMMITTEE!
   For small changes (fixing typos, language errors, etc.) create a PR and ping @ansible/steering-committee.
   For other changes, create a `community topic <https://forum.ansible.com/new-topic?category=project&tags=community-wg>`_ to discuss them.
   (Creating a draft PR for this file and mentioning it in the community topic is also OK.)

.. _community_topics_workflow:

Ansible community topics workflow
=================================

Overview
--------

This document describes the Ansible community topics workflow (hereinafter ``Workflow``) to provide guidance on successful resolving topics in the asynchronous way.

The Workflow is a set of actions that need to be done successively within the corresponding time frames.

.. note::

   If you have any ideas on how the Workflow can be improved, please create an issue in this repository or pull request against this document.

Creating a topic
----------------

Any person can `create a topic <https://forum.ansible.com/new-topic?title=topic%20title&body=topic%20body&category=project&tags=community-wg>`_ tagged with ``community-wg`` under the ``Project Discussions`` category in the `Ansible Forum <https://forum.ansible.com/>`_. A :ref:`Steering Committee member<steering_members>` can tag the forum post with `community-wg-nextmtg` to put it on the meeting agenda.

Workflow
========

.. note::

  This is a rough scenario and it can vary depending on a topic's complexity and other nuances, for example, when there is a mass agreement upfront.

Preparation stage
-----------------

A Committee person checks the topic's content, asks the author/other persons to provide additional information if needed.

Discussion stage
----------------

* If the topic is ready to be discussed, the Committee person:

  * Adds the ``community-wg-nextmtg`` tag if it needs to be discussed in the meeting.

  * Opens the discussion by adding a comment asking the Community and the Committee to take part in it.

* No synchronous discussion is needed (there are no blockers, complications, confusion, or impasses).

Voting stage
------------

* Depending on the topic's complexity, 1-2 weeks after the discussion was opened, the Committee person formulates vote options based on the prior discussion and gives participants reasonable amount of time to propose changes to the options (no longer than a week). The person summarizes the options in a comment and also establishes a date when the vote begins if there are no objections about the options / vote date.
* In the vote date, the vote starts with the comment of a Committee person which opens the vote and establishes a date when the vote ends ($CURRENT_DATE + no longer than 21 days; usually it should not exceed 14 days, 21 days should only be used if it is known that a lot of interested persons will likely not have time to vote in a 14 days period).
* The Committee person labels the topic with the ``active-vote`` tag.
* The Committee person adds ``[Vote ends on $YYYY-MM-DD]`` to the beginning of the topic's description.
* A vote is actually two polls, one for the Steering Committee, one for everyone else. To create a vote in a topic:

  * Create a new post in the topic.

  * Click the ``gear`` button in the composer and select ``Build Poll``.

  * Click the ``gear`` in the Poll Builder for advanced mode.

  * Set up the options (generally this will be Single Choice but other poll types can be used).

  * Title it "Steering Committee vote" and "Limit voting" to the ``Steering Committee``.

  * Do not set the close date because this cannot be changed later.

  * Results should be "Always Visible" unless there is some good reason for the SC votes not to be public.

  * Submit the poll (the BBcode will appear in the post) and then repeat the above for the second poll.

    * The title should be "Community vote".

    * No group limitation.

Voting result stage
-------------------

* The next day after the last day of the vote, the Committee person:

  * Closes the polls.

  * Removes the ``active-vote`` tag.

  * Add a comment that the vote ended.

  * Changes the beginning of the topic's description to ``[Vote ended]``.

  * Creates a summary comment declaring the vote result.

* The vote's result and the final decision are announced via the `Bullhorn newsletter <https://forum.ansible.com/c/news/bullhorn/17>`_.


Implementation stage
--------------------

* If the topic implies some actions (if it does not, just mark this as complete), the Committee person:

  * Assigns the topic to a person responsible for performing the actions.

  * Add the ``being-implemented`` tag to the topic.

  * After the topic is implemented, the assignee:

  * Comments on the topic that the work is done.

  * Removes the ``being-implemented`` tag.

  * Add the ``implemented`` tag.

* If the topic implies actions related to the future Ansible Community package releases (for example, a collection exclusion), the Committee person:

  * Adds the ``scheduled-for-future-release`` tag to the topic.

  * Checks if there is a corresponding milestone in the `ansible-build-data <https://github.com/ansible-community/ansible-build-data/milestones>`_ repository. If there is no milestone, the person creates it.

  * Creates an issue in ansible-build-data that references the topic in community-topics, and adds it to the milestone.

Tools
=====

We have some `scripts <https://github.com/ansible-community/community-topics/tree/main/scripts>`_ that can be used to create Ansible community announcements on Bullhorn and similar.
