***************************
Developing ``ansible-core``
***************************

Although ``ansible-core`` (the code hosted in the `ansible/ansible repository <https://github.com/ansible/ansible>`_ on GitHub) includes a few plugins that can be swapped out by the playbook directives or configuration, much of the code there is not modular.  The documents here give insight into how the parts of ``ansible-core`` work together.

.. toctree::
   :maxdepth: 1

   core_branches_and_tags
   developing_program_flow_modules

.. seealso::

   :ref:`developing_api`
       Learn about the Python API for task execution
   :ref:`developing_plugins`
       Learn about developing plugins
   :ref:`Communication<communication>`
       Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide
