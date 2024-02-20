:orphan:

.. _testing_module_documentation:
.. _testing_plugin_documentation:

****************************
Testing plugin documentation
****************************

A quick test while developing is to use ``ansible-doc -t <plugin_type> <name>`` to see if it renders, you might need to add ``-M /path/to/module`` if the module is not somewhere Ansible expects to find it.

Before you submit a plugin for inclusion in ansible-core, you must run tests to ensure that the argspec matches the documentation in your Python file, and that the argspec's and documentation's structure is correct.

The community pages offer more information on :ref:`testing reStructuredText documentation <testing_documentation_locally>` if you extend the Ansible documentation with additional RST files.

To ensure that your module documentation matches your ``argument_spec``:

#. Install required Python packages (drop '--user' in venv/virtualenv):

   .. code-block:: bash

      pip install --user -r test/lib/ansible_test/_data/requirements/sanity.txt

#. run the ``validate-modules`` test:

   .. code-block:: bash

    ansible-test sanity --test validate-modules mymodule

If you have Docker or Podman installed, you can also use them with the ``--docker`` option, which uses an image that already has all requirements installed:

.. code-block:: bash

    ansible-test sanity --docker --test validate-modules mymodule

For other plugin types the steps are similar, just adjusting names and paths to the specific type.
