.. _yaml_syntax:


YAML Syntax
===========

This page provides a basic overview of correct YAML syntax, which is how Ansible
playbooks (our configuration management language) are expressed.

We use YAML because it is easier for humans to read and write than other common
data formats like XML or JSON.  Further, there are libraries available in most
programming languages for working with YAML.

You may also wish to read :ref:`working_with_playbooks` at the same time to see how this
is used in practice.


YAML Basics
-----------

All YAML files (regardless of their association with Ansible) can optionally begin with ``---`` and end with ``...``. 
This is part of the YAML format and indicates the start and end of a document.

One of the most common structures that can be found in a yaml file is a list.
Each item of a list starts with a ``"- "`` (a dash and a space) and must be at the same indentation level:

.. note:: Indentation is the amount of whitespace from the start of a line. Correct indentation is important for YAML documents to be valid.

.. code:: yaml

    ---
    # A list of tasty fruits
    - Apple
    - Orange
    - Strawberry
    - Mango
    ...

Another common structure is a dictionary which consists of one or more key/value pairs: ``key: value`` (the colon must be followed by a space):

.. code:: yaml

    # An employee record
    martin:
      name: Martin D'vloper
      job: Developer
      skill: Elite

Dictionaries and lists can be combined into more complex data structures. As an example, below is a lists of dictionaries:

.. code:: yaml

    # Employee records
    - martin:
        name: Martin D'vloper
        job: Developer
        skills:
          - python
          - perl
          - pascal
    - tabitha:
        name: Tabitha Bitumen
        job: Developer
        skills:
          - lisp
          - fortran
          - erlang

Dictionaries and lists can also be written in a short form called "Flow collections":

