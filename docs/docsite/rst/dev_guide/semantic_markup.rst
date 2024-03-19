Semantic markup within plugin documentation
-------------------------------------------

You can use semantic markup to highlight option names, option values, and environment variables. The markup processor formats these highlighted terms in a uniform way. With semantic markup, we can modify how the output looks without changing underlying code.

The correct formats for semantic markup are as follows:

* ``O()`` for option names, whether mentioned alone or with values. For example: ``Required if O(state=present).`` and ``Use with O(force) to require secure access.``
* ``V()`` for option values when mentioned alone. For example: ``Possible values include V(monospace) and V(pretty).``
* ``RV()`` for return value names, whether mentioned alone or with values. For example: ``The plugin returns RV(changed=true) in case of changes.`` and ``Use the RV(stdout) return value for standard output.``
* ``E()`` for environment variables. For example: ``If not set, the environment variable E(ACME_PASSWORD) will be used.``

The parameters for these formatting functions can use escaping with backslashes: ``V(foo(bar="a\\b"\), baz)`` results in the formatted value ``foo(bar="a\b"), baz)``.

Rules for using ``O()`` and ``RV()`` are very strict. You must follow syntax rules so that documentation renderer can create hyperlinks for the options and return values, respectively.

The allowed syntax are as follows:
- To reference an option for the current plugin/module, or the entry point of the current role (inside role entry point documentation), use ``O(option)`` and ``O(option=name)``.
- To reference an option for another entry point ``entrypoint`` from inside role documentation, use ``O(entrypoint:option)`` and ``O(entrypoint:option=name)``. The entry point information can be ignored by the documentation renderer, turned into a link to that entry point, or even directly to the option of that entry point.
- To reference an option for *another* plugin/module ``plugin.fqcn.name`` of type ``type``, use ``O(plugin.fqcn.name#type:option)`` and ``O(plugin.fqcn.name#type:option=name)``. For modules, use ``type=module``. The FQCN and plugin type can be ignored by the documentation renderer, turned into a link to that plugin, or even directly to the option of that plugin.
- To reference an option for entry point ``entrypoint`` of *another* role ``role.fqcn.name``, use ``O(role.fqcn.name#role:entrypoint:option)`` and ``O(role.fqcn.name#role:entrypoint:option=name)``. The FQCN and entry point information can be ignored by the documentation renderer, turned into a link to that entry point, or even directly to the option of that entry point.
- To reference options that do not exist (for example, options that were removed in an earlier version), use ``O(ignore:option)`` and ``O(ignore:option=name)``. The ``ignore:`` part will not be shown to the user by documentation rendering.

Format macros within module documentation
-----------------------------------------

While it is possible to use standard Ansible formatting macros to control the look of other terms in plugin documentation, you should do so sparingly.

Possible macros include the following:

* ``C()`` for ``monospace`` (code) text. For example: ``This plugin functions like the unix command C(foo).``
* ``B()`` for bold text.
* ``I()`` for italic text.
* ``HORIZONTALLINE`` for a horizontal rule (the ``<hr>`` HTML tag) to separate long descriptions.

Note that ``C()``, ``B()``, and ``I()`` do **not allow escaping**, and thus cannot contain the value ``)`` as it always ends the formatting sequence. If you need to use ``)`` inside ``C()``, we recommend to use ``V()`` instead; see the above section on semantic markup.

