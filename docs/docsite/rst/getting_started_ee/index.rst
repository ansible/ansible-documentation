.. _getting_started_ee_index:

###########################################
Getting started with Execution Environments
###########################################

.. note::

  Do you have any questions or ideas on how to improve this document?
  Please share them with us by creating an issue in the `GitHub repository <https://github.com/ansible/ansible-documentation/issues>`_.

You can run Ansible automation in containers, like any other modern software application.
Ansible uses container images known as execution environments (EE) that act as control nodes.

An execution environment (EE) image contains the following packages as standard:

* ``ansible-core``
* ``ansible-runner``
* Python and required dependencies

In addition to the standard packages, an EE can also contain one or more Ansible collections and any other custom components.

This getting started guide shows you how to build and test a simple execution environment.
The resulting container image represents an Ansible control node that contains the standard EE packages plus the ``community.postgresql`` collection and the ``psycopg2-binary`` Python package.

.. toctree::
   :maxdepth: 1

   introduction
   setup_environment
   build_execution_environment
   run_execution_environment