.. _maintainers_workflow:

Ansible Collection Maintenance and Workflow
===========================================

Each collection community can set its own rules and workflows for managing pull requests (PRs), bug reports, documentation issues, feature requests, as well as for adding and replacing maintainers.

Collection maintainers have ``write`` or higher access to a collection, allowing them to merge pull requests and perform other administrative tasks.

Managing pull requests
----------------------

Maintainers review and merge PRs according to the following guidelines:

* :ref:`code_of_conduct`
* :ref:`maintainer_requirements`
* :ref:`Committer guidelines <committer_general_rules>`
* :ref:`PR review checklist<review_checklist>`

Releasing a collection
----------------------

Collection maintainers are responsible for releasing new collection versions. The general release process includes:

#.  **Planning and announcement**: Define the release scope and communicate it.
#.  **Changelog generation**: Create a comprehensive list of changes.
#.  **Git tagging**: Create and push a release Git tag.
#.  **Automated publication**: The release tarball is automatically published on `Ansible Galaxy <https://galaxy.ansible.com/>`_ via the `Zuul dashboard <https://dashboard.zuul.ansible.com/t/ansible/builds?pipeline=release>`_ or a custom GitHub Actions workflow.
#.  **Final announcement**: Communicate the successful release.

See :ref:`releasing_collections` for more information.

.. _Backporting:

Backporting
------------

Collection maintainers backport merged pull requests to stable branches if they exist. This process adheres to the collection's `semantic versioning <https://semver.org/>`_ and release policies.

The manual backporting process mirrors the :ref:`ansible-core backporting guidelines <backport_process>`.

For streamlined backporting, GitHub bots like the `Patchback app <https://github.com/apps/patchback>`_ can automate the process through labeling, as implemented in the `community.general <https://github.com/ansible-collections/community.general>`_ collection.

.. _including_collection_ansible:

Including a collection in Ansible
-----------------------------------

To include a collection in the Ansible community package, maintainers create a discussion in the `ansible-collections/ansible-inclusion repository <https://github.com/ansible-collections/ansible-inclusion>`_. See the `submission process <https://github.com/ansible-collections/ansible-inclusion/blob/main/README.md>`_ and the :ref:`Ansible community package collections requirements <collections_requirements>` for details.

Stepping down as a collection maintainer
===========================================

If you can no longer continue as a collection maintainer, follow these steps:

* **Inform other maintainers**: Notify your co-maintainers.
* **Notify the community**: For collections under the ``ansible-collections`` GitHub organization, inform the relevant :ref:`communication_irc` channels, or email ``ansible-community@redhat.com``.
* **Identify potential replacements**: Look for active contributors within the collection who could become new maintainers. Discuss these candidates with other maintainers or the `Ansible community team <https://forum.ansible.com/g/CommunityEngTeam>`_.
* **Announce the need for maintainers (if no replacement is found)**: If you cannot find a replacement, create a pinned issue in the collection repository announcing the need for new maintainers.
* **Post in the Bullhorn newsletter**: Make the same announcement through the `Bullhorn newsletter <https://forum.ansible.com/t/about-the-newsletter-category/166>`_.
* **Engage in candidate discussions**: Be available to discuss potential candidates identified by other maintainers or the community team.

Remember, this is a community and you are welcome to rejoin at any time.
