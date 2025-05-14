.. _maintainer_requirements:

Maintainer responsibilities
===========================

This document is intended for:

* Contributors to collections who are interested in joining their maintainer teams.
* Collection maintainers who want to learn more about the subject.

This document explains what a collection maintainer is, outlines their responsibilities, and describes the process for becoming one.

.. contents::
   :depth: 1
   :local:

Collection maintainer definition
--------------------------------

An Ansible collection maintainer (or maintainer for short) is a contributor who:

* Makes significant and regular contributions to the project.
* Has shown themselves as a specialist in the area the collection automates.
* Trusted by the community: to be able to perform their duties, maintainers have the ``write`` or higher access level in the collection.

Maintainer responsibilities
---------------------------

Collection maintainers:

* Act in accordance with the :ref:`code_of_conduct`.
* Subscribe to the repository they maintain (click :guilabel:`Watch > All activity` in GitHub).
* Keep README, development guidelines, and other general :ref:`maintainer_documentation` relevant.
* Review using the :ref:`review_checklist` and commit changes made by other contributors.
* :ref:`Backport <Backporting>` changes to stable branches.
* :ref:`Plan and perform releases <Releasing>`.
* Ensure that the collection adhere to the :ref:`collections_requirements`.
* Track changes announced through the `news-for-maintainers <https://forum.ansible.com/tag/news-for-maintainers>`_ forum tag (click the ``Bell`` button) and update the collection accordingly.
* :ref:`Build a healthy community <expanding_community>` to increase the number of active contributors and maintainers around collections.

Multiple maintainers can divide responsibilities among each other.

Becoming a maintainer
---------------------

If you are interested in becoming a maintainer and satisfy the :ref:`requirements<maintainer_requirements>`, please nominate yourself. You can also nominate another person:

1. Create a GitHub issue in the relevant repository.
2. If there is no response, message the `Red Hat Ansible Community Engineering Team <https://forum.ansible.com/g/CommunityEngTeam>`_ on the `Ansible forum <https://forum.ansible.com/>`_.

Communicating as a maintainer
-----------------------------

Maintainers communicate with the community through channels listed in the :ref:`Ansible communication guide<communication>`.

.. _wg_and_real_time_chat:

Establishing working group communication
----------------------------------------

Working groups depend on efficient communication.
As a maintainer, you can use the following techniques to establish communication for your working groups:

* Find an existing `forum group <https://forum.ansible.com/g>`_ and tags that suit your project and join the conversation.

  * If nothing suits, `request them <https://forum.ansible.com/t/working-groups-things-you-can-ask-for/175>`_.

* Provide working group details and links to chat rooms in the contributor section of your project ``README.md``.
* Encourage contributors to join the forum group and appropriate tags.

Participating in community topics
---------------------------------

The Community and the :ref:`Steering Committee <steering_responsibilities>` asynchronously discuss and vote on the :ref:`community topics<creating_community_topic>`.
The topics impact the whole project or its parts including collections and packaging.

Share your opinion and vote on the topics to help the community make the best decisions.

.. _expanding_community:

Expanding the collection community
==================================

Here are some ways you can expand the community around your collection:

* Have it explicitly in your ``README`` that the collection welcomes new maintainers and contributors.
* Give :ref:`newcomers a positive first experience <collection_new_contributors>`.
* Invite contributors to join forum groups/subscribe to tags related to your project.
* Have :ref:`good documentation <maintainer_documentation>` with guidelines for new contributors.
* Make people feel welcome personally and individually. Greet and thanks them.
* Use labels to show easy fixes and leave non-critical easy fixes to newcomers.
* Offer help explicitly.
* Include quick ways contributors can help and contributor documentation references in your ``README``.
* Be responsive in issues, pull requests (or PRs for short) and other communication channels.
* Conduct PR days regularly.
* Maintain a zero-tolerance policy towards behavior violating the :ref:`code_of_conduct`.

  * Put information about how people can register code of conduct violations in your ``README`` and ``CONTRIBUTING`` files.

* Look for new maintainers among active contributors.

.. _maintainer_documentation:

Maintaining good collection documentation
=========================================

Look after the collection documentation to ensure:

* It is up-to-date.
* It matches the :ref:`style_guide`.
* Collection module and plugin documentation adheres to the :ref:`Ansible documentation format <module_documenting>`.
* Collection user guides follow the :ref:`Collection documentation format <collections_doc_dir>`.
* Repository files include at least a ``README`` and ``CONTRIBUTING`` file.
* The ``README`` file contains all sections from `collection_template/README.md <https://github.com/ansible-collections/collection_template/blob/main/README.md>`_.
* The ``CONTRIBUTING`` file includes all the details or links to the details on how a new or continuing contributor can contribute to your collection.
