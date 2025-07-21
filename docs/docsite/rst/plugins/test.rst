.. _test_plugins:

Test plugins
=============

.. contents::
   :local:
   :depth: 2

Test plugins evaluate template expressions and return True or False. With test plugins you can create :ref:`conditionals <playbooks_conditionals>` to implement the logic of your tasks, blocks, plays, playbooks, and roles. Ansible uses the `standard tests <https://jinja.palletsprojects.com/en/latest/templates/#builtin-tests>`_ shipped as part of Jinja and adds some specialized test plugins. You can :ref:`create custom Ansible test plugins <developing_test_plugins>`.


.. _enabling_test:

Enabling test plugins
----------------------

You can add a custom test plugin by dropping it into a ``test_plugins`` directory adjacent to your play, inside a role, or by putting it in one of the test plugin directory sources configured in :ref:`ansible.cfg <ansible_configuration_settings>`.


.. _using_test:

Using test plugins
-------------------

You can use tests anywhere you can use templating in Ansible: in a play, in a variables file, or in a Jinja2 template for the :ref:`template <template_module>` module. For more information on using test plugins, see :ref:`playbooks_tests`.

Tests always return ``True`` or ``False``, they are always a boolean, if you need a different return type, you should be looking at filters.

You can recognize test plugins by the use of the ``is`` statement in a template, they can also be used as part of the ``select`` family of filters.

.. code-block:: yaml+jinja

  vars:
    is_ready: '{{ task_result is success }}'

  tasks:
  - name: conditionals are always in 'template' context
    action: dostuff
    when: task_result is failed

Tests will always have an ``_input`` and this is normally what is on the left side of ``is``. Tests can also take additional parameters as you would to most programming functions. These parameters can be either ``positional`` (passed in order) or ``named`` (passed as key=value pairs). When passing both types, positional arguments should go first.

.. code-block:: yaml+jinja

  tasks:
  - name: pass a positional parameter to match test
    action: dostuff
    when: myurl is match("https://example.com/users/.*/resources")

  - name: pass named parameter to truthy test
    action: dostuff
    when: myvariable is truthy(convert_bool=True)

  - name: pass both types to 'version' test
    action: dostuff
    when: sample_semver_var is version('2.0.0-rc.1+build.123', 'lt', version_type='semver')


Using test plugins with lists
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As mentioned above, one way to use tests is with the ``select`` family of filters (``select``, ``reject``, ``selectattr``, ``rejectattr``).

.. code-block:: yaml+jinja

   # give me only defined variables from a list of variables, using 'defined' test
   good_vars: "{{ all_vars|select('defined') }}"

   # this uses the 'equalto' test to filter out non 'fixed' type of addresses from a list
   only_fixed_addresses:  "{{ all_addresses|selectattr('type', 'equalto', 'fixed') }}"

   # this does the opposite of the previous one
   only_fixed_addresses:  "{{ all_addresses|rejectattr('type', 'equalto', 'fixed') }}"


Plugin list
-----------

You can use ``ansible-doc -t test -l`` to see the list of available plugins. Use ``ansible-doc -t test <plugin name>`` to see plugin-specific documentation and examples.


.. seealso::

   :ref:`about_playbooks`
       An introduction to playbooks
   :ref:`playbooks_tests`
       Using tests
   :ref:`playbooks_conditionals`
       Using conditional statements
   :ref:`filter_plugins`
       Filter plugins
   :ref:`playbooks_tests`
       Using tests
   :ref:`lookup_plugins`
       Lookup plugins
   :ref:`Communication<communication>`
       Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide
