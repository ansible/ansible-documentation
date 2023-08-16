import
======

Ansible :ref:`allows unchecked imports<allowed_unchecked_imports>` of some libraries from specific directories.
Importing any other Python library requires :ref:`handling import errors<handling_import_errors>`.
This enables support for sanity tests such as :ref:`testing_validate-modules` and provides better error messages to the user.

.. important::

   Please see the :ref:`frequently asked questions<frequently_asked_questions>` for answers to common questions about resolving errors reported by this test.

.. _handling_import_errors:

Handling import errors
----------------------

Ansible executes across many hosts and can use multiple Python interpreters at the same time, which may even have different versions.
To ensure users get an actionable and easy to understand error we try to ensure any non-core imports in modules/plugins are guarded to avoid a traceback,
which most users won't be able to understand, much less use to solve the issue.

Another reason Ansible does this is to import the code for inspection. This allows Ansible to easily test, document, configure, etc based on the code without having to install
any and all requirements everywhere, especially when that is not the context in which you execute the code.

The code below shows examples of how to avoid errors on import and then use the provided ``missing_required_lib`` to ensure the user knows which LIBRARY is missing,
on which HOST it is missing and the specific INTERPRETER that requires it.


In modules
^^^^^^^^^^

Instead of using ``import another_library``:

.. code-block:: python

   import traceback

   from ansible.module_utils.basic import missing_required_lib

   try:
       import another_library
   except ImportError:
       HAS_ANOTHER_LIBRARY = False
       ANOTHER_LIBRARY_IMPORT_ERROR = traceback.format_exc()
   else:
       HAS_ANOTHER_LIBRARY = True
       ANOTHER_LIBRARY_IMPORT_ERROR = None

.. note::

   The ``missing_required_lib`` import above will be used below.

Then in the module code, normally inside the ``main`` method:

.. code-block:: python

   module = AnsibleModule(...)

   if not HAS_ANOTHER_LIBRARY:
       module.fail_json(
           msg=missing_required_lib('another_library'),
           exception=ANOTHER_LIBRARY_IMPORT_ERROR)

In plugins
^^^^^^^^^^

Instead of using ``import another_library``:

.. code-block:: python

   try:
       import another_library
   except ImportError as imp_exc:
       ANOTHER_LIBRARY_IMPORT_ERROR = imp_exc
   else:
       ANOTHER_LIBRARY_IMPORT_ERROR = None

Then in the plugin code, for example in the ``run`` method of the plugin (some plugins don't have a ``run`` method and will require it in the ``__init__`` method instead):

.. code-block:: python

   if ANOTHER_LIBRARY_IMPORT_ERROR:
       raise AnsibleError('another_library must be installed to use this plugin') from ANOTHER_LIBRARY_IMPORT_ERROR

When used as base classes
^^^^^^^^^^^^^^^^^^^^^^^^^

.. important::

   This solution builds on the previous two examples.
   Make sure to pick the appropriate one before continuing with this solution.

Sometimes an import is used in a base class, for example:

.. code-block:: python

   from another_library import UsefulThing

   class CustomThing(UsefulThing):
       pass

One option is make the entire class definition conditional:

.. code-block:: python

   if not ANOTHER_LIBRARY_IMPORT_ERROR:
       class CustomThing(UsefulThing):
           pass

Another option is to define a substitute base class by modifying the exception handler:

.. code-block:: python

   try:
       from another_library import UsefulThing
   except ImportError:
       class UsefulThing:
           pass
       ...

.. _allowed_unchecked_imports:

Allowed unchecked imports
-------------------------

Ansible allows the following unchecked imports from these specific directories:

* ansible-core:

  * For ``lib/ansible/modules/`` and ``lib/ansible/module_utils/``, unchecked imports are only allowed from the Python standard library;
  * For ``lib/ansible/plugins/``, unchecked imports are only allowed from the Python standard library, from public dependencies of ansible-core, and from ansible-core itself;

* collections:

  * For ``plugins/modules/`` and ``plugins/module_utils/``, unchecked imports are only allowed from the Python standard library;
  * For other directories in ``plugins/`` (see `the community collection requirements <https://github.com/ansible-collections/overview/blob/main/collection_requirements.rst#modules-plugins>`_ for a list), unchecked imports are only allowed from the Python standard library, from public dependencies of ansible-core, and from ansible-core itself.

Public dependencies of ansible-core are:

  * Jinja2
  * PyYAML
  * MarkupSafe (as a dependency of Jinja2)

.. _frequently_asked_questions:

Frequently asked questions (FAQ)
--------------------------------

Why do I get an ``ImportError`` when my module or plugin works?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``import`` sanity test is very different from other tests.
By design, it can only see modules that are in the Python standard library.
This means your module or plugin can work in your playbooks, integration tests and unit tests, while failing the ``import`` sanity test.

All occurrences of ``ImportError`` must be :ref:`properly handled<handling_import_errors>` in the module or plugin where it occurs.

Why isn't the test using the Python interpreter I specify?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The sanity test will use the Python interpreter you specify.
However, it will create its own virtual environment using that Python interpreter.

All occurrences of ``ImportError`` must be :ref:`properly handled<handling_import_errors>` in the module or plugin where it occurs.

How do I use a custom virtual environment?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is not possible, since doing so would defeat the purpose of the test.

All occurrences of ``ImportError`` must be :ref:`properly handled<handling_import_errors>` in the module or plugin where it occurs.

How do I specify where to find my imports?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is not possible, since doing so would defeat the purpose of the test.

All occurrences of ``ImportError`` must be :ref:`properly handled<handling_import_errors>` in the module or plugin where it occurs.

How do I specify which requirements file to use?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is not possible, since doing so would defeat the purpose of the test.

All occurrences of ``ImportError`` must be :ref:`properly handled<handling_import_errors>` in the module or plugin where it occurs.

How do I fix the ``ImportError`` without changing my code?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is no way to fix an ``ImportError`` in your plugins or modules without making changes to them.

All occurrences of ``ImportError`` must be :ref:`properly handled<handling_import_errors>` in the module or plugin where it occurs.
