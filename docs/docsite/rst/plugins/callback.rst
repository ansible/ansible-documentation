.. _callback_plugins:

Callback plugins
================

.. contents::
   :local:
   :depth: 2

Callback plugins enable adding new behaviors to Ansible when responding to events. By default, callback plugins control most of the output you see when running the command line programs, but can also be used to add additional output, integrate with other tools and marshal the events to a storage backend. If necessary, you can :ref:`create custom callback plugins <developing_callbacks>`.

.. _callback_examples:

Example callback plugins
------------------------

The :ref:`log_plays <log_plays_callback>` callback is an example of how to record playbook events to a log file, and the :ref:`mail <mail_callback>` callback sends email on playbook failures.

The :ref:`say <say_callback>` callback responds with computer synthesized speech in relation to playbook events.

.. _enabling_callbacks:

Enabling callback plugins
-------------------------

You can activate a custom callback by either dropping it into a ``callback_plugins`` directory adjacent to your play, inside a role, or by putting it in one of the callback directory sources configured in :ref:`ansible.cfg <ansible_configuration_settings>`.

Plugins are loaded in alphanumeric order. For example, a plugin implemented in a file named `1_first.py` would run before a plugin file named `2_second.py`.

Most callbacks shipped with Ansible are disabled by default and need to be enabled in your :ref:`ansible.cfg <ansible_configuration_settings>` file in order to function. For example:

.. code-block:: ini

  #callbacks_enabled = timer, mail, profile_roles, collection_namespace.collection_name.custom_callback

Setting a callback plugin for ``ansible-playbook``
--------------------------------------------------

You can only have one plugin be the main manager of your console output. If you want to replace the default, you should define ``CALLBACK_TYPE = stdout`` in the subclass and then configure the stdout plugin in :ref:`ansible.cfg <ansible_configuration_settings>`. For example:

.. code-block:: ini

  stdout_callback = dense

or for my custom callback:

.. code-block:: ini

  stdout_callback = mycallback

This only affects :ref:`ansible-playbook` by default.

Setting a callback plugin for ad hoc commands
---------------------------------------------

The :ref:`ansible` ad hoc command specifically uses a different callback plugin for stdout, so there is an extra setting in :ref:`ansible_configuration_settings` you need to add to use the stdout callback defined above:

.. code-block:: ini

    [defaults]
    bin_ansible_callbacks=True

You can also set this as an environment variable:

.. code-block:: shell

    export ANSIBLE_LOAD_CALLBACK_PLUGINS=1


.. _callback_plugin_types:

Types of callback plugins
-------------------------

There are three types of callback plugins:

:stdout callback plugins:

  These plugins handle the main console output. Only one of these can be active.

:aggregate callback plugins:

  Aggregate callbacks can add additional console output next to a stdout callback. This can be aggregate information at the end of a playbook run, additional per-task output, or anything else.

:notification callback plugins:

  Notification callbacks inform other applications, services, or systems. This can be anything from logging to databases, informing on errors in Instant Messaging applications, or sending emails when a server is unreachable.

.. _callback_plugin_list:

Plugin list
-----------

You can use ``ansible-doc -t callback -l`` to see the list of available plugins.
Use ``ansible-doc -t callback <plugin name>`` to see specific documents and examples.

.. seealso::

   :ref:`action_plugins`
       Action plugins
   :ref:`cache_plugins`
       Cache plugins
   :ref:`connection_plugins`
       Connection plugins
   :ref:`inventory_plugins`
       Inventory plugins
   :ref:`shell_plugins`
       Shell plugins
   :ref:`strategy_plugins`
       Strategy plugins
   :ref:`vars_plugins`
       Vars plugins
   `User Mailing List <https://groups.google.com/forum/#!forum/ansible-devel>`_
       Have a question?  Stop by the Google group!
   :ref:`communication_irc`
       How to join Ansible chat channels
