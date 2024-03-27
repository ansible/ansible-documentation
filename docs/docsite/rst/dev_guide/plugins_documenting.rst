.. _plugins_documenting:

*******************************
Plugin format and documentation
*******************************

Not all plugins can be documented, but those that can (`documentable <https://github.com/ansible/ansible/blob/devel/lib/ansible/constants.py#L111>`), follow a specific common format, except modules that have their own extended format. Also, some of these plugin types (`configurable <https://github.com/ansible/ansible/blob/devel/lib/ansible/constants.py#L109>`) use the documentation to build their argument validation and type casting, unlike modules that require a separate 'args_spec'.

This document will describe how the plugin configuration works in general, excluding modules, which have their own `documentation reference:developing_modules_documenting`.

.. note:: While most plugins support having the documentation in YAML format inside the same Python code file, filters and tests also support an 'adjacent' YAML file as both of those plugins also support having multiple of them defined in the same file.
 With YAML files, the examples below are easy to use by removing Python quoting and substituting ``=`` for ``:``, for example ``DOCUMENTATION = r''' ... '''` ` to ``DOCUMENTATION: ...`` and removing closing quotes. :ref:`adjacent_yaml_doc`


Every Ansible plugin must be written in Python, with modules being the main exception, also they must begin with several standard sections in a particular order, followed by the code. The sections in order are:

.. contents::
   :depth: 1
   :local:

.. note:: Why don't the imports go first?

  Keen Python programmers may notice that contrary to PEP 8's advice we don't put ``imports`` at the top of the file. This is because the ``DOCUMENTATION`` through ``RETURN`` sections are essentially extra docstrings for the file. The imports are placed after these special variables for the same reason as PEP 8 puts the imports after the introductory comments and docstrings. This keeps the active parts of the code together and the pieces which are purely informational apart. The decision to exclude E402 is based on readability (which is what PEP 8 is about). Documentation strings in a plugin are much more similar to module-level docstrings. Placing the imports below this documentation and closer to the code, consolidates and groups all related code in a congruent manner to improve readability, debugging and understanding.


.. _plugins_shebang_and_encoding:

Python shebang & UTF-8 coding
===============================

Unlike modules, shebangs are not used by plugins since they are imported into Ansible's engine rather than being run as a script.
So your first line will normally be the encoding::

    # -*- coding: utf-8 -*-

.. _plugins_copyright:

Copyright and license
=====================

After the UTF-8 encoding notice, add a `copyright line <https://www.linuxfoundation.org/blog/copyright-notices-in-open-source-software-projects/>`_ with the original copyright holder and a license declaration. The license declaration should be ONLY one line, not the full GPL prefix.::

    # -*- coding: utf-8 -*-

    # Copyright: Contributors to the Ansible project
    # GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

Additions to the module (for example, rewrites) are not permitted to add additional copyright lines other than the default copyright statement if missing::

    # Copyright: Contributors to the Ansible project

Any legal review will include the source control history, so an exhaustive copyright header is not necessary.
Please do not include a copyright year. If the existing copyright statement includes a year, do not edit the existing copyright year. Any existing copyright header should not be modified without permission from the copyright author.

.. _plugins_documentation_block:

DOCUMENTATION block
===================

The next section is the ``DOCUMENTATION`` block. Ansible's plugin documentation is generated from the ``DOCUMENTATION`` blocks, both for the online site and the ``ansible-doc`` output. The ``DOCUMENTATION`` block must be valid YAML. You may find it easier to start writing your ``DOCUMENTATION`` string in an :ref:`editor with YAML syntax highlighting <other_tools_and_programs>` before you include it in your Python file.

Plugin documentation should briefly and accurately define what each plugin is meant to accomplish and what and each option does. Documentation should be written for a broad audience--readable both by experts and non-experts.
    * Descriptions should always start with a capital letter and end with a full stop. Consistency always helps.

To create clear, concise, consistent, and useful documentation, follow the :ref:`style guide <style_guide>`.

Each documentation field is described below. Before committing your plugin documentation, please test it at the command line and as HTML:

* You can use ``ansible-doc -t <plugin_type> <plugin_name>`` to view your documentation at the command line. Any parsing errors will be obvious - you can view details by adding ``-vvv`` to the command.
* You should also :ref:`test the HTML output <testing_plugin_documentation>` of your plugin documentation.


Documentation fields
--------------------

All fields in the ``DOCUMENTATION`` block are lower-case. All fields are required unless specified otherwise:

:name:

  * The name of the plugin.
  * For most plugins, it must be the same as the file name, without the ``.py`` extension.
  * For filters and tests it must match the name used to invoke them in a template.

:short_description:

  * The ``short_description`` is displayed by ``ansible-doc -l`` without any category grouping,
    so it needs enough detail to explain the module's purpose without the context of the directory structure in which it lives.
  * Unlike ``description:``, ``short_description`` should not have a trailing period/full stop.

