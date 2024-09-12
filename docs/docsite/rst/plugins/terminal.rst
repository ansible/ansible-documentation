.. _terminal_plugins:

Terminal plugins
================

.. contents::
   :local:
   :depth: 2

Terminal plugins contain information on how to ensure that a particular network device's SSH shell is properly initialized to be used with Ansible. This typically includes disabling automatic paging, detecting errors in output, and enabling privileged mode if the device supports and requires it.

These plugins correspond one-to-one to network device platforms. Ansible loads the appropriate terminal plugin automatically based on the ``ansible_network_os`` variable.

.. _enabling_terminal:

Adding terminal plugins
-------------------------

You can extend Ansible to support other network devices by dropping a custom plugin into the ``terminal_plugins`` directory.

.. _using_terminal:

Using terminal plugins
------------------------

Ansible determines which terminal plugin to use automatically from the ``ansible_network_os`` variable. There should be no reason to override this functionality.

Terminal plugins operate without configuration. All options to control the terminal are exposed in the ``network_cli`` connection plugin.

Plugins are self-documenting. Each plugin should document its configuration options.


.. seealso::

   :ref:`Ansible for Network Automation<network_guide>`
       An overview of using Ansible to automate networking devices.
   :ref:`connection_plugins`
       Connection plugins
   :ref:`Communication<communication>`
       Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide
