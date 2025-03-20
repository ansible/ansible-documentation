..
   THIS DOCUMENT IS OWNED BY THE ANSIBLE COMMUNITY STEERING COMMITTEE. ALL CHANGES MUST BE APPROVED BY THE STEERING COMMITTEE!
   For small changes (fixing typos, language errors, etc.) create a PR and ping @ansible/steering-committee.
   For other changes, create a :ref:`topic<creating_community_topic>` on the Forum to discuss the changes.
   (Creating a draft PR for this file and mentioning it in the community topic is also OK.)

.. _collections_requirements:

**************************************************
Ansible community package collections requirements
**************************************************

.. contents::
    :local:

Overview
========

This document describes the requirements for maintainers of Ansible community collections included in the Ansible community package. All inclusion candidates and already included collections must meet the criteria marked with ``MUST`` in this document.

You can also find these requirements on the `Collection inclusion criteria checklist <https://github.com/ansible-collections/overview/blob/main/collection_checklist.md>`_.

Every rejected candidate will get feedback from the :ref:`community_steering_committee` based on a decision made in a dedicated :ref:`community topic<creating_community_topic>`.

Feedback and communications
==============================

Any feedback and help is very welcome. Please create a :ref:`community topic<creating_community_topic>` or bring your questions to the :ref:`community meeting<community_wg_meetings>`.

Keeping informed
================

To track changes that affect collections:

* Join the `Collection Maintainers & Contributors forum group <https://forum.ansible.com/g/CollectionMaintainer>`_.
* Subscribe to the :ref:`bullhorn` Ansible contributor newsletter.

.. _coll_wg_reqs:

Communication and Working Groups
================================

Forum overview
--------------

The :ref:`ansible_forum` is our asynchronous default communication platform.

In the context of organizing communication around Ansible collections, you need to understand the following notions:

* `Tags <https://forum.ansible.com/tags>`_: together with categories, tags are the main feature used in the Forum to organize conversations around specific topics. Most Ansible projects have one or more associated tags. For Ansible collections the main tag name is usually the technology the collection targets: examples include `kubernetes <https://forum.ansible.com/tag/kubernetes>`_ for ``kubernetes.core``, `windows <https://forum.ansible.com/tag/windows>`_ for ``ansible.windows``, and `postgresql <https://forum.ansible.com/tag/postgresql>`_ for ``community.postgresql``.
* `Forum groups <https://forum.ansible.com/g>`_: groups allow you to organize users, manage permissions, have a working group page that provides related information, automatically subscribe members to tags, mention or message the whole group, and more. An example collection working group is the `PostgreSQL Ansible Collection Working Group <https://forum.ansible.com/g/PostgreSQLTeam>`_.

See the `Working Groups - things you can ask for! <https://forum.ansible.com/t/working-groups-things-you-can-ask-for/175>`_ forum topic for more details.

Communication requirements
--------------------------

Your collection:

* MUST have a corresponding public tag in the :ref:`ansible_forum` or reuse at least one of the `existing tags <https://forum.ansible.com/tags>`_.

  * Multiple collections can share a tag if they cover similar topics; for example, ``amazon.aws`` and ``community.aws`` could both use the tag ``aws``.

  * In addition, the collection can :ref:`request a forum group<requesting_forum_group>`. If the collection requests or already has a group:

     * All related tags MUST be associated with the group. Everyone who joins the group is automatically subscribed to the tags.
     * The group MUST be public and free to join by any forum user.

  * Use the `Requesting a tag/forum group <https://forum.ansible.com/t/requesting-a-tag-forum-group/503>`_ topic to request a tag and a forum group.

* MUST have a communication section in its README with references to the :ref:`ansible_forum` similar to the `collection_template README.md <https://github.com/ansible-collections/collection_template#communication>`_.

  * The section MUST contain at least a reference to the `Get Help <https://forum.ansible.com/c/help/6>`_ forum category, potentially including a tag in the URL.
  * The section MUST contain information on which tags participants should use for collection-related topics.
  * If the collection has a forum group, the section MUST contain a reference to the group.
  * Descriptions of the references MUST welcome readers to join and participate.
  * Maintainers of the collection SHOULD be subscribed to all associated tags and be members of all associated groups.

* SHOULD have the ``Discussions`` GitHub feature disabled in favor of the Forum.

  * Unless GitHub discussions are currently used, this feature MUST be `disabled on the repo <https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/enabling-or-disabling-github-discussions-for-a-repository>`_.

.. _coll_infrastructure_reqs:

Collection infrastructure
=========================

The following guidelines describe the required infrastructure for your collection:

* MUST have a publicly available issue tracker that does not require a paid level of service to create an account and to create and view issues.
* MUST have the issue feature enabled in its repository and accept issue reports from anyone.
* MUST have a Code of Conduct (CoC) compatible with the :ref:`code_of_conduct`.

  * The CoC MUST be linked from the ``README.md`` file, or MUST be present or linked from the ``CODE_OF_CONDUCT.md`` file in the collection root.
  * The recommended approach is have a link to the Ansible :ref:`code_of_conduct`.
  * If the collection has its own CoC, it MUST be evaluated by the :ref:`Diversity and Inclusion working group <working_group_list>` and confirmed as compatible with the :ref:`code_of_conduct`.

* MUST be published to `Ansible Galaxy <https://galaxy.ansible.com>`_ with version 1.0.0 or later.
* MUST contain only objects that follow the :ref:`Licensing rules <coll_licensing_req>`.
* SHOULD NOT contain any large objects (binaries) comparatively to the current Galaxy tarball size limit of 20 MB, For example, do not include package installers for testing purposes.
* SHOULD NOT contain any unnecessary files such as temporary files.

.. _coll_python_compatibility:

Python Compatibility
====================

In addition to the Python requirements specified in this section, collections SHOULD adhere to the tips at :ref:`ansible_and_python_3`.

.. _coll_python_reqs:

Python Requirements
-------------------

Python requirements for a collection vary between **controller environment** and **other environment**.

.. _coll_controller_req:

Controller environment
~~~~~~~~~~~~~~~~~~~~~~

* Collections MUST support all eligible controller Python versions in the controller environment, unless required libraries do not support these Python versions. The :ref:`Steering Committee <steering_responsibilities>` can grant other exceptions on a case-by-case basis.

  * controller environment: the plugins/modules always run in the same environment (Python interpreter, venv, host, and so on) as ansible-core itself.
  * eligible controller Python version: a Python version that is supported on the controller side by at least one ansible-core version that the collection supports. The eligible versions can be determined from the :ref:`ansible_core_support_matrix` and from the ``requires_ansible`` value in ``meta/runtime.yml`` in the collection.

* The collection MUST document all eligible controller Python versions that are **not** supported in the controller environment. See :ref:`coll_python_docs_req` for details.

Other environment
~~~~~~~~~~~~~~~~~

* Collections MUST support all eligible controller Python versions in the other environment, unless required libraries do not support these Python versions. The :ref:`Steering Committee <steering_responsibilities>` can grant other exceptions on a case-by-case basis.

  * other environment: the plugins/modules run not in a controller environment.
  * eligible target Python version: a Python version that is supported on the target side by at least one ansible-core version that the collection supports. The eligible versions can be determined from the :ref:`ansible_core_support_matrix` and from the ``requires_ansible`` value in ``meta/runtime.yml`` in the collection.

* The collection MUST document all eligible target Python versions that are not supported in the other environment. See :ref:`coll_python_docs_req` for details.

Dropping Python versions support
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Because dropping support for a Python version for an existing module/plugin is a breaking change, the collection:

* SHOULD announce it under the deprecated features section in its changelog in previous versions before the support is dropped.
* MUST release a major version that actually drops the support.

.. _coll_python_docs_req:

Python documentation requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* If your collection does not support all eligible controller/target Python versions, you MUST document which versions it supports in the README.
* If most of your collection supports the same Python versions as ansible-core, but some modules and plugins do not, you MUST include the supported Python versions in the documentation for those modules and plugins.

