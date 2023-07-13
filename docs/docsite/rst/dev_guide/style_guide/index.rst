.. _style_guide:

**********************************
Ansible documentation style guide
**********************************

Welcome to the Ansible style guide!
To create clear, concise, consistent, useful materials on docs.ansible.com, follow these guidelines:

.. contents::
   :local:

Linguistic guidelines
=====================

We want the Ansible documentation to be:

* clear
* direct
* conversational
* easy to translate

We want reading the docs to feel like having an experienced, friendly colleague
explain how Ansible works.

Stylistic cheat-sheet
---------------------

This cheat-sheet illustrates a few rules that help achieve the "Ansible tone":

+-------------------------------+------------------------------+----------------------------------------+
| Rule                          | Good example                 | Bad example                            |
+===============================+==============================+========================================+
| Use active voice              | You can run a task by        | A task can be run by                   |
+-------------------------------+------------------------------+----------------------------------------+
| Use the present tense         | This command creates a       | This command will create a             |
+-------------------------------+------------------------------+----------------------------------------+
| Address the reader            | As you expand your inventory | When the number of managed nodes grows |
+-------------------------------+------------------------------+----------------------------------------+
| Use standard English          | Return to this page          | Hop back to this page                  |
+-------------------------------+------------------------------+----------------------------------------+
| Use American English          | The color of the output      | The colour of the output               |
+-------------------------------+------------------------------+----------------------------------------+

Header case
-----------

Headers should be written in sentence case. For example, this section's title is
``Header case``, not ``Header Case`` or ``HEADER CASE``.


Avoid using Latin phrases
-------------------------

Latin words and phrases like ``e.g.`` or ``etc.``
are easily understood by English speakers.
They may be harder to understand for others and are also tricky for automated translation.

Use the following English terms in place of Latin terms or abbreviations:

+-------------------------------+------------------------------+
| Latin                         | English                      |
+===============================+==============================+
| i.e                           | in other words               |
+-------------------------------+------------------------------+
| e.g.                          | for example                  |
+-------------------------------+------------------------------+
| etc                           | and so on                    |
+-------------------------------+------------------------------+
| via                           | by/ through                  |
+-------------------------------+------------------------------+
| vs./versus                    | rather than/against          |
+-------------------------------+------------------------------+


reStructuredText guidelines
===========================

The Ansible documentation is written in reStructuredText and processed by Sphinx.
We follow these technical or mechanical guidelines on all rST pages:

.. _headers_style:

Header notation
---------------

`Section headers in reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#sections>`_
can use a variety of notations.
Sphinx will 'learn on the fly' when creating a hierarchy of headers.
To make our documents easy to read and to edit, we follow a standard set of header notations.
We use:

* ``###`` with overline, for parts:

.. code-block:: rst

      ###############
      Developer guide
      ###############

* ``***`` with overline, for chapters:

.. code-block:: rst

      *******************
      Ansible style guide
      *******************

* ``===`` for sections:

.. code-block:: rst

      Mechanical guidelines
      =====================

* ``---`` for subsections:

.. code-block:: rst

      Internal navigation
      -------------------

* ``^^^`` for sub-subsections:

.. code-block:: rst

      Adding anchors
      ^^^^^^^^^^^^^^

* ``"""`` for paragraphs:

.. code-block:: rst

      Paragraph that needs a title
      """"""""""""""""""""""""""""


Syntax highlighting - Pygments
------------------------------

The Ansible documentation supports a range of `Pygments lexers <https://pygments.org/>`_
for `syntax highlighting <https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#code-examples>`_ to make our code examples look good. Each code-block must be correctly indented and surrounded by blank lines.

The Ansible documentation allows the following values:

* none (no highlighting)
* ansible-output (a custom lexer for Ansible output)
* bash
* console
* csharp
* ini
* json
* powershell
* python
* rst
* sh
* shell
* shell-session
* text
* yaml
* yaml+jinja

