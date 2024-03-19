Linking within plugin documentation
-----------------------------------

You can link from your plugin or module documentation to other plugin/module, other resources on docs.ansible.com, and resources elsewhere on the internet with the help of some pre-defined macros. The correct formats for these macros are:

* ``L()`` for links with a heading. For example: ``See L(Ansible Automation Platform,https://www.ansible.com/products/automation-platform).`` As of Ansible 2.10, do not use ``L()`` for relative links between Ansible documentation and collection documentation.
* ``U()`` for URLs. For example: ``See U(https://www.ansible.com/products/automation-platform) for an overview.``
* ``R()`` for cross-references with a heading (added in Ansible 2.10). For example: ``See R(Cisco IOS Platform Guide,ios_platform_options)``.  Use the RST anchor for the cross-reference. See :ref:`adding_anchors_rst` for details.
* ``M()`` for module names. For example: ``See also M(ansible.builtin.yum) or M(community.general.apt_rpm)``. A FQCN **must** be used, short names will create broken links; use ``ansible.builtin`` for modules in ansible-core.
* ``P()`` for plugin names. For example: ``See also P(ansible.builtin.file#lookup) or P(community.general.json_query#filter)``. This can also reference roles: ``P(community.sops.install#role)``. This is supported since ansible-core 2.15. FQCNs must be used; use ``ansible.builtin`` for plugins in ansible-core.

.. note::

  For links between pluigins and documentation within a collection, you can use any of the options above. For links outside of your collection, use ``R()`` if available. Otherwise, use ``U()`` or ``L()`` with full URLs (not relative links). For modules, use ``M()`` with the FQCN or ``ansible.builtin`` as shown in the example. If you are creating your own documentation site, you will need to use the `intersphinx extension <https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html>`_ to convert ``R()`` and ``M()`` to the correct links.

.. note::
  To refer to a group of modules in a collection, use ``R()``.  When a collection is not the right granularity, use ``C(..)``:

    - ``Refer to the R(kubernetes.core collection, plugins_in_kubernetes.core) for information on managing kubernetes clusters.``
    - ``The C(win_*) modules (spread across several collections) allow you to manage various aspects of windows hosts.``

.. note::

   Because it stands out better, use ``seealso`` for general references over the use of notes or adding links to the description.

