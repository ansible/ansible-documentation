.. _modules_support:

******************************
Module maintenance and support
******************************

If you are using a module and you discover a bug, you may want to know where to report that bug, who is responsible for fixing it, and how you can track changes to the module. If you are a Red Hat subscriber, you may want to know whether you can get support for the issue you are facing.

Starting in Ansible 2.10, most modules live in collections. The distribution method for each collection reflects the maintenance and support for the modules in that collection.

.. contents::
  :local:

Maintenance
===========

.. table::
   :class: documentation-table

   ============================= ========================================== ==========================
   Collection                    Code location                              Maintained by
   ============================= ========================================== ==========================
   ansible.builtin               `ansible/ansible repo`_ on GitHub          core team

   distributed on Galaxy         various; follow ``repo`` link              community or partners

   distributed on Automation Hub various; follow ``repo`` link              content team or partners
   ============================= ========================================== ==========================

.. _ansible/ansible repo: https://github.com/ansible/ansible/tree/devel/lib/ansible/modules

Issue Reporting
===============

If you find a bug that affects a plugin in the main Ansible repo, also known as ``ansible-core``:

  #. Confirm that you are running the latest stable version of Ansible or the devel branch.
  #. Look at the `issue tracker in the Ansible repo <https://github.com/ansible/ansible/issues>`_ to see if an issue has already been filed.
  #. Create an issue if one does not already exist. Include as much detail as you can about the behavior you discovered.

If you find a bug that affects a plugin in a Galaxy collection:

  #. Find the collection on Galaxy.
  #. Find the issue tracker for the collection.
  #. Look there to see if an issue has already been filed.
  #. Create an issue if one does not already exist. Include as much detail as you can about the behavior you discovered.

Some partner collections may be hosted in private repositories.

If you are not sure whether the behavior you see is a bug, if you have questions, if you want to discuss development-oriented topics, or if you just want to get in touch, visit the :ref:`Ansible communication guide<communication>` for information on how to join the community.

If you find a bug that affects a module in an Automation Hub collection:

  #. If the collection offers an Issue Tracker link on Automation Hub, click there and open an issue on the collection repository. If it does not, follow the standard process for reporting issues on the `Red Hat Customer Portal <https://access.redhat.com/>`_. You must have a subscription to the Red Hat Ansible Automation Platform to create an issue on the portal.

Support
=======

All plugins that remain in ``ansible-core`` and all collections hosted in Automation Hub are supported by Red Hat. No other plugins or collections are supported by Red Hat. If you have a subscription to the Red Hat Ansible Automation Platform, you can find more information and resources on the `Red Hat Customer Portal. <https://access.redhat.com/>`_

.. seealso::

   :ref:`intro_adhoc`
       Examples of using modules in /usr/bin/ansible
   :ref:`working_with_playbooks`
       Examples of using modules with /usr/bin/ansible-playbook
   :ref:`Communication<communication>`
       Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide
