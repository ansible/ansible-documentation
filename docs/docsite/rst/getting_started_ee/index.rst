.. _getting_started_ee_index:

*******************************************
Getting started with Execution Environments
*******************************************

You can run Ansible automation in containers, like any other modern software application.
Ansible uses container images known as Execution Environments (EE) that act as control nodes.
EEs remove complexity to scale out automation projects and make things like deployment operations much more straightforward.

An Execution Environment image contains the following packages as standard:

* ``ansible-core``
* ``ansible-runner``
* Python
* Ansible content dependencies

In addition to the standard packages, an EE can also contain:

* one or more Ansible collections and their dependencies
* other custom components

This getting started guide shows you how to build and test a simple Execution Environment.
The resulting container image represents an Ansible control node that contains:

* standard EE packages
* ``community.postgresql`` collection
* ``psycopg2-binary`` Python package

.. toctree::
   :maxdepth: 1

   introduction
   setup_environment
   build_execution_environment
   run_execution_environment
   run_community_ee_image
