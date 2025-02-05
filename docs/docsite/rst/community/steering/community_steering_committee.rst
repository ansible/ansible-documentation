..
   THIS DOCUMENT IS OWNED BY THE ANSIBLE COMMUNITY STEERING COMMITTEE. ALL CHANGES MUST BE APPROVED BY THE STEERING COMMITTEE!
   For small changes (fixing typos, language errors, etc.) create a PR and ping @ansible/steering-committee.
   For other changes, create a `community topic <https://forum.ansible.com/new-topic?category=project&tags=community-wg>`_ to discuss them.
   (Creating a draft PR for this file and mentioning it in the community topic is also OK.)

.. _steering_responsibilities:
 
Steering Committee mission and responsibilities
===============================================

The Steering Committee mission is to provide continuity, guidance, and suggestions to the Ansible community to ensure the delivery and high quality of the Ansible package. In addition, the committee helps decide the technical direction of the Ansible project. It is responsible for approving new proposals and policies in the community, package, and community collections world, new community collection-inclusion requests, and other technical aspects regarding inclusion and packaging.
The Committee should reflect the scope and breadth of the Ansible community.

Steering Committee responsibilities
------------------------------------

The Committee:

* Designs policies and procedures for the community collections world.
* Votes on approval changes to established policies and procedures.
* Reviews community collections for compliance with the policies.
* Helps create and define roadmaps for our deliverables such as the ``ansible`` package, major community collections, and documentation.
* Reviews community collections submitted for inclusion in the Ansible package and decides whether to include them or not.
* Review other proposals of importance that need the Committee's attention and provide feedback.

.. _steering_members:

Current Steering Committee members
-----------------------------------

The following table lists the current Steering Committee members. See :ref:`steering_past_members` for a list of past members.

The Steering Committee itself is also a group in the forum (`@SteeringCommittee <https://forum.ansible.com/g/SteeringCommittee>`_).



.. table:: Current Steering committee members

  +------------------+---------------+--------------+-------------+
  | Name             | GitHub        | Forum        | Start year  |
  +==================+===============+==============+=============+
  | Alexei Znamensky | russoz        | russoz       | 2022        |
  +------------------+---------------+--------------+-------------+
  | Alicia Cozine    | acozine       | acozine      | 2021        |
  +------------------+---------------+--------------+-------------+
  | Andrew Klychkov  | Andersson007  | Andersson007 | 2021        |
  +------------------+---------------+--------------+-------------+
  | Brian Scholer    | briantist     | briantist    | 2022        |
  +------------------+---------------+--------------+-------------+
  | Core Team repr.  | See Forum     |              | 2024        |
  +------------------+---------------+--------------+-------------+
  | Dylan Silva      | thaumos       | thaumos      | 2021        |
  +------------------+---------------+--------------+-------------+
  | Felix Fontein    | felixfontein  | felixfontein | 2021        |
  +------------------+---------------+--------------+-------------+
  | James Cassell    | jamescassell  | cassel       | 2021        |
  +------------------+---------------+--------------+-------------+
  | John Barker      | gundalow      | gundalow     | 2021        |
  +------------------+---------------+--------------+-------------+
  | Mario Lenz       | mariolenz     | mariolenz    | 2022        |
  +------------------+---------------+--------------+-------------+
  | Markus Bergholz  | markuman      | markuman     | 2022        |
  +------------------+---------------+--------------+-------------+
  | Maxwell G        | gotmax23      | gotmax23     | 2022        |
  +------------------+---------------+--------------+-------------+
  | Sorin Sbarnea    | ssbarnea      | ssbarnea     | 2021        |
  +------------------+---------------+--------------+-------------+


John Barker (`gundalow <https://github.com/gundalow>`_) has been elected by the Committee as its :ref:`chairperson`.

Committee members are selected based on their active contribution to the Ansible Project and its community. See :ref:`community_steering_guidelines` to learn details.

.. _creating_community_topic:

Creating new policy proposals & inclusion requests
----------------------------------------------------

The Committee uses the `Ansible Forum <https://forum.ansible.com/>`_ to asynchronously discuss with the Community and vote on the proposals in corresponding `community topics <https://forum.ansible.com/tags/c/project/7/community-wg>`_.

You can `create a community topic <https://forum.ansible.com/new-topic?category=project&tags=community-wg>`_ (make sure you use the ``Project Discussions`` category and the ``community-wg`` tag) if you want to discuss an idea that impacts any of the following:

  * Ansible Community
  * Community collection best practices and requirements
  * Community collection inclusion/exclusion policy and workflow
  * The Community governance
  * Other proposals of importance that need the Committee's or overall Ansible community attention

To request changes to the inclusion policy and :ref:`collections_requirements`:

#. Submit a new pull request against the document by clicking the ``Edit`` button on its web page.
#. Create a `community topic <https://forum.ansible.com/new-topic?category=project&tags=community-wg>`_ containing the rationale for the proposed changes.

To submit new collections for inclusion into the Ansible package:

* Submit the new collection inclusion requests through a new discussion in the `ansible-inclusion <https://github.com/ansible-collections/ansible-inclusion/discussions/new>`_ repository.

Depending on a topic you want to discuss with the Community and the Committee, as you prepare your proposal, please consider the requirements established by:

* :ref:`code_of_conduct`.
* :ref:`collections_requirements`.
* `Ansible Collection Inclusion Checklist <https://github.com/ansible-collections/ansible-inclusion/blob/main/collection_checklist.md>`_.
* :ref:`removal_from_ansible`.

.. _community_topics_workflow:

Community topics workflow
^^^^^^^^^^^^^^^^^^^^^^^^^

