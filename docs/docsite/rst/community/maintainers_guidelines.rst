.. _maintainer_requirements:

Maintainer responsibilities
===========================

This document provides guidance for:

* Contributors to collections who want to join maintainer teams.
* Collection maintainers seeking to understand their roles better.

This document defines the role of an Ansible collection maintainer, outlines their responsibilities, and describes the process for becoming one.

.. contents::
   :depth: 1
   :local:

Collection maintainer definition
--------------------------------

An Ansible collection maintainer, or simply maintainer, is a contributor who:

* Makes significant and regular contributions to a project.
* Demonstrates expertise in the area the collection automates.
* Earns the community's trust. To fulfill their duties, maintainers have ``write`` or higher access to the collection.

Maintainer responsibilities
---------------------------

Collection maintainers perform the following tasks:

* Act in accordance with the :ref:`code_of_conduct`.
* Subscribe to the repository they maintain. In GitHub, click :guilabel:`Watch > All activity`.
* Keep the ``README``, development guidelines, and other general :ref:`maintainer_documentation` current.
* Review and commit changes from other contributors using the :ref:`review_checklist`.
* :ref:`Backport <Backporting>` changes to stable branches.
* :ref:`Plan and perform releases <Releasing>`.
* Ensure the collection adheres to the :ref:`collections_requirements`.
* Track changes announced through the `news-for-maintainers <https://forum.ansible.com/tag/news-for-maintainers>`_ forum tag. Click the ``Bell`` button to subscribe. Update the collection accordingly.
* :ref:`Build a healthy community <expanding_community>` to increase the number of active contributors and maintainers for collections.

Multiple maintainers can divide these responsibilities among themselves.

Becoming a maintainer
---------------------

If you are interested in becoming a maintainer and meet the :ref:`requirements<maintainer_requirements>`, nominate yourself. You can also nominate another person by following these steps:

1. Create a GitHub issue in the relevant repository.
2. If you receive no response, message the `Red Hat Ansible Community Engineering Team <https://forum.ansible.com/g/CommunityEngTeam>`_ on the `Ansible forum <https://forum.ansible.com/>`_.

Communicating as a maintainer
-----------------------------

Maintainers communicate with the community through the channels listed in the :ref:`Ansible communication guide<communication>`.

.. _wg_and_real_time_chat:

Establishing working group communication
----------------------------------------

Working groups rely on efficient communication. As a maintainer, you can establish communication for your working groups using these techniques:

* Find and join an existing `forum group <https://forum.ansible.com/g>`_ and use tags that suit your project.

  * If no suitable options exist, `request them <https://forum.ansible.com/t/working-groups-things-you-can-ask-for/175>`_.

* Provide working group details and chat room links in the contributor section of your project's ``README.md``.
* Encourage contributors to join the forum group and use appropriate tags.

Participating in community topics
---------------------------------

The Community and the :ref:`Steering Committee <steering_responsibilities>` discuss and vote on :ref:`community topics<creating_community_topic>` asynchronously. These topics impact the entire project or its components, including collections and packaging.

Share your opinion and vote on the topics to help the community make informed decisions.

.. _expanding_community:

Expanding the collection community
==================================

You can expand the community around your collection in the following ways:

* Explicitly state in your ``README`` that the collection welcomes new maintainers and contributors.
* Give :ref:`newcomers a positive first experience <collection_new_contributors>`.
* Invite contributors to join forum groups and subscribe to tags related to your project.
* Maintain :ref:`good documentation <maintainer_documentation>` with guidelines for new contributors.
* Make people feel welcome personally and individually. Greet and thank them.
* Use labels to identify easy fixes and leave non-critical easy fixes to newcomers.
* Offer help explicitly.
* Include quick ways contributors can help and provide contributor documentation references in your ``README``.
* Be responsive in issues, pull requests (PRs), and other communication channels.
* Conduct PR days regularly.
* Maintain a zero-tolerance policy toward behavior that violates the :ref:`code_of_conduct`.
  * Include information about how people can report code of conduct violations in your ``README`` and ``CONTRIBUTING`` files.

* Look for new maintainers among active contributors.

.. _maintainer_documentation:

Maintaining good collection documentation
=========================================

Ensure the collection documentation meets these criteria:

* It is up-to-date.
* It matches the :ref:`style_guide`.
* Collection module and plugin documentation adheres to the :ref:`Ansible documentation format <module_documenting>`.
* Collection user guides follow the :ref:`Collection documentation format <collections_doc_dir>`.
* Repository files include at least a ``README`` and ``CONTRIBUTING`` file.
* The ``README`` file contains all sections from `collection_template/README.md <https://github.com/ansible-collections/collection_template/blob/main/README.md>`_.
* The ``CONTRIBUTING`` file includes all details or links to details on how new or continuing contributors can contribute to your collection.