For example, you can highlight Python code using following syntax:

.. code-block:: rst

      .. code-block:: python

         def my_beautiful_python_code():
            pass

.. _style_links:

Internal navigation
-------------------

`Anchors (also called labels) and links <https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html#ref-role>`_
work together to help users find related content.
Local tables of contents also help users navigate quickly to the information they need.
All internal links should use the ``:ref:`` syntax.
Every page should have at least one anchor to support internal ``:ref:`` links.
Long pages, or pages with multiple levels of headers, can also include a local TOC.

.. note::

	Avoid raw URLs. RST and sphinx allow ::code:`https://my.example.com`, but this is unhelpful for those using screen readers. ``:ref:`` links automatically pick up the header from the anchor, but for external links, always use the ::code:`link title <link-url>`_` format.

.. _adding_anchors_rst:

Adding anchors
^^^^^^^^^^^^^^

* Include at least one anchor on every page
* Place the main anchor above the main header
* If the file has a unique title, use that for the main page anchor:

.. code-block:: text

   .. _unique_page::

* You may also add anchors elsewhere on the page

Adding internal links
^^^^^^^^^^^^^^^^^^^^^

* All internal links must use ``:ref:`` syntax. These links both point to the anchor defined above:

.. code-block:: rst

   :ref:`unique_page`
   :ref:`this page <unique_page>`

The second example adds custom text for the link.

Adding links to modules and plugins
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use the ``:ansplugin:`` RST role to link to modules and plugins using their Fully Qualified Collection Name (FQCN):

.. code-block:: rst

  The ansible.builtin.copy module can be linked with
  :ansplugin:`ansible.builtin.copy#module`

  If you want to specify an explicit type, use:
  :ansplugin:`the copy module <ansible.builtin.copy#module>`

This displays as
"The ansible.builtin.copy module can be linked with :ansplugin:`ansible.builtin.copy#module`"
and
"If you want to specify an explicit type, use: :ansplugin:`the copy module <ansible.builtin.copy#module>`".

Instead of ``#module``, you can also specify ``#<plugin_type>`` to reference to a plugin of type ``<plugin_type>``:

.. code-block:: rst

   :ansplugin:`arista.eos.eos_config <arista.eos.eos_config#module>`
   :ansplugin:`kubernetes.core.kubectl connection plugin <kubernetes.core.kubectl#connection>`
   :ansplugin:`ansible.builtin.file lookup plugin <ansible.builtin.file#lookup>`

.. note::

    ``ansible.builtin`` is the FQCN for modules included in ansible-core.

Adding links to module and plugin options and return values
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use the ``:ansopt:`` and ``:ansretval:`` roles to reference options and return values of modules and plugins:

.. code-block:: rst

  :ansopt:`ansible.builtin.file#module:path` references the ``path`` parameter of the
  ``ansible.builtin.file`` module; :ansopt:`ansible.builtin.file#module:path=/root/.ssh/known_hosts`
  shows the assignment ``path=/root/.ssh/known_hosts`` as a clickable link.

  :ansretval:`ansible.builtin.stat#module:stat.exists` references the ``stat.exists`` return value
  of the ``ansible.builtin.stat`` module. You can also use ``=`` as for option values:
  :ansretval:`ansible.builtin.stat#module:stat.exists=true` shows ``stat.exists=true``.

  :ansopt:`foo` and :ansopt:`foo=bar` use the same markup for an option and an option
  assignment without a link; the same is true for return values: :ansretval:`foo` and
  :ansretval:`foo=bar`.

This displays as
":ansopt:`ansible.builtin.file#module:path` references the ``path`` parameter of the
``ansible.builtin.file`` module; :ansopt:`ansible.builtin.file#module:path=/root/.ssh/known_hosts`
shows the assignment ``path=/root/.ssh/known_hosts`` as a clickable link."
and
":ansretval:`ansible.builtin.stat#module:stat.exists` references the ``stat.exists`` return value
of the ``ansible.builtin.stat`` module. You can also use ``=`` as for option values:
:ansretval:`ansible.builtin.stat#module:stat.exists=true` shows ``stat.exists=true``."
and
":ansopt:`foo` and :ansopt:`foo=bar` use the same markup for an option and an option
assignment without a link; the same is true for return values: :ansretval:`foo` and
:ansretval:`foo=bar`.".