:description:

  * A detailed description (generally two or more sentences).
  * Must be written in full sentences, in other words, with capital letters and periods/full stops.
  * Should not mention the plugin name.
  * Make use of multiple entries rather than using one long paragraph.
  * Do not quote complete values unless it is required by YAML.

:version_added:

  * The version of the collection when the plugin was added. In the case of adding to Ansible core, that version is used instead.
  * This is a string, and not a float, for example, ``version_added: '2.1.0'``.

:author:

  * Name of the author in the form ``First Last (@GitHubID)``.
  * Use a multi-line list if there is more than one author.
  * Do not use quotes as it should not be required by YAML.

:deprecated:

  * Marks the plugin for removal in future releases. See also :ref:`module_lifecycle`.

:options:

  * Options are often called `parameters` or `arguments`. Because the documentation field is called `options`, we will use that term.
  * If the plugin has no options, all you need is one line: ``options: {}``.
  * If your plugin has options (in other words, accepts arguments), each option should be documented thoroughly. For each option, include:

  :option-name:

    * Declarative operation (not CRUD), to focus on the final state, for example `online:`, rather than `is_online:`.
    * The name of the option should be consistent with the rest of the plugin, as well as other plugins in the same category.
    * When in doubt, look for other plugins to find option names that are used for the same purpose, we like to offer consistency to our users.

  :description:

    * Detailed explanation of what this option does. It should be written in full sentences.
    * The first entry is a description of the option itself; subsequent entries detail its use, dependencies, or format of possible values.
    * Should not list the possible values (that's what ``choices:`` is for, though it should explain what the values do if they aren't obvious).
    * If an option is only sometimes required, describe the conditions. For example, "Required when I(state=present)."
    * Mutually exclusive options must be documented as the final sentence on each of the options.

  :required:

    * Only needed if ``true``.
    * If missing, we assume the option is not required.

  :default:

    * If ``required`` is false/missing, ``default`` may be specified (assumed 'null' if missing).
    * Ensure that the default value in the docs matches the default value in the code.
    * The default field must not be listed as part of the description, unless it requires additional information or conditions.
    * If the option is a boolean value, you can use any of the boolean values recognized by Ansible
      (such as ``true``/``false`` or ``yes``/``no``).  Document booleans as ``true``/``false`` for consistency and compatibility with ansible-lint.

  :choices:

    * List of option values.
    * Should be absent if empty.

  :type:

    * Specifies the data type that option accepts, must match the ``argspec``.
    * If an argument is ``type='bool'``, this field should be set to ``type: bool`` and no ``choices`` should be specified.
    * If an argument is ``type='list'``, ``elements`` should be specified.

  :elements:

    * Specifies the data type for list elements in case ``type='list'``.

  :version_added:

    * Only needed if this option was extended after initial release of the plugin, in other words, this is greater than the top level `version_added` field.
    * This is a string, and not a float, for example, ``version_added: '2.3.0'``.

:requirements:

  * List of requirements, this should include any Python non core libraries/imports and command line utilities (if applicable).
  * Include minimum versions, maximum also if the requirement has made backward incompatible changes.

:seealso:

  * A list of references to other plugins, documentation or Internet resources
  * In Ansible 2.10 and later, references to plugins or modules must use the FQCN or ``ansible.builtin`` for plugins in ``ansible-core``.
  * Plugin references are supported since ansible-core 2.15.
  * A reference can be one of the following formats:


    .. code-block:: yaml+jinja

        seealso:

        # Reference by module name
        - module: cisco.aci.aci_tenant

        # Reference by module name, including description
        - module: cisco.aci.aci_tenant
          description: ACI module to create tenants on a Cisco ACI fabric.

        # Reference by plugin name
        - plugin: ansible.builtin.file
          plugin_type: lookup

        # Reference by plugin name, including description
        - plugin: ansible.builtin.file
          plugin_type: lookup
          description: You can use the ansible.builtin.file lookup to read files on the control node.

        # Reference by rST documentation anchor
        - ref: aci_guide
          description: Detailed information on how to manage your ACI infrastructure using Ansible.

        # Reference by rST documentation anchor (with custom title)
        - ref: The official Ansible ACI guide <aci_guide>
          description: Detailed information on how to manage your ACI infrastructure using Ansible.

        # Reference by Internet resource
        - name: APIC Management Information Model reference
          description: Complete reference of the APIC object model.
          link: https://developer.cisco.com/docs/apic-mim-ref/


  * If you use ``ref:`` to link to an anchor that is not associated with a title, you must add a title to the ref for the link to work correctly.


:notes:

  * Details of any important information that doesn't fit in one of the above sections.

.. _plugins_documents_linking:

.. include:: document_linking.rst

.. _plugins_semantic_markup:

.. include:: semantic_markup.rst

.. _plugins_docs_fragments:

Documentation fragments
-----------------------

