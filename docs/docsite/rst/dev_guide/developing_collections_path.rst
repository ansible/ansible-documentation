.. _developing_collections_path:

*******************************
Ansible collection creator path
*******************************

.. note::

  If you are unfamiliar with Ansible collections, first take a look at the :ref:`Using Ansible collections guide<collections>`.

Ansible collections are a distribution format for Ansible content that can include playbooks, roles, modules, and plugins.
A typical collection addresses a set of related use cases. For example, the ``community.dns`` collection includes modules and plugins to work with DNS.

You can install collections made by others or share yours with the community through a distribution server such as `Ansible Galaxy <https://galaxy.ansible.com/ui/>`_. Certified collections can be published to the Red Hat Automation Hub, a part of the Red Hat Ansible Automation Platform.

Creating and sharing collections is a great way of contributing to the Ansible project.

The Ansible community package consists of ``ansible-core``, which, among other core components, includes the ``ansible.builtin`` collection maintained by the Core team, and a set of collections maintained by the community.

The purpose of this guide is to give you as a (potential) content creator a consistent overview of the Ansible collection creator journey from an idea for the first module/role to having your collection included in the Ansible community package. The :ref:`Collection development guidelines section<developing_collections>` provides references to more detailed aspects of this journey.
The overall journey consists of the following milestones:

.. contents::
   :local:

.. _examine_existing_content:

Examine currently available solutions
=====================================

If you have an idea for a new role or module/plugin, there is no need to reinvent the wheel if there is already a sufficient solution that solves your automation issue.

Therefore, first examine the currently available content including:

* :ref:`Ansible builtin modules and plugins <plugins_in_ansible.builtin>`
* :ref:`Ansible package collection index<all_modules_and_plugins>`
* `Ansible Galaxy <https://galaxy.ansible.com/ui/>`_
* `Ansible Automation Hub <https://www.ansible.com/products/automation-hub>`_ if you have the Ansible Automation Platform subscription

In case the solutions you found are not fully sufficient or have flaws, consider improving them rather than creating your own. Each collection includes information on where to create issues for that collection to propose your enhancement ideas.

If you already have your content written and used in your workflows, you can still consider integrating it to the existing solutions.
However, if these options do not apply to your collection ideas, we encourage you to create and share your own.

.. _create_content:

Create your content
===================

You :ref:`tried <examine_existing_content>` but have not found any sufficient solution for your automation issue.

Use one of the following guides:

* :ref:`Roles guide<playbooks_reuse_roles>`: if you want to create a role.
* :ref:`Developer guide<developer_guide>`: if you want to create a new Ansible module or plugin for your personal use.

Put your content in a collection
================================

You :ref:`created <create_content>` new content.

Now it is time to create a reusable and sharable collection.
Use the :ref:`Developing collections guide<developing_collections>` to learn how.

We recommend you to use the `collection_template repository <https://github.com/ansible-collections/collection_template>`_ as a basis for your collection.

Write good user collection documentation
========================================

Your collection ``README.md`` file should contain a quick-start installation and usage guides.
You can use the `community.general collection README file <https://github.com/ansible-collections/community.general/blob/main/README.md>`_ as an example.

If your collection contains modules or plugins, make sure their documentation is comprehensive.
Use the :ref:`Module format and documentation guide<developing_modules_documenting>` and :ref:`Ansible documentation style guide<style_guide>` to learn more.

Publish your collection source code
===================================

Publish your collection on a platform for software development and version control such as `GitHub <https://github.com/>`_.

It can be your personal repository or your organization's one.
You can also :ref:`request<request_coll_repo>` a repository under the `ansible-collections <https://github.com/ansible-collections/>`_ organization.

Make sure your collection contains exhaustive license information.
Ansible is an open source project, so we encourage you to license it under one of open source licenses.
If you plan to submit your collection for inclusion in the Ansible community package, your collection must satisfy the :ref:`licensing requirements<coll_licensing_req>`.

If you have used the `collection_template repository <https://github.com/ansible-collections/collection_template>`_ we recommended earlier as a skeleton for your collection, it already contains the ``GNU GPL v3`` license.

Follow a versioning convention
==============================

When releasing new versions of your collections, take the following recommended practices into consideration:

* Follow a versioning convention. Using `SemVer <https://semver.org/>`_ is highly recommended.
* Base your releases on `Git tags <https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases>`_.

Understand and implement testing and CI
=======================================

This section is applicable to collections containing modules and plugins.

For role testing, see the `Ansible Molecule <https://ansible.readthedocs.io/projects/molecule/>`_ project.

Add tests
---------

Testing your collection ensures that your code works well and integrates with other components such as ``ansible-core``.

Take a look at the following documents:

* :ref:`Testing Ansible guide<developing_testing>`: provides general information about testing.
* :ref:`Testing collections guide<testing_collections>`: contains collection-specific testing information.

Implement continuous integration
--------------------------------

Now make sure when pull requests are created in your collection repository they are automatically tested using a CI tool such as GitHub Actions or Azure Pipelines.

The `collection_template repository <https://github.com/ansible-collections/collection_template>`_ contains GitHub Actions `templates <https://github.com/ansible-collections/collection_template/tree/main/.github/workflows>`_ you can adjust and use to enable the workflows in your repository.

Provide good contributor & maintainer documentation
===================================================

See the `collection_template/README.md <https://github.com/ansible-collections/collection_template/blob/main/README.md>`_ as an example.

Publish your collection on distribution servers
===============================================

To distribute your collection and allow others to conveniently use it, publish your collection on one or more distribution servers.
See the :ref:`Distributing collections guide<distributing_collections>` to learn how.

Make your collection a part of Ansible community package
========================================================

Make you collection satisfy the :ref:`Ansible community package collections requirements<collections_requirements>` and submit it for inclusion.
See the `inclusion process description <https://github.com/ansible-collections/ansible-inclusion/blob/main/README.md>`_ to learn how.

Maintain
========

Maintain your collection.
See the :ref:`Ansible collection maintainer guidelines<maintainers>` for details.

Communicate
===========

Engage with the community.
Take a look at the :ref:`Ansible communication guide<communication>` to see available communication options.

.. seealso::

   :ref:`developing_collections`
       A set of guidelines about collection development aspects