For both option and return values, ``.`` is used to reference suboptions and contained return values.
Array stubs (``[...]``) can be used to indicate that something is a list, for example the ``:retval:``
argument ``ansible.builtin.service_facts#module:ansible_facts.services['systemd'].state`` references
the ``ansible_facts.services.state`` return value of the ``ansible.builtin.service_facts`` module
(:ansretval:`ansible.builtin.service_facts#module:ansible_facts.services['systemd'].state`).

.. _local_toc:

Adding local TOCs
^^^^^^^^^^^^^^^^^

The page you're reading includes a `local TOC <https://docutils.sourceforge.io/docs/ref/rst/directives.html#table-of-contents>`_.
If you include a local TOC:

* place it below, not above, the main heading and (optionally) introductory text
* use the ``:local:`` directive so the page's main header is not included
* do not include a title

The syntax is:

.. code-block:: rst

   .. contents::
      :local:

Accessibility guidelines
=========================

Ansible documentation has a goal to be more accessible. Use the following guidelines to help us reach this goal.

Images and alternative text
  Ensure all icons, images, diagrams, and non text elements have a meaningful alternative-text description. Do not include screen captures of CLI output. Use ``code-block`` instead.

  .. code-block:: text

    .. image:: path/networkdiag.png
       :width: 400
       :alt: SpiffyCorp network diagram


Links and hypertext
  URLs and cross-reference links have descriptive text that conveys information about the content of the linked target. See :ref:`style_links` for how to format links.

Tables
  Tables have a simple, logical reading order from left to right, and top to bottom.
  Tables include a header row and avoid empty or blank table cells.
  Label tables with a descriptive title.

  .. code-block:: reStructuredText

    .. table:: File descriptions

      +----------+----------------------------+
      |File      |Purpose                     |
      +==========+============================+
      |foo.txt   |foo configuration settings  |
      +----------+----------------------------+
      |bar.txt   |bar configuration settings  |
      +----------+----------------------------+


Colors and other visual information
  * Avoid instructions that rely solely on sensory characteristics. For example, do not use ``Click the square, blue button to continue.``
  * Convey information by methods and not by color alone.
  * Ensure there is sufficient contrast between foreground and background text or graphical elements in images and diagrams.
  * Instructions for navigating through an interface make sense without directional indicators such as left, right, above, and below.

Accessibility resources
------------------------

Use the following resources to help test your documentation changes:

* `axe DevTools browser extension <https://chrome.google.com/webstore/detail/axe-devtools-web-accessib/lhdoppojpmngadmnindnejefpokejbdd?hl=en-US&_ga=2.98933278.1490638154.1645821120-953800914.1645821120>`_ - Highlights accessibility issues on a website page.
* `WAVE browser extension <https://wave.webaim.org/extension/>`_ from WebAIM  - another accessibility tester.
* `Orca screen reader <https://help.gnome.org/users/orca/stable/>`_ - Common tool used by people with vision impairments.
* `color filter <https://www.toptal.com/designers/colorfilter/>`_ - For color-blind testing.

More resources
==============

These pages offer more help with grammatical, stylistic, and technical rules for documentation.

.. toctree::
  :maxdepth: 1

  basic_rules
  voice_style
  trademarks
  grammar_punctuation
  spelling_word_choice
  search_hints
  resources

.. seealso::

   :ref:`community_documentation_contributions`
       How to contribute to the Ansible documentation
   :ref:`testing_documentation_locally`
       How to build the Ansible documentation
   `irc.libera.chat <https://libera.chat>`_
       #ansible-docs IRC chat channel
