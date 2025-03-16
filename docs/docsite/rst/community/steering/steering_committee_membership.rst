..
   THIS DOCUMENT IS OWNED BY THE ANSIBLE COMMUNITY STEERING COMMITTEE. ALL CHANGES MUST BE APPROVED BY THE STEERING COMMITTEE!
   For small changes (fixing typos, language errors, etc.) create a PR and ping @ansible/steering-committee.
   For other changes, create a :ref:`community topic<creating_community_topic>` to discuss the changes.
   (Creating a draft PR for this file and mentioning it in the community topic is also OK.)

.. _community_steering_guidelines:

Steering Committee membership guidelines
==========================================

This document describes the expectations and policies related to membership in the :ref:`Ansible Community Steering Committee <steering_responsibilities>` (hereinafter the Committee).

.. contents:: Topics:

.. _steering_expectations:

Expectations of a Steering Committee member
-------------------------------------------

As a Committee member, you agree to:

#. Abide by the :ref:`code_of_conduct` in all your interactions with the Community.
#. Be a Community ambassador by representing its needs within the Committee and throughout the decision making process.
#. Asynchronously participate in discussions and voting on the `Community Topics <https://forum.ansible.com/tags/c/project/7/community-wg>`_.
#. Review other proposals of importance that need the Committee's attention and provide feedback.
#. Act for the sake of the Community by not promoting corporate or individual agenda during the decision making process.
#. Engage with the Community in a professional and positive manner, encourage community members to express their opinion.

.. _Joining the committee:

Joining the Steering Committee
-------------------------------

Eligibility
^^^^^^^^^^^

A person is eligible to become a Committee member if they have:

#. A wide knowledge of Ansible and/or its related projects.
#. Active contributions to  Ansible and/or related projects in any form described in the :ref:`collections_contributions`.
#. A consent to follow the :ref:`steering_expectations`.

Team membership
^^^^^^^^^^^^^^^

The Committee can accept a team to be a member.
In this case, the team chooses its representative and announces the person in a dedicated `Community Topic <https://forum.ansible.com/tags/c/project/7/community-wg>`_.
After the announcement is made, the new representative is added to the `SteeringCommittee <https://forum.ansible.com/g/SteeringCommittee>`_ group on the forum, and the previous representative is removed from that group.

The team uses the same Community Topic for announcing subsequent representative changes. Representatives should commit to at least two months of membership.

The team representative must still abide by all expectations listed in :ref:`steering_expectations`, including those surrounding participation.
Steering Committee members are generally expected to participate in discussions — asynchronously on the forum and/or synchronously in meetings — and votes,
even if the issue in question does not entirely pertain to the team they represent.

Process
^^^^^^^^

Any community member may nominate someone or themselves for Steering Committee membership.

The process to join the Steering Committee consists of the following steps:

#. The nominator contacts one of the :ref:`current Committee members <steering_members>` or by sending an email to ``ansible-community@redhat.com``. Existing members nominating would skip to the following step.
#. A Committee member who receives the nomination must inform the Committee about it by forwarding the full nomination message in a private message to the `SteeringCommittee <https://forum.ansible.com/g/SteeringCommittee>`_ group on the forum.
#. The vote is conducted in the forum thread. Nominees must receive a majority of votes from the present Committee members to be added to the Committee.
#. Provided that the vote result is positive, it is announced in the `Bullhorn <https://forum.ansible.com/t/about-the-newsletter-category/166>`_ newsletter and the new member is added to the :ref:`Committee member list <steering_members>`.

Leaving the Steering Committee
-------------------------------

Steering Committee members can resign voluntarily or be removed by the
rest of the Steering Committee under certain circumstances. See the details
below.

.. _Voluntarily leaving process:

Voluntarily leaving the Steering Committee
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A Committee member can voluntarily leave the Committee.
In this case, the member notifies the other members via a private message to the ``SteeringCommittee`` group in the forum.
This change in the steering committee has also to be announced in Bullhorn.
If the member voluntarily leaving does not want to write this announcement, one of the remaining Committee members will write it.
After that, they are no longer considered a Committee member.

Committee members who resign and later change their minds can
rejoin the Committee by following the :ref:`Process for joining the Steering Committee<Joining the committee>`.

Involuntarily leaving the Steering Committee
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A Committee member will be removed from the Committee if they:

#. Do not participate in asynchronous discussions and voting on `Community Topics <https://forum.ansible.com/tags/c/project/7/community-wg>`_ for more than 3 months in a row.
#. Participate unreasonably irregularly (for example, once a month for several months). Unreasonably is defined by other Committee members considering circumstances in each particular case.
#. Violate the :ref:`code_of_conduct`.

.. _Absence or irregular participation removal process:

Absence or irregular participation in discussing topics and votes
..................................................................

In case of absence or irregular participation, the removal process consists of the following steps:

#. Another Committee member (hereinafter the initiator) contacts the person by PM on the forum asking if they are still interested in fulfilling their Committee member's duties.

  * If the answer is negative, the initiator asks the person to :ref:`step down voluntarily<Voluntarily leaving process>`.

#. If there is no response from the person within a week after the message was sent, the initiator contacts the person by email asking if they are still interested in fulfilling their Committee member's duties.

  * If the answer is negative, the initiator asks the person to :ref:`step down voluntarily<Voluntarily leaving process>`.

#. In case there is no response from the person within a week after the message was sent or if the person agreed to step down but has no time to do it themselves, the initiator:

  * Sends a private message to the ``SteeringCommittee`` group on the forum.

  * The message title is ``Steering Committee member audit.``.

  * The message body must not contain or imply any form of condemnation.

  * It must mention that the person has been inactive and, in accordance with the Steering Committee policies, their place should be freed for another person who can continue their great job.

  * The message should thank the Committee member for their time and effort they spent serving the Community during their time on the Committee.

#. The Committee members vote in the thread.
#. If the Committee votes for removal, a pull request is raised to move the person from the :ref:`steering_members` list to the :ref:`steering_past_members` and merged.

Ansible Community Code of Conduct violations
.............................................

In case of the `Ansible Community Code of Conduct <https://docs.ansible.com/ansible/latest/community/code_of_conduct.html>`_ violations, the process is the same as above except steps 1-2. Instead:

#. The initiator reports the case to the Committee by email.

#. The Committee discusses the case internally, evaluates its severity, and possible solutions.

#. If the Committee concludes that the violation is not severe, it develops a proposal to the person on how the situation can be corrected and further interactions with the Community improved.

#. A Committee representative reaches out to the person with the proposal.

#. The removal process starts if:

  * The Committee decided that the severity of the violation excludes the possibility of further membership.

  * The person does not respond to the proposal.

  * The person explicitly rejects the proposal.

In the case of starting the removal process, the topic's description in the reason's part changes correspondingly.

.. _chairperson:

Chairperson
------------

The chairperson election happens once a year at the time the Committee agrees on by voting in a dedicated forum thread.
If the current chairperson has to step down early, the election happens immediately.

The process of the election consists of the following steps:

#. Send a private message to the `Steering Committee <https://forum.ansible.com/g/SteeringCommittee>`_ forum group.
#. Members interested in being the chairperson nominate themselves in the thread.
#. Conduct anonymous voting in the thread.
#. Internally and publicly announce the elected candidate.

The chairperson has the following powers unlike regular members:

* The chairperson's vote breaks ties to resolve deadlocks when equal numbers of steering committee members vote for and against a `community topic <https://forum.ansible.com/tags/c/project/7/community-wg>`_.
