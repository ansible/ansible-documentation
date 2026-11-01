.. _interpreter_discovery:

Interpreter Discovery
=====================

Most Ansible modules that execute under a POSIX environment require a Python
interpreter on the target host. Unless configured otherwise, Ansible will
attempt to discover a suitable Python interpreter on each target host
the first time a Python module is executed for that host.

To control the discovery behavior:

* for individual hosts and groups, use the ``ansible_python_interpreter`` inventory variable
* globally, use the ``interpreter_python`` key in the ``[defaults]`` section of ``ansible.cfg``

Configure a path to a specific Python interpreter, or one of the following values:

auto (default) :
  Searches the configurable list of common Python interpreter paths
  (see :ref:`INTERPRETER_PYTHON_FALLBACK`) and issues a warning that
  future installation of another Python interpreter could alter the one chosen.

auto_silent :
  Same as ``auto``, but does not issue warnings.

The ``auto_legacy`` and ``auto_legacy_silent`` values were removed in ansible-core 2.21.
Use ``auto`` or ``auto_silent`` instead.

