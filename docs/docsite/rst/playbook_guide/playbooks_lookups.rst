.. _playbooks_lookups:

*******
Lookups
*******

Lookup plugins retrieve data from outside sources such as files, databases, key/value stores, APIs, and other services. Like all templating, lookups execute and are evaluated on the Ansible control machine. Ansible makes the data returned by a lookup plugin available using the standard templating system. Before Ansible 2.5, lookups were mostly used indirectly in ``with_<lookup>`` constructs for looping. Starting with Ansible 2.5, lookups are used more explicitly as part of Jinja2 expressions fed into the ``loop`` keyword.

.. _lookups_and_variables:

The lookup function
===================

You can use the ``lookup`` function to populate variables dynamically. Ansible evaluates the value each time it is executed in a task (or template).

.. code-block:: yaml+jinja

    vars:
      motd_value: "{{ lookup('file', '/etc/motd') }}"
    tasks:
      - debug:
          msg: "motd value is {{ motd_value }}"

The first argument to the ``lookup`` function is required and specifies the name of the lookup plugin. If the lookup plugin is in a collection, the fully qualified name must be provided, since the :ref:`collections keyword<collections_keyword>` does not apply to lookup plugins.

The ``lookup`` function also accepts an optional boolean keyword ``wantlist``, which defaults to ``False``. When ``True``, the result of the lookup is ensured to be a list.

Refer to the lookup plugin's documentation to see plugin-specific arguments and keywords.

.. _lookups_and_variables_query:

The query/q function
====================

This function is shorthand for ``lookup(..., wantlist=True)``. These are equivalent:

.. code-block:: yaml+jinja

   block:
     - debug:
         msg: "{{ item }}"
       loop: "{{ lookup('ns.col.lookup_items', wantlist=True) }}"

     - debug:
         msg: "{{ item }}"
       loop: "{{ q('ns.col.lookup_items') }}"

For more details and a list of lookup plugins in ansible-core, see :ref:`plugins_lookup`. You may also find lookup plugins in collections. You can review a list of lookup plugins installed on your control machine with the command ``ansible-doc -l -t lookup``.

.. seealso::

   :ref:`working_with_playbooks`
       An introduction to playbooks
   :ref:`playbooks_conditionals`
       Conditional statements in playbooks
   :ref:`playbooks_variables`
       All about variables
   :ref:`playbooks_loops`
       Looping in playbooks
   :ref:`Communication<communication>`
       Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide
