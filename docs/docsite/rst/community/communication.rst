.. _communication:

*****************************************
Communicating with the Ansible community
*****************************************

.. contents::
   :local:

Code of Conduct
===============

All communication and interactions in the Ansible Community are governed by our :ref:`code_of_conduct`. Please read and understand it!

.. _ansible_forum:

Forum
=====

The `Ansible Community Forum <https://forum.ansible.com>`_ is a single starting point for questions and help, development discussions, events, and much more. `Register <https://forum.ansible.com/signup?>`_ to join the community. Search by categories and tags to find interesting topics or start a new one; subscribe only to topics you need!

Take a look at the `forum groups <https://forum.ansible.com/g>`_ and join ones that match your interests.
In most cases, joining a forum group automatically subscribes you to related posts.

Want to create a group?
Request it in the `forum topic <https://forum.ansible.com/t/requesting-a-forum-group/503>`_.

.. _communication_irc:

Real-time chat
==============

For real-time interactions, conversations in the Ansible community happen over two chat protocols: Matrix (recommended) and IRC.
The main Matrix and IRC channels exchange messages.
This means you can choose whichever protocol you prefer for the main channels.

.. note::

  Although you can choose either Matrix or IRC, please take into account that many Ansible communities use only Matrix.

Join a channel any time to ask questions, participate in a Working Group meeting, or just say hello.

Ansible community on Matrix
---------------------------

To join the community using Matrix, you need two things:

* a Matrix account (from `Matrix.org <https://app.element.io/#/register>`_ or any other Matrix homeserver)
* a `Matrix client <https://matrix.org/clients/>`_ (we recommend `Element Webchat <https://app.element.io>`_)

The Ansible community maintains its own Matrix homeserver at ``ansible.im``, however, public registration is currently unavailable.

Matrix chat supports:

* persistence (when you log on, you see all messages since you last logged off)
* edits (Let you fix typos and so on. **NOTE** Each edit you make on Matrix re-sends the message to IRC. Please try to avoid multiple edits!)
* replies to individual users
* reactions/emojis
* bridging to IRC
* no line limits
* images

The room links in the :ref:`general_channels` or the :ref:`working_group_list` list will take you directly to the relevant rooms.

If there is no appropriate room for your community, please create it.

For more information, see the community-hosted `Matrix FAQ <https://hackmd.io/@ansible-community/community-matrix-faq>`_.

You can add Matrix shields to your repository's ``README.md`` using the shield in the `community-topics <https://github.com/ansible-community/community-topics#community-topics>`_ repository as a template.

Ansible community on IRC
------------------------

The Ansible community maintains several IRC channels on `irc.libera.chat <https://libera.chat/>`_. To join the community using IRC, you need one thing:

* an IRC client

IRC chat supports:

* no persistence (you only see messages when you are logged on unless you add a bouncer)
* simple text interface
* bridging from Matrix

Our IRC channels may require you to register your IRC nickname. If you receive an error when you connect or when posting a message, see `libera.chat's Nickname Registration guide <https://libera.chat/guides/registration>`_ for instructions. To find all ``ansible`` specific channels on the libera.chat network, use the following command in your IRC client:

.. code-block:: text

   /msg alis LIST #ansible* -min 5

as described in the `libera.chat docs <https://libera.chat/guides/findingchannels>`_.

Our channels record history on the Matrix side. The channel history can be viewed in a browser - all channels will report an appropriate link to ``chat.ansible.im`` in their Chanserv entrymsg upon joining the room. Alternatively, a URL of the form ``https://chat.ansible.im/#/room/# {IRC channel name}:libera.chat`` will also work, for example -  for the #ansible-docs channel it would be `https://app.element.io/#/room/#ansible-docs:libera.chat`.

.. _general_channels:

General channels
----------------

The clickable links will take you directly to the relevant Matrix room in your browser; room/channel information is also given for use in other clients:

- `Community social room and posting news for the Bullhorn newsletter <https://matrix.to:/#/#social:ansible.com>`_ - ``Matrix: #social:ansible.com | IRC: #ansible-social``
- `General usage and support questions <https://matrix.to:/#/#users:ansible.com>`_ - ``Matrix: #users:ansible.com | IRC: #ansible``
- `Discussions on developer topics and code related to features or bugs <https://matrix.to/#/#devel:ansible.com>`_ - ``Matrix: #devel:ansible.com | IRC: #ansible-devel``
- `Discussions on community and collections related topics <https://matrix.to:/#/#community:ansible.com>`_ - ``Matrix: #community:ansible.com | IRC: #ansible-community``
- `For public community meetings <https://matrix.to/#/#meeting:ansible.im>`_ - ``Matrix: #meeting:ansible.im | IRC: #ansible-meeting``
   - We will generally announce these on one or more of the above mailing lists. See the `meeting schedule <https://github.com/ansible-community/meetings/blob/main/README.md>`_

Working group-specific channels
-------------------------------

Many of the working groups have dedicated chat channels. See the :ref:`working_group_list` for more information.

Regional and Language-specific channels
---------------------------------------

- Comunidad Ansible en español - Matrix: `#espanol:ansible.im <https://matrix.to:/#/#espanol:ansible.im>`_ | IRC: ``#ansible-es``
- Communauté française d'Ansible - Matrix: `#francais:ansible.im <https://matrix.to:/#/#francais:ansible.im>`_ | IRC: ``#ansible-fr``
- Communauté suisse d'Ansible - Matrix: `#suisse:ansible.im <https://matrix.to:/#/#suisse:ansible.im>`_ | IRC: ``#ansible-zh``
- European Ansible Community - Matrix: `#europe:ansible.im <https://matrix.to:/#/#europe:ansible.im>`_ | IRC: ``#ansible-eu``

Meetings on chat
----------------

The Ansible community holds regular meetings on various topics on Matrix/IRC, and anyone who is interested is invited to participate. For more information about Ansible meetings, consult the `meeting schedule and agenda page <https://github.com/ansible-community/meetings/blob/main/README.md>`_.

.. _working_group_list:

Working groups
==============

Working Groups are a way for Ansible community members to self-organize around particular topics of interest.

Our community working groups are represented in Matrix rooms and  `Forum groups <https://forum.ansible.com/g>`_.

Many of them meet in chat. If you want to get involved in a working group, join the Matrix room or IRC channel where it meets or comment on the agenda.

- `AAP Configuration as Code <https://github.com/redhat-cop/controller_configuration/wiki/AAP-Configuration-as-Code>`_ - Matrix: `#aap_config_as_code:ansible.com <https://matrix.to/#/#aap_config_as_code:ansible.com>`_
- `Amazon (AWS) Working Group <https://forum.ansible.com/g/AWS/members>`_ - Matrix: `#aws:ansible.com <https://matrix.to:/#/#aws:ansible.com>`_ | IRC: ``#ansible-aws``
- `AWX Working Group <https://forum.ansible.com/g/AWX/members>`_ - Matrix: `#awx:ansible.com <https://matrix.to:/#/#awx:ansible.com>`_ | IRC: ``#ansible-awx``
- Azure Working Group  - Matrix: `#azure:ansible.com <https://matrix.to:/#/#azure:ansible.com>`_ | IRC: ``#ansible-azure``
- `Community Working Group <https://forum.ansible.com/tags/c/project/7/community-wg>`_ (including Meetups) - Matrix: `#community:ansible.com <https://matrix.to:/#/#community:ansible.com>`_ | IRC: ``#ansible-community``
- Container Working Group  - Matrix: `#container:ansible.com <https://matrix.to:/#/#container:ansible.com>`_ | IRC: ``#ansible-container``
- DigitalOcean Working Group - Matrix: `#digitalocean:ansible.im <https://matrix.to:/#/#digitalocean:ansible.im>`_ | IRC: ``#ansible-digitalocean``
- Diversity Working Group - Matrix: `#diversity:ansible.com <https://matrix.to:/#/#diversity:ansible.com>`_ | IRC: ``#ansible-diversity``
- Docker Working Group - Matrix: `#devel:ansible.com <https://matrix.to:/#/#devel:ansible.com>`_ | IRC: ``#ansible-devel``
- `Documentation Working Group <https://forum.ansible.com/g/Docs>`_ - Matrix: `#docs:ansible.com <https://matrix.to:/#/#docs:ansible.com>`_ | IRC: ``#ansible-docs``
- `Execution Environments Group <https://forum.ansible.com/g/ExecutionEnvs>`_
- `Galaxy Working Group <https://forum.ansible.com/g/galaxy/members>`_ - Matrix: `#galaxy:ansible.com <https://matrix.to:/#/#galaxy:ansible.com>`_ | IRC: ``#ansible-galaxy``
- JBoss Working Group - Matrix: `#jboss:ansible.com <https://matrix.to:/#/#jboss:ansible.com>`_ | IRC: ``#ansible-jboss``
- Kubernetes Working Group - Matrix: `#kubernetes:ansible.com <https://matrix.to:/#/#kubernetes:ansible.com>`_ | IRC: ``#ansible-kubernetes``
- Linode Working Group - Matrix: `#linode:ansible.com <https://matrix.to:/#/#linode:ansible.com>`_ | IRC: ``#ansible-linode``
- Molecule Working Group (`testing platform for Ansible playbooks and roles <https://ansible.readthedocs.io/projects/molecule/>`_) - Matrix: `#molecule:ansible.im <https://matrix.to:/#/#molecule:ansible.im>`_ | IRC: ``#ansible-molecule``
- MySQL Working Group - Matrix: `#mysql:ansible.com <https://matrix.to:/#/#mysql:ansible.com>`_
- `Network Working Group <https://forum.ansible.com/g/network-wg/members>`_ - Matrix: `#network:ansible.com <https://matrix.to:/#/#network:ansible.com>`_ | IRC: ``#ansible-network``
- `PostgreSQL Working Group <https://forum.ansible.com/g/PostgreSQLTeam/>`_ - Matrix: `#postgresql:ansible.com <https://matrix.to:/#/#postgresql:ansible.com>`_
- `Release Management Working Group <https://forum.ansible.com/g/release-managers>`_ - Matrix: `#release-management:ansible.com <https://matrix.to/#/#release-management:ansible.com>`_
- Remote Management Working Group - Matrix: `#devel:ansible.com <https://matrix.to:/#/#devel:ansible.com>`_ | IRC: ``#ansible-devel``
- Storage Working Group - Matrix: `#storage:ansible.com <https://matrix.to/#/#storage:ansible.com>`_ | IRC: ``#ansible-storage``
- VMware Working Group - Matrix: `#vmware:ansible.com <https://matrix.to:/#/#vmware:ansible.com>`_ | IRC: ``#ansible-vmware``
- Windows Working Group - Matrix: `#windows:ansible.com <https://matrix.to:/#/#windows:ansible.com>`_ | IRC: ``#ansible-windows``
- Ansible developer tools Group - Matrix: `#devtools:ansible.com <https://matrix.to/#/#devtools:ansible.com>`_ | IRC: ``#ansible-devtools``

Forming a new working group
----------------------------

The basic components of a working group are:

* Group name and charter (why the group exists).
* Registered :ref:`real-time chat channel<communication_irc>`.
* Group of users (at least two!) who will be driving the agenda of the working group.
* Dedicated `forum group <https://forum.ansible.com/g>`_.

The basic responsibilities of a working group are:

* Follow the :ref:`code_of_conduct`.
* Be responsive on your real-time chat channel.
* Be responsive on the `forum <https://forum.ansible.com/>`_ in related topics.
* Report semi-regularly on the cool stuff that your working group is working on.
* Keep your forum group information updated.


Requesting a working group
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Anyone can request to start a Working Group, for any reason. 

If you need only a `Forum group <https://forum.ansible.com/g>`_, 
request it in the `forum topic <https://forum.ansible.com/t/requesting-a-forum-group/503>`_.

