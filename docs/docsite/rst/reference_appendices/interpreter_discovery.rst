.. _interpreter_discovery:

Interpreter Discovery
=====================

Note: the behavior of this option changed in ansible-core 2.17. Consult the
previous documentation if you are using ansible-core < 2.17.

Most Ansible modules that execute under a POSIX environment require a Python
interpreter on the target host. Unless configured otherwise, Ansible will
attempt to discover a suitable Python interpreter on each target host the first
time a Python module is executed for that host.

To control the discovery behavior:

* for individual hosts and groups, use the ``ansible_python_interpreter`` inventory variable
* globally, use the ``interpreter_python`` key in the ``[defaults]`` section of ``ansible.cfg``

Use one of the following values:

auto (default) :
  Searches a list of common Python interpreter paths and uses the first one
  found. Also issues a warning that future installation of another Python
  interpreter could alter the one chosen.

auto_legacy : 
  Deprecated alias for ``auto``.

auto_silent :
  Same as ``auto``, but does not issue warnings.

auto_legacy_silent :
  Deprecated alias for ``auto_silent``.

``/path/to/python`` :
  Use the specified path to Python.
