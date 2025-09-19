.. _ansible_markup:

**************
Ansible markup
**************

Ansible markup allows you to format and structure documentation for Ansible modules, plugins, and roles.
It lets you add basic formatting to text, such as bold, italics, code, and horizontal lines, as well as create various references, such as URLs, hyperlinks, Ansible module references, and RST references.
The Ansible markup language was extended in 2023, starting with ansible-core 2.15. It now lets you apply semantic markup for values, module/plugin options, return values, environment variables, and for referencing plugins.

This page documents the currently supported Ansible markup.

.. _semantic_markup:

Semantic markup within module documentation
-------------------------------------------

Use the semantic markup to highlight option names, option values, and environment variables. The markup processor formats these highlighted terms in a uniform way. With semantic markup, we can modify how the output looks without changing underlying code.

The correct formats for semantic markup are as follows:

* ``O()`` for option names, whether mentioned alone or with values. For example: ``Required if O(state=present).`` and ``Use with O(force) to require secure access.``
* ``V()`` for option values when mentioned alone. For example: ``Possible values include V(monospace) and V(pretty).``
* ``RV()`` for return value names, whether mentioned alone or with values. For example: ``The module returns RV(changed=true) in case of changes.`` and ``Use the RV(stdout) return value for standard output.``
* ``E()`` for environment variables. For example: ``If not set, the environment variable E(ACME_PASSWORD) will be used.``

The parameters for these formatting functions can use escaping with backslashes: ``V(foo(bar="a\\b"\), baz)`` results in the formatted value ``foo(bar="a\b"), baz)``.

.. _option_return_value_link_syntax:

Rules for using O() and RV()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Rules for using ``O()`` and ``RV()`` are very strict. You must follow syntax rules so that documentation renderers can create hyperlinks for the options and return values, respectively.

The allowed syntaxes are as follows:

* To reference an option for the current plugin/module, or the entrypoint of the current role (inside role entrypoint documentation), use ``O(option)`` and ``O(option=value)``.
* To reference an option for another entrypoint ``entrypoint`` from inside role documentation, use ``O(entrypoint:option)`` and ``O(entrypoint:option=name)``. The entrypoint information can be ignored by the documentation renderer, turned into a link to that entrypoint, or even directly to the option of that entrypoint.
* To reference an option for *another* plugin/module ``plugin.fqcn.name`` of type ``type``, use ``O(plugin.fqcn.name#type:option)`` and ``O(plugin.fqcn.name#type:option=value)``. For modules, use ``type=module``. The FQCN and plugin type can be ignored by the documentation renderer, turned into a link to that plugin, or even directly to the option of that plugin.
* To reference an option for entrypoint ``entrypoint`` of *another* role ``role.fqcn.name``, use ``O(role.fqcn.name#role:entrypoint:option)`` and ``O(role.fqcn.name#role:entrypoint:option=value)``. The FQCN and entrypoint information can be ignored by the documentation renderer, turned into a link to that entrypoint, or even directly to the option of that entrypoint.
* To reference options that do not exist (for example, options that were removed in an earlier version), use ``O(ignore:option)`` and ``O(ignore:option=value)``. The ``ignore:`` part will not be shown to the user by documentation rendering.

Option names can refer to suboptions by listing the path to the option separated by dots. For example, if you have an option ``foo`` with suboption ``bar``, then you must use ``O(foo.bar)`` to reference that suboption. You can add array indications like ``O(foo[].bar)`` or even ``O(foo[-1].bar)`` to indicate specific list elements. Everything between ``[`` and ``]`` pairs will be ignored to determine the real name of the option. For example, ``O(foo[foo | length - 1].bar[])`` results in the same link as ``O(foo.bar)``, but the text ``foo[foo | length - 1].bar[]`` displays instead of ``foo.bar``.

The same syntaxes can be used for ``RV()``, except that these will refer to return value names instead of option names; for example ``RV(ansible.builtin.service_facts#module:ansible_facts.services)`` refers to the :ansretval:`ansible.builtin.service_facts#module:ansible_facts.services` fact returned by the :ansplugin:`ansible.builtin.service_facts module <ansible.builtin.service_facts#module>`.

.. _module_documents_linking:

Linking within module documentation
-----------------------------------

You can link from your module documentation to other module docs, other resources on docs.ansible.com, and resources elsewhere on the internet with the help of some pre-defined macros. The correct formats for these macros are:

* ``R()`` for cross-references with a heading (supported since Ansible 2.10). For example: ``See R(Cisco IOS Platform Guide,ios_platform_options)``. Use the RST anchor for the cross-reference. See :ref:`adding_anchors_rst` for details.

  * For links outside of your collection, use ``R()`` if available. Otherwise, use ``U()`` or ``L()`` with full URLs (not relative links).
  * To refer to a group of modules in a collection, use ``R()``. When a collection is not the right granularity, use ``C(..)``, for example:

    - ``Refer to the R(kubernetes.core collection, plugins_in_kubernetes.core) for information on managing kubernetes clusters.``
    - ``The C(win_*) modules (spread across several collections) allow you to manage various aspects of windows hosts.``

* ``L()`` for links with a heading. For example: ``See L(Ansible Automation Platform,https://www.ansible.com/products/automation-platform).`` As of Ansible 2.10, do not use ``L()`` for relative links between Ansible documentation and collection documentation.
* ``U()`` for URLs. For example: ``See U(https://www.ansible.com/products/automation-platform) for an overview.``
* ``M()`` for module names. For example: ``See also M(ansible.builtin.yum) or M(community.general.apt_rpm)``.

  * FQCNs MUST be used, short names will create broken links; use ``ansible.builtin`` for modules in ansible-core.

* ``P()`` for plugin names (supported since ansible-core 2.15). For example: ``See also P(ansible.builtin.file#lookup) or P(community.general.json_query#filter)``.

  * This can also reference roles: ``P(community.sops.install#role)``.
  * FQCNs must be used, short names will create broken links; use ``ansible.builtin`` for plugins in ansible-core.

* ``O()`` and ``RV()`` can also link, see :ref:`the section on their syntax <option_return_value_link_syntax>`.

.. note::

  If you are creating your own documentation site, you will need to use the `intersphinx extension <https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html>`_ to convert ``R()``, ``M()``, ``P()``, ``O()``, and ``RV()`` to the correct links.

Format macros within module documentation
-----------------------------------------

While it is possible to use standard Ansible formatting macros to control the look of other terms in module documentation, you should do so sparingly.

Possible macros include the following:

* ``C()`` for ``monospace`` (code) text. For example: ``This module functions like the unix command C(foo).``
* ``B()`` for bold text.
* ``I()`` for italic text.
* ``HORIZONTALLINE`` for a horizontal rule (the ``<hr>`` html tag) to separate long descriptions.

Note that ``C()``, ``B()``, and ``I()`` do **not allow escaping**, and thus cannot contain the value ``)`` as it always ends the formatting sequence. If you need to use ``)`` inside ``C()``, we recommend to use ``V()`` instead; see the above section on semantic markup.
