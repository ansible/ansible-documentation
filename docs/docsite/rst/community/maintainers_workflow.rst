.. _maintainers_workflow:

Backporting and Ansible inclusion
==================================

Each collection community defines its own rules and workflows for managing pull requests (PRs), bug reports, documentation issues, feature requests, and maintainer changes. Maintainers review and merge PRs according to the following guidelines:

* :ref:`code_of_conduct`
* :ref:`maintainer_requirements`
* :ref:`Committer guidelines <committer_general_rules>`
* :ref:`PR review checklist<review_checklist>`

Collections can have two types of maintainers: :ref:`collection_maintainers` and :ref:`module_maintainers`.

.. _collection_maintainers:

Collection maintainers
----------------------

Collection-scope maintainers have ``write`` or higher access to a collection. They have commit rights, allowing them to merge pull requests and perform other administrative tasks.

If a collection maintainer determines a contribution is significant (e.g., a complex bug fix, new feature, or consistent reviews), they can invite the author to become a module maintainer.

.. _module_maintainers:

Module maintainers
------------------

Module-scope maintainers are present in collections that use the `collection bot <https://github.com/ansible-community/collection_bot>`_, such as `community.general <https://github.com/ansible-collections/community.general>`_ and `community.network <https://github.com/ansible-collections/community.network>`_.

Module maintainers are typically a precursor to becoming a collection maintainer. They are listed in ``.github/BOTMETA.yml`` and maintain a specific scope, such as a file, module, plugin, directory, or repository. Although their scope can vary, they are primarily referred to as module maintainers because their responsibilities often center on modules or groups of modules. The collection bot notifies module maintainers of relevant issues and PRs.

Module maintainers have indirect commit rights through the `collection bot <https://github.com/ansible-community/collection_bot>`_. When two module maintainers comment with ``shipit``, ``LGTM``, or ``+1`` on a pull request for a module they maintain, the collection bot automatically merges the PR.

For more information about the collection bot and its interface, see the `Collection bot overview <https://github.com/ansible-community/collection_bot/blob/main/ISSUE_HELP.md>`_.

Releasing a collection
----------------------

Collection maintainers are responsible for releasing new collection versions. The general release process includes:

#.  **Planning and announcement**: Define the release scope and communicate it.
#.  **Changelog generation**: Create a comprehensive list of changes.
#.  **Git tagging and pushing**: Create and push a release Git tag.
#.  **Automated publication**: The release tarball is automatically published on `Ansible Galaxy <https://galaxy.ansible.com/>`_ via the `Zuul dashboard <https://dashboard.zuul.ansible.com/t/ansible/builds?pipeline=release>`_.
#.  **Final announcement**: Communicate the successful release.
#.  **Optional inclusion request**: Consider `filing a request to include the collection in the Ansible package <https://github.com/ansible-collections/ansible-inclusion>`_.

For detailed information, see :ref:`releasing_collections`.

.. _Backporting:

Backporting
------------

Collection maintainers backport merged pull requests to stable branches. This process adheres to the collection's `semantic versioning <https://semver.org/>`_ and release policies.

The manual backporting process mirrors the :ref:`ansible-core backporting guidelines <backport_process>`.

For streamlined backporting, GitHub bots like the `Patchback app <https://github.com/apps/patchback>`_ can automate the process through labeling, as implemented in `community.general <https://github.com/ansible-collections/community.general>`_ and `community.network <https://github.com/ansible-collections/community.network>`_.

.. _including_collection_ansible:

Including a collection in Ansible
-----------------------------------

To include a collection in the Ansible package, maintainers can create a discussion in the `ansible-collections/ansible-inclusion repository <https://github.com/ansible-collections/ansible-inclusion>`_. For more details, refer to the `repository's README <https://github.com/ansible-collections/ansible-inclusion/blob/main/README.md>`_ and the :ref:`Ansible community package collections requirements <collections_requirements>`.

Stepping down as a collection maintainer
===========================================

If you can no longer continue as a collection maintainer, follow these steps:

* **Inform other maintainers**: Notify your co-maintainers.
* **Notify the community**: For collections under the ``ansible-collections`` organization, inform the relevant :ref:`communication_irc` channels (IRC or Matrix ``community`` chat channels), or email ``ansible-community@redhat.com``.
* **Identify potential replacements**: Look for active contributors within the collection who could become new maintainers. Discuss these candidates with other maintainers or the community team.
* **Announce the need for maintainers (if no replacement is found)**: If you cannot find a replacement, create a pinned issue in the collection repository announcing the need for new maintainers.
* **Post in the Bullhorn newsletter**: Make the same announcement through the `Bullhorn newsletter <https://forum.ansible.com/t/about-the-newsletter-category/166>`_.
* **Engage in candidate discussions**: Be available to discuss potential candidates identified by other maintainers or the community team.

Remember, this is a community, and you are welcome to rejoin at any time.