.. _coll_plugin_standards:

Standards for developing module and plugin utilities
====================================================

* ``module_utils`` and ``plugin_utils`` can be marked for only internal use in the collection, but they MUST document this and MUST use a leading underscore for file names.

  * If you change a utility in ``module_utils`` from public to private, you are making a breaking change. If you do this, you must release a new major version of your collection.

* Below are some recommendations for ``module_utils`` documentation:

  * No docstring: everything we recommend for ``other-environment`` is supported.
  * The docstring ``'Python versions supported: same as for controller-environment'``: everything we recommend for ``controller-environment`` is supported.
  * The docstring with specific versions otherwise: ``'Python versions supported: '``.

.. _coll_repo_structure:

Repository structure requirements
==================================

galaxy.yml
----------

* The ``tags`` field MUST be set.
* Collection dependencies MUST meet a set of rules. See the section on :ref:`Collection Dependencies <coll_dependencies>` for details.
* If you plan to split up your collection, the new collection MUST be approved for inclusion before the smaller collections replace the larger in Ansible.
* If you plan to add other collections as dependencies, they MUST run through the formal application process.

.. _coll_readme_req:

README.md
---------

Your collection repository MUST have a ``README.md`` in the root of the collection, see `collection_template/README.md <https://github.com/ansible-collections/collection_template/blob/main/README.md>`_ for an example.

meta/runtime.yml
----------------

Example: `meta/runtime.yml <https://github.com/ansible-collections/collection_template/blob/main/meta/runtime.yml>`_

* The ``meta/runtime.yml`` MUST define the minimum version of ansible-core which this collection works with using the ``requires_ansible`` field. For example, if the collection works with ansible-core 2.16 and later, set ``requires_ansible: '>=2.16'`` in the ``meta/runtime.yml`` file.

.. _coll_module-reqs:

meta/execution-environment.yml
------------------------------

If a collection has controller-side Python package and/or system package requirements, to allow easy :ref:`execution environment<getting_started_ee_index>` building, they SHOULD be listed in corresponding files under the ``meta`` directory, specified in ``meta/execution-environment.yml``, and `verified <https://ansible.readthedocs.io/projects/builder/en/latest/collection_metadata/#when-installing-collections-using-ansible-galaxy>`_.

See the `Collection-level dependencies guide <https://ansible.readthedocs.io/projects/builder/en/latest/collection_metadata/#collection-level-dependencies>`_ for more information and `collection_template/meta <https://github.com/ansible-collections/collection_template/tree/main/meta>`_ directory content as an example.

Modules & Plugins
------------------

* Collections MUST only use the directories specified below in the ``plugins/`` directory and
  only for the purposes listed:

  :Those recognized by ansible-core: ``doc_fragments``, ``modules``, ``module_utils``, ``terminal``, and those listed in :ref:`working_with_plugins`. This list can be verified by looking at the last element of the package argument of each ``*_loader`` in https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/loader.py#L1126
  :plugin_utils: For shared code which is only used controller-side, not in modules.
  :sub_plugins: For other plugins that are managed by plugins inside of collections instead of ansible-core.  We use a subfolder so there aren't conflicts when ansible-core adds new plugin types.

  The core team (which maintains ansible-core) has committed not to use these directories for
  anything which would conflict with the uses specified here.

Other directories
-----------------

* Collections MUST not use files outside ``meta/``, ``plugins/``, ``roles/`` and ``playbooks/`` in any plugin, role, or playbook that can be called by FQCN, used from other collections, or used from user playbooks and roles.

  * A collection MUST work if every file or directory is deleted from the installed collection except those four directories and their contents.
  * Internal plugins, roles and playbooks (artifacts used only in testing, or only to release the collection, or only for some other internal purpose and not used externally) are exempt from this rule and may rely on files in other directories.

.. _coll_docs_structure_reqs:

Documentation requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~

Collections:

* ``MUST`` use :ref:`links and formatting macros <module_documents_linking>`.
* ``SHOULD`` have contributor guidelines in the ``CONTRIBUTING.md`` or ``README.md`` file.

All modules and plugins:

* ``MUST`` include a :ref:`DOCUMENTATION <documentation_block>` block.
* ``MUST`` include an :ref:`EXAMPLES <examples_block>` block (except where not relevant for the plugin type).
* ``MUST`` use FQCNs when referring to modules, plugins and documentation fragments inside and outside the collection including ``ansible.builtin.`` for ansible-core.
* ``MUST`` include a :ref:`RETURN <return_block>` block for modules and other plugins that return data.
* ``MUST`` include the ``version_added`` field when adding new content to an existing collection for entities that support it, for example, for modules, plugins, options, return values, and attributes.

  * You do not have to add ``version_added`` when creating a new collection before its first release.
  * The ``version_added`` field for objects in a collection MUST refer to the version of the collection in which the options were added -- ``NOT`` the version of Ansible or ansible-core.

    * If, for some reason, you need to specify version numbers of Ansible or another collection, you ``MUST`` also provide ``version_added_collection: collection_name``. We strongly recommend to ``NOT`` do this.

.. _coll_workflow:

Contributor Workflow
====================

.. _coll_changlogs_req:

Changelogs
----------

* Collections MUST include a changelog in the `correct format <https://ansible.readthedocs.io/projects/antsibull-changelog/changelog.yaml-format/>`_.

  #. You can generate or check changelogs using `antsibull-changelog <https://github.com/ansible-community/antsibull-changelog>`_ (`documentation <https://ansible.readthedocs.io/projects/antsibull-changelog/changelogs/>`_), which provides consistency for changelogs across collections included in the ``ansible`` package.

.. _coll_versioning_req:

Versioning and deprecation
--------------------------

* Collections MUST adhere to the `Semantic versioning conventions <https://semver.org/>`_:

  * MUST have this information in its ``README.md`` file in the collection root directory.
  * SHOULD have this information in its contributor and maintainer documentation.
  * MUST have changelog entries under correct categories (``Major changes``, ``Minor changes``, ``Bugfixes``, and so on).

* Collections MUST preserve backward compatibility:

  * To preserve backward compatibility for users, every Ansible minor version series (x.Y.z) will keep the major version of a collection constant.

    * For example, if Ansible 3.0.0 includes ``community.general`` 2.2.0, then each 3.Y.z (3.1.z, 3.2.z, and so on) release will include the latest ``community.general`` 2.y.z release available at build time.
    * Ansible 3.y.z will **never** include a ``community.general`` 3.y.z release, even if it is available.
    * Major collection version changes will be included in the next Ansible major release (4.0.0 in this example).
    * Therefore, ensure that the current major release of your collection included in 3.0.0 receives at least bugfixes as long as new 3.Y.Z releases are produced.
  * Since new minor releases are included, you can include new features, modules and plugins. You MUST make sure that you DO NOT break backward compatibility! This means in particular:

    * You can fix bugs in ``patch releases``, but you MUST NOT add new features or deprecate things.
    * You can add new features and deprecate things in ``minor releases`` but you MUST NOT remove things or change the behavior of existing features.
    * You can only remove things or make breaking changes in ``major releases``.
    * See `semantic versioning <https://semver.org/>`_ for more information.

  * We recommend that you ensure if a deprecation is added in a collection version that is included in Ansible 3.y.z, the removal itself will only happen in a collection version included in Ansible 5.0.0 or later, but not in a collection version included in Ansible 4.0.0.

* The collection SHOULD make its policy of releasing and deprecation available to contributors and users in some way, for example, in its README or pinned issue. See `the announcement in community.general <https://github.com/ansible-collections/community.general/issues/582>`_ as an example.

.. _ coll_naming_req:

Naming
======

Collection naming
-----------------

When choosing a name for a brand new namespace:

* Take into consideration the `Namespace limitations <https://galaxy.ansible.com/docs/contributing/namespaces.html#galaxy-namespace-limitations>`_ which list requirements for namespaces in Galaxy.
* If the namespace does not exist yet and is not occupied by anybody else, submit a `namespace request <https://github.com/ansible/galaxy/issues/new/choose>`_ to have it created for you.

Naming recommendations:

* For collections under the ``ansible-collections`` GitHub organization the repository SHOULD be named ``NAMESPACE.COLLECTION``.
* For collections created for working with a particular entity, they should contain the entity name, for example ``community.mysql``.
* For corporate maintained collections, the repository can be named ``COMPANY_NAME.PRODUCT_NAME``, for example ``ibm.db2``.
* Avoid FQCN/repository names:

  * which are unnecessarily long: try to make it compact but clear.
  * contain the same words / collocations in ``NAMESPACE`` and ``COLLECTION`` parts, for example ``my_system.my_system``.

.. note::

  If you plan to get your collection certified on **Red Hat Automation Hub**, please consult with Red Hat Partner Engineering through ``ansiblepartners@redhat.com`` to ensure collection naming compatibility between the community collection on **Galaxy** and the certified collection.

.. _coll_module_name_req:

Module naming
-------------

* Modules that only gather and return information MUST be named ``<something>_info``.
* Modules that gather and return ``ansible_facts`` MUST be named ``<something>_facts`` and MUST NOT return anything but facts.

For more information, refer to the :ref:`Developing modules guidelines <creating_info_facts>`.

.. _coll_licensing_req:

Collection licensing requirements
===================================

These guidelines are the policy for inclusion in the Ansible package and are in addition to any licensing and legal concerns that may otherwise affect your code.

.. note::

  The guidelines below are more restrictive than strictly necessary. We will try to add a larger list of acceptable licenses once we have approval from Red Hat Legal.

There are several types of content in collections which licensing has to address in different ways.

* The content that MUST be licensed with a free software license that is **compatible with** the `GPL-3.0-or-later <https://www.gnu.org/licenses/gpl-3.0-standalone.html>`_:

  * The ``modules/`` directory content.
  * The ``module_utils/`` directory content: ansible-core typically uses the `BSD-2-clause <https://opensource.org/licenses/BSD-2-Clause>`_ license to allow third-party modules to use the ``module_utils`` in cases when those third-party modules have licenses that are incompatible with the GPLv3. Please consider this use case when licensing your own ``module_utils``.
  * Code outside ``plugins/``: if it DOES NOT import code licensed under ``GPL-3.0-or-later`` it may be licensed under another license compatible with ``GPL-3.0-or-later``.
  * Non-code content.
  * To be allowed, the license MUST be considered open source and compatible with ``GPL-3.0-or-later`` on **both**:

    * The `gnu.org license list <https://www.gnu.org/licenses/license-list.html#GPLCompatibleLicenses>`_.
    * The `Debian Free Software Guidelines <https://wiki.debian.org/DFSGLicenses>`_.

* The content that MUST be licensed with the `GPL-3.0-or-later <https://www.gnu.org/licenses/gpl-3.0-standalone.html>`_:

  * All other code in the ``plugins/`` directory except code under the ``modules/`` and ``module_utils/`` directories (see above): these plugins are run inside of the Ansible controller process which is licensed under the ``GPL-3.0-or-later`` and often must import code from the controller. For these reasons, ``GPL-3.0-or-later`` MUST be used.
  * Code outside ``plugins/``: if it imports any other code that is licensed under ``GPL-3.0-or-later``. Note that this applies in particular to unit tests that often import code from ansible-core, ``plugins/``, ``module_utils/``, or ``modules/``, and such code is often licensed under ``GPL-3.0-or-later``.


.. _coll_cla:

Contributor License Agreements
==============================

Collections MUST NOT require community contributors to sign any type of
contributor license agreement (CLA) other than the
`Developer Certificate of Origin (DCO) <https://developercertificate.org/>`_
or similar agreements that only require confirming the provenance of contributions.
This requirement seeks to preserve the community's ownership over its contributions,
prevent unwelcome licensing changes that can occur when one entity
owns the copyrights for an entire project,
and lower barriers to contribution.

.. _coll_repo_management:

Repository management
=====================

* Every collection MUST have a public Git repository.
* Releases of the collection MUST be tagged in its repository.

  * The ``git`` utility with the ``tag`` argument MUST be used to tag the releases.
  * The tag name MUST exactly match the Galaxy version number.
  * Tag names MAY have a ``v`` prefix.
  * Tag names MUST have a consistent format from release to release.

* Collection artifacts released to Galaxy MUST be built from the sources that are tagged in the collection's Git repository as that release.

  * Any changes made during the build process MUST be clearly documented so the collection artifact can be reproduced.

.. _coll_branch_config:

Branch name and configuration
-----------------------------

.. note::

  This subsection is **only** for repositories under `ansible-collections <https://github.com/ansible-collections>`_! Other collection repositories can also follow these guidelines, but do not have to.

* All new repositories MUST have ``main`` as the default branch.
* Pull Requests settings MUST disallow ``merge commits``.
* The following branch protection rules that MUST be enabled for all release branches:

  * ``Require linear history``
  * ``Do not allow bypassing the above settings``

.. _coll_ci_tests:

CI Testing
===========

.. note::

  You can copy the free-to-use `GitHub action workflow file <https://github.com/ansible-collections/collection_template/blob/main/.github/workflows/ansible-test.yml>`_ from the `collection_template <https://github.com/ansible-collections/collection_template/>`_ repository to the ``.github/workflows`` directory in your collection to set up testing through GitHub actions. The workflow covers all the requirements below.

  Add new `ansible-core` versions in a timely manner and consider dropping support and testing against its EOL versions and versions your collection does not support.

  If your collection repository is under the ``ansible-collections`` GitHub organization, please keep in mind that the number of testing jobs is limited and shared across all the collections in the organization. Therefore, focusing on good test coverage of your collection, please avoid testing against unnecessary entities such as ``ansible-core`` EOL versions that your collection does not support.

To receive important announcements that can affect the collections (for example, testing), collection maintainers SHOULD:

* Subscribe to the `news-for-maintainers <https://github.com/ansible-collections/news-for-maintainers>`_ repository.
* Join the `Collection Maintainers & Contributors <https://forum.ansible.com/g/CollectionMaintainer>`_ forum group.

* You MUST run the ``ansible-test sanity`` command from the `latest stable ansible-base/ansible-core branch <https://github.com/ansible/ansible/branches/all?query=stable->`_.

  * Collections MUST run an equivalent of the ``ansible-test sanity --docker`` command.

    * If they do not use ``--docker``, they must make sure that all tests run, in particular the compile and import tests (which should run for all :ref:`supported Python versions <ansible_and_python_3>`).
    * Collections can choose to skip certain Python versions that they explicitly do not support; this needs to be documented in ``README.md`` and in every module and plugin (hint: use a docs fragment). However, we strongly recommend you follow the :ref:`Ansible Python Compatibility <ansible_and_python_3>` section for more details.

* You SHOULD *additionally* run ``ansible-test sanity`` from the ansible/ansible ``devel`` branch so that you find out about new linting requirements earlier.
* The sanity tests MUST pass.

  * You SHOULD avoid adding entries to the ``test/sanity/ignore*.txt`` files to get your tests to pass but it is allowed except in cases listed below.
  * You MUST NOT ignore the following validations. They MUST be fixed and removed from the files before approval:
      * ``validate-modules:doc-choices-do-not-match-spec``
      * ``validate-modules:doc-default-does-not-match-spec``
      * ``validate-modules:doc-missing-type``
      * ``validate-modules:doc-required-mismatch``
      * ``validate-modules:mutually_exclusive-unknown``
      * ``validate-modules:no-log-needed`` (use ``no_log=False`` in the argument spec to flag false positives!)
      * ``validate-modules:nonexistent-parameter-documented``
      * ``validate-modules:parameter-list-no-elements``
      * ``validate-modules:parameter-type-not-in-doc``

  * The following validations MUST not be ignored except in specific circumstances:
      * ``validate-modules:undocumented-parameter``: this MUST only be ignored in one of these two cases:

        1. A dangerous module parameter has been deprecated or removed, and code is present to inform the user that they should not use this specific parameter anymore or that it stopped working intentionally.
        2. Module parameters are only used to pass in data from an accompanying action plugin.

  * All entries in ``ignore-*.txt`` files MUST have a justification in a comment in the files for each entry. For example ``plugins/modules/docker_container.py use-argspec-type-path # uses colon-separated paths, can't use type=path``.

* You MUST run CI against each of the "major versions" (2.14, 2.16, 2.17, etc) of ``ansible-core`` that the collection supports. (Usually the ``HEAD`` of the stable-xxx branches.)
* All CI tests MUST run against every pull request and SHOULD pass before merge.
* At least sanity tests MUST run against a commit that releases the collection; if they do not pass, the collection will NOT be released.

  - If the collection has integration/unit tests, they SHOULD run too; if they do not pass, the errors SHOULD be analyzed to decide whether they should block the release or not.
* All CI tests MUST run regularly (nightly, or at least once per week) to ensure that repositories without regular commits are tested against the latest version of ansible-test from each ansible-core version tested. The results from the regular CI runs MUST be checked regularly.

All of the above can be achieved by using the `GitHub Action template <https://github.com/ansible-collections/collection_template/tree/main/.github/workflows>`_.

To learn how to add tests to your collection, see:

* :ref:`collection_integration_tests`
* :ref:`collection_unit_tests`

.. _coll_migrating_reqs:

When moving modules between collections
=======================================

See :ref:`Migrating content to a different collection <migrate_to_collection>` for complete details.

Generally, we do not object to moving content between collections or moving content from collections included in Ansible to collections outside the Ansible package, as long as semantic versioning is not violated. More precisely, replacing content with redirects is only a minor change if the destination collection is the dependency of the original collection. (See :ref:`coll_dependencies` for more information about adding new dependencies to collections included in Ansible.)

For the community "catch all" collections, we have slightly different rules. We allow to move content out of community.general and community.network to other collections outside of Ansible under the following conditions:

1. The new collection is appropriately licensed and follows the :ref:`Contributor License Agreements <coll_cla>` policy.
2. None of the contributors who contributed to the content in the last 6 months object in a four-week period after the plan to deprecate the module has been announced.
3. There is a deprecation period of at least 6 months during which deprecation warnings are shown. The deprecation notice must mention that the content is moved to a collection outside the Ansible community package and that users need to install that collection separately.
4. If community members or contributors bring up good reasons in these 6 months to cancel the migration, the Steering Committee will discuss these and vote on them before the content is removed.

Redirects are only added if full backwards compatibility can be ensured. If they are not used, tombstoning has to be used, and the tombstone message needs to explicitly mention the new collection and that the content in the new collection is not fully backwards compatible.

.. _coll_development_conventions:

Development conventions
=======================

All modules in your collection:

* MUST satisfy all the requirements listed in the :ref:`module_dev_conventions`.
* MUST satisfy the concept of :term:`idempotency <Idempotency>`: if a module repeatedly runs with the same set of inputs, it will not make any changes on the system.
* MUST NOT query information using special ``state`` option values like ``get``, ``list``, ``query``, or ``info`` -
  create new ``_info`` or ``_facts`` modules instead (for more information, refer to the :ref:`Developing modules guidelines <creating_info_facts>`).
* ``check_mode`` MUST be supported by all ``*_info`` and ``*_facts`` modules (for more information, refer to the :ref:`Development conventions <developing_modules_best_practices>`).

.. _coll_dependencies:

Collection Dependencies
=======================

**Notation:** if foo.bar has a dependency on baz.bam, we say that baz.bam is the collection *depended on*, and foo.bar is the *dependent collection*.

* The collection MUST NOT depend on collections not included in the ``ansible`` package.
* Collection dependencies MUST be published on Galaxy.
* Collection dependencies MUST have a lower bound on the version which is at least 1.0.0.

  * This means that all collection dependencies have to specify lower bounds on the versions, and these lower bounds should be stable releases, and not versions of the form 0.x.y.
  * When creating new collections where collection dependencies are also under development, you need to watch out since Galaxy checks whether dependencies exist in the required versions:

    #. Assume that ``foo.bar`` depends on ``foo.baz``.
    #. First release ``foo.baz`` as 1.0.0.
    #. Then modify ``foo.bar``'s ``galaxy.yml`` to specify ``'>=1.0.0'`` for ``foo.baz``.
    #. Finally release ``foo.bar`` as 1.0.0.

* The dependencies between collections included in Ansible MUST be valid. If a dependency is violated, the involved collections MUST be pinned so that all dependencies are valid again. This means that the version numbers from the previous release are kept or only partially incremented so that the resulting set of versions has no invalid dependencies.

* If a collection has a too strict dependency for a longer time, and forces another collection depended on to be held back, that collection will be removed from the next major Ansible release. What "longer time" means depends on when the next Ansible major release happens. If a dependent collection prevents a new major version of a collection it depends on to be included in the next major Ansible release, the dependent collection will be removed from that major release to avoid blocking the collection being depended on.

* We strongly suggest that collections also test against the ``main`` branches of their dependencies to ensure that incompatibilities with future releases of these are detected as early as possible and can be resolved in time to avoid such problems. Collections depending on other collections must understand that they bear the risk of being removed when they do not ensure compatibility with the latest releases of their dependencies.

* Collections included in Ansible MUST NOT depend on other collections except if they satisfy one of the following cases:

  #. They have a loose dependency on one (or more) major versions of other collections included in Ansible. For example, ``ansible.netcommon: >=1.0.0``, or ``ansible.netcommon: >=2.0.0, <3.0.0``. In case a collection depends on releases of a new major version outside of this version range that will be included in the next major Ansible release, the dependent collection will be removed from the next major Ansible release. The cut-off date for this is feature freeze.
  #. They are explicitly being allowed to do so by the Steering Committee.

Examples
--------

#. ``community.foo 1.2.0`` has a dependency on ``community.bar >= 1.0.0, < 1.3.0``.

   * Now ``community.bar`` creates a new release ``1.3.0``. When ``community.foo`` does not create a new release with a relaxed dependency, we have to include ``community.bar 1.2.x`` in the next Ansible release despite ``1.3.0`` being available.
   * If ``community.foo`` does not relax its dependency on ``community.bar`` for some time, ``community.foo`` will be removed from the next Ansible major release.
   * Unfortunately ``community.bar`` has to stay at ``1.2.x`` until either ``community.foo`` is removed (in the next major release), or loosens its requirements so that newer ``community.bar 1.3.z`` releases can be included.

#. ``community.foonetwork`` depends on ``ansible.netcommon >= 2.0.0, <3.0.0``.

   * ``ansible.netcommon 4.0.0`` is released during this major Ansible release cycle.
   * ``community.foonetwork`` either releases a new version before feature freeze of the next major Ansible release that allows depending on all ``ansible.netcommon 4.x.y`` releases, or it will be removed from the next major Ansible release.

Other requirements
===================

* After content is moved out of another currently included collection such as ``community.general`` or ``community.network`` OR a new collection satisfies all the requirements, see `Adding a new collection <https://github.com/ansible-community/ansible-build-data/#adding-a-new-collection>`_ in the `ansible-build-data repository <https://github.com/ansible-community/ansible-build-data/>`_'s README.
* :ref:`The Steering Committee <steering_responsibilities>` can reject a collection inclusion request or exclude a collection from the Ansible package even if the collection satisfies the requirements listed in this document. See the :ref:`Collection inclusion request workflow<steering_inclusion>` for details.

.. seealso::

   :ref:`developing_collections_path`
       A consistent overview of the Ansible collection creator journey
