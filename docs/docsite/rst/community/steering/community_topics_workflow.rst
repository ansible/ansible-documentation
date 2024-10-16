..
   THIS DOCUMENT IS OWNED BY THE ANSIBLE COMMUNITY STEERING COMMITTEE. ALL CHANGES MUST BE APPROVED BY THE STEERING COMMITTEE!
   For small changes (fixing typos, language errors, etc.) create a PR and ping @ansible/steering-committee.
   For other changes, create a `community topic <https://forum.ansible.com/new-topic?category=project&tags=community-wg>`_ to discuss them.
   (Creating a draft PR for this file and mentioning it in the community topic is also OK.)

.. _community_topics_workflow:

Community topics workflow
=========================

Overview
--------

This document describes the Ansible community topics workflow to provide guidance on successful resolving topics in the asynchronous way.

The workflow is a set of actions that need to be completed in order within the corresponding time frames.

.. note::

  The following section outlines a generic scenario for a workflow.
  Workflows can vary depending on a topic's complexity and other nuances; for example, when there is a mass agreement from the beginning.

Creating a topic
----------------

Any person can :ref:`create a community topic<creating_community_topic>`.

Preparation stage
-----------------

* A Committee person checks the topic's content and asks the author/other persons to provide additional information as needed.

Discussion stage
----------------

* By default, the discussion happens asynchronously in the topic.

  * A :ref:`steering committee <steering_responsibilities>` member can tag the forum post with ``community-wg-nextmtg`` to put it on the synchronous meeting agenda.

Voting stage
------------

The Committee person:

* Formulates vote options based on the prior discussion and gives participants up to one week to propose changes to the options. This step takes place one to two weeks after the discussion was opened, depending on the complexity of the topic.
* Summarizes the options in a comment and establishes a date for the vote to begin if there are no objections to the options.
* Starts the vote on the beginning date and establishes an end date, which is $CURRENT_DATE plus:

  * 7 days: simple cases
  * 14 days: maximum vote length
  * 21 days: only used in exceptional cases such as holiday seasons when the majority of the Committee are not able to participate in the vote
* Labels the topic with the ``active-vote`` tag.
* Adds ``[Vote ends on $YYYY-MM-DD]`` to the beginning of the topic's description.

The vote always consists of two polls: one for the Steering Committee, one for everyone else. To create a vote in a topic:

  * Create a new post in the topic.
  * Click the ``gear`` button in the composer and select ``Build Poll``.
  * Click the ``gear`` in the ``Poll Builder`` for advanced mode.
  * Set up the options (generally this will be ``Single Choice`` but other poll types can be used).
  * Title it "Steering Committee vote" and ``Limit voting`` to the ``@SteeringCommittee``.
  * Do NOT set the close date because this cannot be changed later.
  * Results should be ``Always Visible`` unless there is a good reason for the SC votes not to be public.
  * Submit the poll (the BBcode will appear in the post):
  * Repeat the above steps for the second poll:

    * Title should be "Community vote".
    * No group limitation.

Voting result stage
-------------------

On the vote end date, the Committee person:

* Closes the polls if the :ref:`quorum<community_topics_workflow>` is reached, otherwise prolongs the polls.
* Removes the ``active-vote`` tag.
* Adds a comment that the vote has ended.
* Changes the beginning of the topic's description to ``[Vote ended]``.
* Creates a summary comment declaring the vote result.
* Announces the vote result and the final decision in the :ref:`Bullhorn <bullhorn>`.

Implementation stage
--------------------

No further action required
~~~~~~~~~~~~~~~~~~~~~~~~~~

The Committee person:

* Merges an associated pull request if exists.
* Adds the ``resolved`` tag.

Further actions required
~~~~~~~~~~~~~~~~~~~~~~~~

The Committee person:

* Assigns a person responsible for performing the actions by mentioning them in a comment.
* Adds the ``being-implemented`` tag to the topic.

After the actions are done, the assignee:

* Comments on the topic that the work is done.
* Removes the ``being-implemented`` tag.
* Adds the ``implemented`` and ``resolved`` tags.

Package-release related actions required
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the topic implies actions related to the future Ansible community package releases (for example, a collection exclusion), the Committee person/assignee:

* Adds the ``scheduled-for-future-release`` tag to the topic.
* Checks if there is a corresponding milestone in the `ansible-build-data <https://github.com/ansible-community/ansible-build-data/milestones>`_ repository.

  * If there is no milestone, the person creates it.
* Creates an issue in ``ansible-build-data`` that references the topic and adds it to the milestone.
* After it is implemented, adds the ``implemented`` and ``resolved`` tags.

Tools
-----

There are a few `scripts <https://github.com/ansible-community/community-topics/tree/main/scripts>`_ that can be used to create Ansible community announcements on the Bullhorn and similar locations.

.. seealso::

  :ref:`steering committee <steering_responsibilities>`
     Ansible Community Steering Committee
