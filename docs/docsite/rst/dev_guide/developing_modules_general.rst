.. _developing_modules_general:
.. _module_dev_tutorial_sample:

******************
Developing modules
******************

A module is a reusable, standalone script that Ansible runs on your behalf, either locally or remotely. Modules interact with your local machine, an API, or a remote system to perform specific tasks like changing a database password or spinning up a cloud instance. Each module can be used by the Ansible API, or by the :command:`ansible` or :command:`ansible-playbook` programs. A module provides a defined interface, accepts arguments, and returns information to Ansible by printing a JSON string to stdout before exiting.

If you need functionality that is not available in any of the thousands of Ansible modules found in collections, you can easily write your own custom module. When you write a module for local use, you can choose any programming language and follow your own rules. Use this topic to learn how to create an Ansible module in Python. After you create a module, you must add it locally to the appropriate directory so that Ansible can find and execute it. For details about adding a module locally, see :ref:`developing_locally`.

If you are developing a module in a :ref:`collection <developing_collections>`,  see those documents instead.

.. contents::
   :local:

.. _environment_setup:

Preparing an environment for developing Ansible modules
=======================================================

You just need ``ansible-core`` installed to test the module. Modules can be written in any language,
but most of the following guide is assuming you are using Python.
Modules for inclusion in Ansible itself must be Python or Powershell.

One advantage of using Python or Powershell for your custom modules is being able to use the ``module_utils`` common code that does a lot of the
heavy lifting for argument processing, logging and response writing, among other things.

Creating a standalone module
============================

It is highly recommended that you use a ``venv`` or ``virtualenv`` for Python development.

To create a standalone module:

1. Create a ``library`` directory in your workspace. Your test play should live in the same directory.
2. Create your new module file: ``$ touch library/my_test.py``. Or just open/create it with your editor of choice.
3. Paste the content below into your new module file. It includes the :ref:`required Ansible format and documentation <developing_modules_documenting>`, a simple :ref:`argument spec for declaring the module options <argument_spec>`, and some example code.
4. Modify and extend the code to do what you want your new module to do. See the :ref:`programming tips <developing_modules_best_practices>` and :ref:`Python 3 compatibility <developing_python_3>` pages for pointers on writing clean and concise module code.

Creating a module in a collection
=================================

To create a new module in an existing collection called ``my_namespace.my_collection``:

1. Create your new module file: ``$ touch <PATH_TO_COLLECTION>/ansible_collections/my_namespace/my_collection/plugins/modules/my_test.py``. Or just create it with your editor of choice.
2. Paste the content below into your new module file. It includes the :ref:`required Ansible format and documentation <developing_modules_documenting>`, a simple :ref:`argument spec for declaring the module options <argument_spec>`, and some example code.
3. Modify and extend the code to do what you want your new module to do. See the :ref:`programming tips <developing_modules_best_practices>` and :ref:`Python 3 compatibility <developing_python_3>` pages for pointers on writing clean and concise module code.

.. literalinclude:: ../../../../examples/scripts/my_test.py
   :language: python

Creating an info or a facts module
==================================

Ansible gathers information about the target machines using facts modules, and gathers information on other objects or files using info modules.
If you find yourself trying to add ``state: info`` or ``state: list`` to an existing module, that is often a sign that a new dedicated ``_facts`` or ``_info`` module is needed.

In Ansible 2.8 and onwards, we have two type of information modules, they are ``*_info`` and ``*_facts``.

If a module is named ``<something>_facts``, it should be because its main purpose is returning ``ansible_facts``. Do not name modules that do not do this with ``_facts``.
Only use ``ansible_facts`` for information that is specific to the host machine, for example network interfaces and their configuration, which operating system and which programs are installed.

Modules that query/return general information (and not ``ansible_facts``) should be named ``_info``.
General information is non-host specific information, for example information on online/cloud services (you can access different accounts for the same online service from the same host), or information on VMs and containers accessible from the machine, or information on individual files or programs.

Info and facts modules, are just like any other Ansible Module, with a few minor requirements:

1. They MUST be named ``<something>_info`` or ``<something>_facts``, where <something> is singular.
2. Info ``*_info`` modules MUST return in the form of the :ref:`result dictionary<common_return_values>` so other modules can access them.
3. Fact ``*_facts`` modules MUST return in the ``ansible_facts`` field of the :ref:`result dictionary<common_return_values>` so other modules can access them.
4. They MUST support :ref:`check_mode <check_mode_dry>`.
5. They MUST NOT make any changes to the system.
6. They MUST document the :ref:`return fields<return_block>` and :ref:`examples<examples_block>`.

You can add your facts into ``ansible_facts`` field of the result as follows:

.. code-block:: python

    module.exit_json(changed=False, ansible_facts=dict(my_new_fact=value_of_fact))

The rest is just like creating a normal module.

Verifying your module code
==========================

After you modify the sample code above to do what you want, you can try out your module.
Our :ref:`debugging tips <debugging_modules>` will help if you run into bugs as you verify your module code.


Verifying your module code locally
----------------------------------

The simplest way is to use ``ansible`` adhoc command:

.. code:: shell

    ANSIBLE_LIBRARY=./library ansible -m my_test -a 'name=hello new=true' remotehost

If your module does not need to target a remote host, you can quickly and easily exercise your code locally like this:

.. code:: shell

    ANSIBLE_LIBRARY=./library ansible -m my_test -a 'name=hello new=true' localhost

For a module developed in an existing collection called ``my_namespace.my_collection`` (as mentioned above):

.. code:: shell

    $ ansible localhost -m my_namespace.my_collection.my_test -a 'name=hello new=true' --playbook-dir=$PWD

-  If you use ``pdb``, ``print()``, or some other method of local debugging for faster iteration,
   you can avoid going through Ansible by creating an arguments file, which is
   a basic JSON config file that passes parameters to your module so that you can run it.
   Name the arguments file ``/tmp/args.json`` and add the following content:

.. code:: json

    {
        "ANSIBLE_MODULE_ARGS": {
            "name": "hello",
            "new": true
        }
    }

-  Then the module can be tested locally and directly. This skips the packing steps and uses module_utils files directly:

.. code:: console

   $ python library/my_test.py /tmp/args.json

You might also need to add your collection's path to the Python path. This tells Python to look for additional module_utils code in the given path.
You can run the module code, as in the following example:

.. code:: shell

   $ export PYTHONPATH=PATH_TO_COLLECTIONS:$PYTHONPATH
   $ python -m ansible_collections.my_namespace.my_collection.plugins.modules.my_test /tmp/args.json


It should return output like this:

.. code:: json

    {"changed": true, "state": {"original_message": "hello", "new_message": "goodbye"}, "invocation": {"module_args": {"name": "hello", "new": true}}}



Verifying your module code in a playbook
----------------------------------------

You can easily run a full test by including it in a playbook, as long as the ``library`` directory is in the same directory as the play:

-  Create a playbook in any directory: ``$ touch testmod.yml``
-  Add the following to the new playbook file:

.. code-block:: yaml

    - name: test my new module
      hosts: localhost
      tasks:
      - name: run the new module
        my_test:
          name: 'hello'
          new: true
        register: testout
      - name: dump test output
        debug:
          msg: '{{ testout }}'

- Run the playbook and analyze the output: ``$ ansible-playbook ./testmod.yml``

Testing your newly-created module
=================================

Review our :ref:`testing <developing_testing>` section for more detailed
information, including instructions for :ref:`testing module documentation <testing_module_documentation>`, adding :ref:`integration tests <testing_integration>`, and more.

.. note::
  If contributing to Ansible, every new module and plugin should have integration tests, even if the tests cannot be run on Ansible CI infrastructure.
  In this case, the tests should be marked with the ``unsupported`` alias in `aliases file <https://docs.ansible.com/ansible/latest/dev_guide/testing/sanity/integration-aliases.html>`_.


Contributing back to Ansible
============================

If you would like to contribute to ``ansible-core`` by adding a new feature or fixing a bug, `create a fork <https://help.github.com/articles/fork-a-repo/>`_ of the ansible/ansible repository and develop against a new feature branch using the ``devel`` branch as a starting point. When you have a good working code change, you can submit a pull request to the Ansible repository by selecting your feature branch as a source and the Ansible devel branch as a target.

If you want to contribute a module to an :ref:`Ansible collection <contributing_maintained_collections>`, review our :ref:`submission checklist <developing_modules_checklist>`, :ref:`programming tips <developing_modules_best_practices>`, and :ref:`strategy for maintaining Python 2 and Python 3 compatibility <developing_python_3>`, as well as information about :ref:`testing <developing_testing>` before you open a pull request.

The :ref:`Community Guide <ansible_community_guide>` covers how to open a pull request and what happens next.


Communication and development support
=====================================

Visit the :ref:`Ansible communication guide<communication>` for information on how to join the conversation.

Credit
======

Thank you to Thomas Stringer (`@trstringer <https://github.com/trstringer>`_) for contributing source
material for this topic.