.. code:: yaml

    ---
    martin: {name: Martin D'vloper, job: Developer, skill: Elite}
    fruits: ['Apple', 'Orange', 'Strawberry', 'Mango']


.. _truthiness:

If a value corresponding to a key is a :ref:`boolean value <playbooks_variables>` (true/false) it can be written in several forms:

.. code:: yaml

    create_key: true
    needs_agent: false
    knows_oop: True
    likes_emacs: TRUE
    uses_cvs: false

Use lowercase 'true' or 'false' to be compatible with default yamllint options.

Values can be written as multiple string values using "Block Scalars".

"Folded Block Scalar" ``>`` will replace carriage returns at the end of each line with spaces. Carriage returns can be added by leaving an empty line.
For example the following:

.. code:: yaml

    fold_newlines: >
                this is really a
                single line of text
                despite appearances

                this is going to be a
                second line of text

will result in two lines of text followed by one newline:

.. code:: text

    this is really a single line of text despite appearances\n
    this is going to be a second line of text\n

"Literal Block Scalar" ``|`` will keep carriage returns and any trailing spaces (again, followed by one newline):

.. code:: yaml

    include_newlines: |
                exactly as you see
                will appear these three
                lines of poetry

                and one more line

becomes

.. code:: text

    exactly as you see\n
    will appear these three\n
    lines of poetry\n
    \n
    and one more line\n

To avoid a new line at the end add ``-`` after block scalar. For example:

.. code:: yaml

    include_newlines: |-
                exactly as you see
                will appear these three
                lines of poetry

                and one more line

becomes

.. code:: text

    exactly as you see\n
    will appear these three\n
    lines of poetry\n
    \n
    and one more line

Note that in all examples above the indentation and the amount of new lines at the end were ignored.
To keep all additional new lines at the end use ``+`` after block scalar. For example:

.. code:: yaml

    include_newlines: |+
                exactly as you see
                will appear these three
                lines of poetry
                \n
                and one more line
                \n
                \n

becomes

.. code:: text

    exactly as you see\n
    will appear these three\n
    lines of poetry\n
    \n
    and one more line\n
    \n
    \n

An example below combines what we learned so far and gives a feel of the format:

.. code:: yaml

    ---
    # An employee record
    name: Martin D'vloper
    job: Developer
    skill: Elite
    employed: True
    foods:
      - Apple
      - Orange
      - Strawberry
      - Mango
    languages:
      perl: Elite
      python: Elite
      pascal: Lame
    education: |
      4 GCSEs
      3 A-Levels
      BSc in the Internet of Things

Gotchas
-------

While you can put just about anything into an unquoted scalar, there are some exceptions.
A colon followed by a space (or newline) ``": "`` is an indicator for a mapping.
A space followed by the pound sign ``" #"`` starts a comment.

Because of this, the following is going to result in a YAML syntax error:

.. code:: text

    foo: somebody said I should put a colon here: so I did

    windows_drive: c:

...but this will work:

.. code:: yaml

    windows_path: c:\windows

You will want to quote hash values using colons followed by a space or the end of the line:

.. code:: yaml

    foo: 'somebody said I should put a colon here: so I did'

    windows_drive: 'c:'

...and then the colon will be preserved.

Alternatively, you can use double quotes:

.. code:: yaml

    foo: "somebody said I should put a colon here: so I did"

    windows_drive: "c:"

The difference between single quotes and double quotes is that in double quotes
you can use escapes:

.. code:: yaml

    foo: "a \t TAB and a \n NEWLINE"

The list of allowed escapes can be found in the YAML Specification under "Escape Sequences" (YAML 1.1) or "Escape Characters" (YAML 1.2).

The following is invalid YAML:

.. code-block:: text

    foo: "an escaped \' single quote"


Further, Ansible uses "{{ var }}" for variables.  If a value after a colon starts
with a "{", YAML will think it is a dictionary, so you must quote it, like so:

.. code:: yaml

    foo: "{{ variable }}"

If your value starts with a quote the entire value must be quoted, not just part of it. Here are some additional examples of how to properly quote things:

.. code:: yaml

    foo: "{{ variable }}/additional/string/literal"
    foo2: "{{ variable }}\\backslashes\\are\\also\\special\\characters"
    foo3: "even if it is just a string literal it must all be quoted"

Not valid:

.. code:: text

    foo: "E:\\path\\"rest\\of\\path

In addition to ``'`` and ``"`` there are a number of characters that are special (or reserved) and cannot be used
as the first character of an unquoted scalar: ``[] {} > | * & ! % # ` @ ,``.

You should also be aware of ``? : -``. In YAML, they are allowed at the beginning of a string if a non-space
character follows, but YAML processor implementations differ, so it is better to use quotes.

In Flow Collections, the rules are a bit more strict:

.. code:: text

    a scalar in block mapping: this } is [ all , valid

    flow mapping: { key: "you { should [ use , quotes here" }

Boolean conversion is helpful, but this can be a problem when you want a literal `yes` or other boolean values as a string.
In these cases just use quotes:

.. code:: yaml

    non_boolean: "yes"
    other_string: "False"


YAML converts certain strings into floating-point values, such as the string
`1.0`. If you need to specify a version number (in a requirements.yml file, for
example), you will need to quote the value if it looks like a floating-point
value:

.. code:: yaml

  version: "1.0"


.. seealso::

   :ref:`working_with_playbooks`
       Learn what playbooks can do and how to write/run them.
   `YAMLLint <http://yamllint.com/>`_
       YAML Lint (online) helps you debug YAML syntax if you are having problems
   `Wikipedia YAML syntax reference <https://en.wikipedia.org/wiki/YAML>`_
       A good guide to YAML syntax
   `YAML 1.1 Specification <https://yaml.org/spec/1.1/>`_
       The Specification for YAML 1.1, which PyYAML and libyaml are currently
       implementing
   `YAML 1.2 Specification <https://yaml.org/spec/1.2/spec.html>`_
       For completeness, YAML 1.2 is the successor of 1.1
   :ref:`Communication<communication>`
       Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide
