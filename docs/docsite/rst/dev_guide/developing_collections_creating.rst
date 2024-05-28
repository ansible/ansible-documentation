.. _creating_collections:

********************
Creating collections
********************

To create a collection:

#. Create a :ref:`collection skeleton<creating_collections_skeleton>` with the ``ansible-galaxy collection init`` command.
#. Add modules and other content to the collection.
#. Build the collection into a collection artifact with :ref:`ansible-galaxy collection build<building_collections>`.
#. Publish the collection artifact to Galaxy with :ref:`ansible-galaxy collection publish<publishing_collections>`.

A user can then install your collection on their systems.

.. contents::
   :local:
   :depth: 2

Naming your collection
======================

Collection names consist of a namespace and a name, separated by a period (``.``). Both namespace and name should be valid Python identifiers. This means that they should consist of ASCII letters, digits, and underscores.

.. note::

    Usually namespaces and names use lower-case letters, digits, and underscores, but no upper-case letters.

You should make sure that the namespace you use is not registered by someone else by checking on `Ansible Galaxy's namespace list <https://galaxy.ansible.com/ui/namespaces/>`_. If you chose a namespace or even a full collection name that collides with another collection on Galaxy, it can happen that if you or someone else runs ``ansible-galaxy collection install`` with your collection name, you end up with another collection. Even if the namespace currently does not exist, it could be created later by someone else.

If you want to request a new namespace on Ansible Galaxy, `create an issue on github.com/ansible/galaxy <https://github.com/ansible/galaxy/issues/new?assignees=thedoubl3j%2C+alisonlhart%2C+chynasan%2C+traytorous&labels=area%2Fnamespace&projects=&template=New_namespace.md&title=namespace%3A+FIXME>`_.

There are a few special namespaces:

:ansible:

  The `ansible namespace <https://galaxy.ansible.com/ui/namespaces/ansible/>`_ is owned by Red Hat and reserved for official Ansible collections. Two special members are the synthetic ``ansible.builtin`` and ``ansible.legacy`` collections. These cannot be found on Ansible Galaxy, but are built-in into ansible-core.

:community:

  The `community namespace <https://galaxy.ansible.com/ui/namespaces/community/>`_ is owned by the Ansible community. Collections from this namespace generally live in the `GitHub ansible-collection organization <https://github.com/ansible-collections/>`_. If you want to create a collection in this namespace, :ref:`request<request_coll_repo>` it on the forum.

:local:

  The `local namespace <https://galaxy.ansible.com/ui/namespaces/local/>`_ does not contain any collection on Ansible Galaxy, and the intention is that this will never change. You can use the ``local`` namespace for collections that are locally on your machine or locally in your git repositories, without having to fear collisions with actually existing collections on Ansible Galaxy.

.. _creating_collections_skeleton:

Creating a collection skeleton
==============================

Create your collection skeleton in a path that includes ``ansible_collections``, for example `collections/ansible_collections/`.


To start a new collection, run the following command in your collections directory:

.. code-block:: bash

    ansible_collections#> ansible-galaxy collection init my_namespace.my_collection

.. note::

	Both the namespace and collection names use the same strict set of requirements. See `Galaxy namespaces <https://galaxy.ansible.com/docs/contributing/namespaces.html#galaxy-namespaces>`_ on the Galaxy docsite for those requirements.

It will create the structure ``[my_namespace]/[my_collection]/[collection skeleton]``.

.. hint:: If Git is used for version control, the corresponding repository should be initialized in the collection directory.

Once the skeleton exists, you can populate the directories with the content you want inside the collection. See `ansible-collections <https://github.com/ansible-collections/>`_ GitHub Org to get a better idea of what you can place inside a collection.

Reference: the ``ansible-galaxy collection`` command

Currently the ``ansible-galaxy collection`` command implements the following sub commands:

* ``init``: Create a basic collection skeleton based on the default template included with Ansible or your own template.
* ``build``: Create a collection artifact that can be uploaded to Galaxy or your own repository.
* ``publish``: Publish a built collection artifact to Galaxy.
* ``install``: Install one or more collections.

To learn more about the ``ansible-galaxy`` command-line tool, see the :ref:`ansible-galaxy` man page.

.. _creating_collection_with_ansible-creator:

Creating collections with ansible-creator
=========================================

`ansible-creator <https://ansible.readthedocs.io/projects/creator/>`_ is designed to quickly scaffold an Ansible collection project.

.. note::

   The `Ansible Development Tools <https://ansible.readthedocs.io/projects/dev-tools/>`_ package offers a convenient way to install ``ansible-creator`` along with a curated set of tools for developing automation content.

After `installing <https://ansible.readthedocs.io/projects/creator/installing/#installation>`_ ``ansible-creator`` you can initialize a project in one of the following ways:

* Use the `init <https://ansible.readthedocs.io/projects/creator/installing/#initialize-ansible-collection-init-subcommand>`_ subcommand.
* Use ``ansible-creator`` with the `Ansible extension <https://ansible.readthedocs.io/projects/creator/collection_creation/#step-1-installing-ansible-creator-in-the-environment>`_ in Visual Studio Code.

.. seealso::

   :ref:`collections`
       Learn how to install and use collections.
   :ref:`collection_structure`
       Directories and files included in the collection skeleton
   `Ansible Development Tools (ADT) <https://ansible.readthedocs.io/projects/dev-tools/>`_
       Python package of tools to create and test Ansible content.
   `Mailing List <https://groups.google.com/group/ansible-devel>`_
       The development mailing list
   :ref:`communication_irc`
       How to join Ansible chat channels
