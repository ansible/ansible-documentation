.. _templating_undef:

The undef function: add hint for undefined variables
====================================================

.. versionadded:: 2.12

The Jinja2 ``undef()`` function returns a Python ``AnsibleUndefined`` object, derived from ``jinja2.StrictUndefined``. Use ``undef()`` to undefine variables of :ref:`lesser precedence <ansible_variable_precedence>`.

For example, ``roles:`` defaults/vars are scoped to the play and a role could avoid inheriting another role's default by using ``undef()``.

.. code-block:: yaml

    roles:
      - role_a
      - role_b

.. code-block:: yaml

    # roles/role_a/defaults/main.yml
    role_default: role_a

    # roles/role_b/defaults/main.yml
    role_default: "{{ undef(hint='If this is required and missing, this error will be displayed. This must be defined with higher precedence than role defaults.') }}"

.. seealso:: :ref:`DEFAULT_PRIVATE_ROLE_VARS` is a general way to do this for M(ansible.builtin.include_role)/M(ansible.builtin.import_role).

The ``undef`` function accepts 1 optional argument:

hint
    Give a custom hint about the undefined variable if :ref:`DEFAULT_UNDEFINED_VAR_BEHAVIOR` is configured to give an error.