If you are writing multiple related plugins, they may share common documentation, such as authentication details, file mode settings, ``notes:`` or ``seealso:`` entries. Rather than duplicate that information in each plugin's ``DOCUMENTATION`` block, you can save it once as a doc_fragment plugin and use it in each plugin's documentation. In Ansible, shared documentation fragments are contained in a ``ModuleDocFragment`` class in `lib/ansible/plugins/doc_fragments/ <https://github.com/ansible/ansible/tree/devel/lib/ansible/plugins/doc_fragments>`_ or the equivalent directory in a collection. To include a documentation fragment, add ``extends_documentation_fragment: FRAGMENT_NAME`` in your plugin documentation. Use the fully qualified collection name for the FRAGMENT_NAME (for example, ``kubernetes.core.k8s_auth_options``).

Plugins should only use items from a doc fragment if the plugin will implement all of the interface documented there in a manner that behaves the same as the existing plugin which import that fragment. The goal is that items imported from the doc fragment will behave identically when used in another plugin that imports the doc fragment.

By default, only the ``DOCUMENTATION`` property from a doc fragment is inserted into the plugin documentation. It is possible to define additional properties in the doc fragment in order to import only certain parts of a doc fragment or mix and match as appropriate. If a property is defined in both the doc fragment and the plugin, the plugin value overrides the doc fragment.

Here is an example doc fragment named ``example_fragment.py``:

.. code-block:: python

    class ModuleDocFragment(object):
        # Standard documentation
        DOCUMENTATION = r'''
        options:
          # options here
        '''

        # Additional section
        OTHER = r'''
        options:
          # other options here
        '''


To insert the contents of ``OTHER`` in a plugin:

.. code-block:: yaml+jinja

    extends_documentation_fragment: example_fragment.other

Or use both :

.. code-block:: yaml+jinja

    extends_documentation_fragment:
      - example_fragment
      - example_fragment.other

.. _note:
  * Prior to Ansible 2.8, documentation fragments were kept in ``lib/ansible/utils/module_docs_fragments``.

.. versionadded:: 2.8

Since Ansible 2.8, you can have user-supplied doc_fragments by using a ``doc_fragments`` directory adjacent to play or role, just like any other plugin.

For example, all AWS modules should include:

.. code-block:: yaml+jinja

    extends_documentation_fragment:
    - aws
    - ec2

:ref:`docfragments_collections` describes how to incorporate documentation fragments in a collection.

.. _plugins_examples_block:

EXAMPLES block
==============

After the shebang, the UTF-8 coding, the copyright line, the license section, and the ``DOCUMENTATION`` block comes the ``EXAMPLES`` block. Here you show users how your plugin works with real-world examples in multi-line plain-text or YAML format. The best examples are ready for the user to copy and paste into a playbook. Review and update your examples with every change to your plugin.

Use a fully qualified collection name (FQCN) as a part of the plugin's name. For plugins in ``ansible-core``, use the ``ansible.builtin.`` identifier, for example ``ansible.builtin.pipe``.

If your examples use boolean options, favor yes/no values, this is not always possible as some plugins will force using Python or Jinja2 specific booleans.

.. _plugins_return_block:

RETURN block
============

After the shebang, the UTF-8 coding, the copyright line, the license section, ``DOCUMENTATION`` and ``EXAMPLES`` blocks comes the ``RETURN`` block. This section documents the information the plugin returns for use by other plugins.

If your plugin doesn't return anything, this section should read: ``RETURN = r''' # '''``
Otherwise, for each value returned, provide the following fields. All fields are required unless specified otherwise.

:return name:
  Name of the returned field.

  :description:
    Detailed description of what this value represents. Capitalized and with trailing dot.
  :type:
    Data type.
  :elements:
    If ``type='list'``, specifies the data type of the list's elements.
  :sample:
    One or more examples.
  :version_added:
    Only needed if this return was extended after initial plugin release, in other words, this is greater than the top level `version_added` field.
    This is a string, and not a float, for example, ``version_added: '2.3.0'``.
  :contains:
    Optional. To describe nested return values, set ``type: dict``, or ``type: list``/``elements: dict``, or if you really have to, ``type: complex``, and repeat the elements above for each sub-field.

Here are two example ``RETURN`` sections, one with three simple fields and one with a complex nested field:

.. code-block:: text

    # lookkup plugin
    RETURN = r'''
    _list:
        description: List of destination file/path(s).
        type: str
        sample: /path/to/file.txt
    '''

    # test plugin
    RETURN = r'''
    _result:
        description: If input matched test or not
        type: bool
    '''

.. _plugins_python_imports:

Python imports
==============

Now can finally add the python imports. Normally we order them in sections: python core, ansible libraries, other 3rd party libraries, then within each section we sort them alphabetically.

.. code-block:: python

   from os import path

   from ansilbe.utils.path import unfrackpath

   import requests

.. _dev_testing_plugin_documentation:

Testing plugin documentation
============================

To test Ansible documentation locally please :ref:`follow instruction<testing_plugin_documentation>`. To test documentation in collections, please see :ref:`build_collection_docsite`.