The Committee uses the :ref:`community_topics_workflow` to asynchronously discuss and vote on the `community topics <https://forum.ansible.com/tags/c/project/7/community-wg>`_.

The quorum, the minimum number of Committee members who must vote on a topic in order for a decision to be officially made, is half of the whole number of the Committee members. If the quorum number contains a fractional part, it is rounded up to the next whole number. For example, if there are thirteen members currently in the committee, the quorum will be seven.

Votes must always have "no change" as an option.

In case of equal numbers of votes for and against a topic, the chairperson's vote will break the tie. For example, if there are six votes for and six votes against a topic, and the chairperson's vote is among those six which are for the topic, the final decision will be positive. If the chairperson has not voted yet, other members ask them to vote.

For votes with more than two options, one choice must have at least half of the votes. If two choices happen to both have half of the votes, the chairperson's vote will break the tie. If no choice has at least half of the votes, the vote choices have to be adjusted so that a majority can be found for a choice in a new vote.

Community topics triage
^^^^^^^^^^^^^^^^^^^^^^^

The Committee conducts a triage of `community topics <https://forum.ansible.com/tags/c/project/7/community-wg>`_ periodically (every three to six months).

The triage goals are:

* Sparking interest for forgotten topics.
* Identifying and closing irrelevant topics, for example, when the reason of the topic does not exist anymore or the topic is out of the Committee responsibilities scope.
* Identifying and closing topics that the Community are not interested in discussing. As indicators, it can be absence of comments or no activity in comments, at least, for the last six months.
* Identifying and closing topics that were solved and implemented but not closed (in this case, such a topic can be closed on the spot with a comment that it has been implemented).
* Identifying topics that have been in pending state for a long time, for example, when it is waiting for actions from someone for several months or when the topics were solved but not implemented.

A person starting the triage:

#. Identifies the topics mentioned above.
#. Creates a special triage topic containing an enumerated list of the topics-candidates for closing.
#. Establishes a vote date considering a number of topics, their complexity and comment-history size giving the Community sufficient time to go through and discuss them.
#. The Community and the Committee vote on each topic-candidate listed in the triage topic whether to close it or keep it open.

.. _steering_inclusion:

Collection inclusion requests workflow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When reviewing community collection `inclusion requests <https://github.com/ansible-collections/ansible-inclusion/discussions>`_, the Committee members check if a collection adheres to the :ref:`collections_requirements`.

.. note::

  The Steering Committee can reject a collection inclusion request or exclude a collection from the Ansible package even when the collection satisfies the requirements if the Steering Committee agrees that presence of the collection will significantly deteriorate the Ansible package user experience or the package build process. In case of rejection/removal, the collection maintainers receive comprehensive feedback from the Committee explaining the reasons of starting the process. In case the reasons are fixable, the feedback will contain information what the maintainers need to change.

#. A Committee member who conducts the inclusion review copies the `Ansible community collection checklist <https://github.com/ansible-collections/ansible-inclusion/blob/main/collection_checklist.md>`_ into a corresponding `discussion <https://github.com/ansible-collections/ansible-inclusion/discussions>`_.

#. In the course of the review, the Committee member marks items as completed or leaves a comment saying whether the reviewer expects an issue to be addressed or whether it is optional (for example, it could be **MUST FIX:** <what> or **SHOULD FIX:** <what> under an item).

#. For a collection to be included in the Ansible community package, the collection:

  * MUST be reviewed and approved as compliant with the requirements by at least two Steering Committee members.

    * At least one of the reviews checks compliance with the entire checklist.
    * All subsequent reviews can focus only on compliance with documentation and development conventions.

  * Reviewers must not be involved significantly in development of the collection. They MUST declare any potential conflict of interest (for example, being friends/relatives/coworkers of the maintainers/authors, being users of the collection, or having contributed to that collection recently or in the past).

#. After the collection gets two Committee member approvals, a Committee member creates a `community topic <https://forum.ansible.com/new-topic?category=project&tags=community-wg>`_ linked to the corresponding inclusion request. The issue's description says that the collection has been approved by the Committee and establishes a date (a week by default) when the inclusion decision will be considered made.

  * The inclusion automatically gets suspended if the Committee members raise concerns or start another inclusion review within this time period.
  * When there are no more objections or ongoing inclusion reviews, the inclusion date gets prolonged for another week.

#. If the inclusion has not been suspended by the established date, the inclusion request is considered successfully resolved. In this case, a Committee member:

  #. Declares the decision in the topic and in the inclusion request.
  #. Moves the request to the ``Resolved reviews`` category.
  #. Adds the collection to the ``ansible.in`` file in a corresponding directory of the `ansible-build-data repository <https://github.com/ansible-community/ansible-build-data>`_.
  #. Announces the inclusion through the `Bullhorn newsletter <https://forum.ansible.com/c/news/bullhorn/17>`_.
  #. Closes the topic.

Collection exclusion workflow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Committee uses the :ref:`removal_from_ansible` to remove collections not satisfying the :ref:`collections_requirements` from the Ansible package. 

.. _community_wg_meetings:

Community Working Group meetings
---------------------------------

See the Community Working Group meeting `schedule <https://github.com/ansible-community/meetings/tree/main#wednesdays>`_. Meeting summaries are posted on the `Forum <https://forum.ansible.com/tags/c/workflow/meetbot/16/community-wg>`_.

.. note::

  Participation in the Community Working Group meetings is optional for Committee members. Decisions on `community topics <https://forum.ansible.com/tags/c/project/7/community-wg>`_ are made asynchronously in the topics themselves.