If you also need a real-time chat channel, you can `request one <https://hackmd.io/@ansible-community/community-matrix-faq#How-do-I-create-a-public-community-room>`_.

.. _request_coll_repo:

Requesting a community collection repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Working groups are often built around Ansible community collections. You can use a repository under your organization or request one under `ansible-collections <https://github.com/ansible-collections>`_ on the forum by creating a topic in the `Project Discussions category and the coll-repo-request tag <https://forum.ansible.com/new-topic?category=project&tags=coll-repo-request>`_.

.. _community_topics:

Ansible Community Topics
========================

The :ref:`Ansible Community Steering Committee<steering_responsibilities>` uses the :ref:`ansible_forum` to asynchronously discuss with the Community and vote on Community topics.

Create a `new topic <https://forum.ansible.com/new-topic?category=project&tags=community-wg>`_ if you want to discuss an idea that impacts any of the following:

* Ansible Community
* Community collection best practices and :ref:`requirements<collections_requirements>`
* :ref:`Community collection inclusion policy<steering_inclusion>`
* :ref:`The Community governance<steering_responsibilities>`
* Other proposals of importance that need the Committee or overall Ansible community attention

See the `Community topics workflow <https://forum.ansible.com/new-topic?category=project&tags=community-wg>`_ to learn more.

Ansible Automation Platform support questions
=============================================

Red Hat Ansible `Automation Platform <https://www.ansible.com/products/automation-platform>`_ is a subscription that contains support, certified content, and tooling for Ansible including content management, a controller, UI and REST API.

If you have a question about Ansible Automation Platform, visit `Red Hat support <https://access.redhat.com/products/red-hat-ansible-automation-platform/>`_ rather than using a chat channel or the general project mailing list.

The Bullhorn
============

**The Bullhorn** is our newsletter for the Ansible contributor community. You can get Bullhorn updates
from the :ref:`ansible_forum`.

If you have any questions or content you would like to share, you are welcome to chat with us
in the `Ansible Social room on Matrix<https://matrix.to/#/#social:ansible.com>, and mention
`newsbot <https://matrix.to/#/@newsbot:ansible.im>`_ to have your news item tagged for review for 
the next weekly issue.

Read past issues of `the Bullhorn <https://forum.ansible.com/c/news/bullhorn/17>`_.

Asking questions over email
===========================

.. note::

  This form of communication is deprecated. Consider using the :ref:`ansible_forum` instead.

Your first post to the mailing list will be moderated (to reduce spam), so please allow up to a day or so for your first post to appear.

* `Ansible Announce list <https://groups.google.com/forum/#!forum/ansible-announce>`_ is a read-only list that shares information about new releases of Ansible, and also rare infrequent event information, such as announcements about an upcoming AnsibleFest, which is our official conference series. Worth subscribing to!
* `Ansible AWX List <https://forum.ansible.com/tag/awx>`_ is for `Ansible AWX <https://github.com/ansible/awx>`_
* `Ansible Development List <https://groups.google.com/forum/#!forum/ansible-devel>`_ is for questions about developing Ansible modules (mostly in Python), fixing bugs in the Ansible Core code, asking about prospective feature design, or discussions about extending Ansible or features in progress.
* `Ansible Outreach List <https://groups.google.com/forum/#!forum/ansible-outreach>`_ help with promoting Ansible and `Ansible Meetups <https://www.meetup.com/topics/ansible/>`_
* `Ansible Project List <https://groups.google.com/forum/#!forum/ansible-project>`_ is for sharing Ansible tips, answering questions about playbooks and roles, and general user discussion.
* `Molecule Discussions <https://github.com/ansible-community/molecule/discussions>`_ is designed to aid with the development and testing of Ansible roles with Molecule.

The Ansible mailing lists are hosted on Google, but you do not need a Google account to subscribe. To subscribe to a group from a non-Google account, send an email to the subscription address requesting the subscription. For example: ``ansible-devel+subscribe@googlegroups.com``.
