.. _styleguide_basic:

Basic rules
===========
.. contents::
  :local:

Use standard American English
-----------------------------
Ansible uses Standard American English. Watch for common words that are spelled differently in American English (color vs colour, organize vs organise, and so on).

Write for a global audience
---------------------------
Everything you say should be understandable by people of different backgrounds and cultures. Avoid idioms and regionalism and maintain a neutral tone that cannot be misinterpreted. Avoid attempts at humor.

Follow naming conventions
-------------------------
Always follow naming conventions and trademarks.

.. good place to link to an Ansible terminology page

Use clear sentence structure
----------------------------
Clear sentence structure means:

- Start with the important information first.
- Avoid padding/adding extra words that make the sentence harder to understand.
- Keep it short - Longer sentences are harder to understand.

Some examples of improving sentences:

Bad:
    The unwise walking about upon the area near the cliff edge may result in a dangerous fall and therefore it is recommended that one remains a safe distance to maintain personal safety.

Better:
    Danger! Stay away from the cliff.

Bad:
    Furthermore, large volumes of water are also required for the process of extraction.

Better:
    Extraction also requires large volumes of water.

.. _one_sentence_per_line:

Use one sentence per line
-------------------------
Consider using a technique called *one sentence per line* when composing paragraphs, or use at least one line per sentence (following https://sembr.org/).
This technique allows you to format RST and Markdown source in a natural and semantic way that is easy to review and edit.

Lines of text that occur next to each other are rendered as a paragraph so readers do not notice the line breaks between sentences.
To create a new paragraph, add an empty line between sentences.
You can still soft wrap lines of text when using one sentence per line.
The important thing is that each line starts at the left margin.

Using one sentence per line reduces cognitive load and makes life much easier for people who review changes.
Diffs become much more straightforward and easier to parse.
For example, when multiple sentences are wrapped at a fixed column width, a change at the start of a paragraph causes the remaining lines in the paragraph to reposition.

In addition to the advantages for version control, one sentence per line makes it easier to do the following:

- Swap sentences around.
- Separate or join paragraphs.
- Comment individual sentences.
- Identify sentences that are too long or that vary widely in length.
- Spot redundant patterns in your writing.

For an example of the one sentence per line in the Ansible documentation, take a look at the RST source under ``docs/docsite/rst/getting_started/``.

Avoid verbosity
---------------
Write short, succinct sentences. Avoid terms like:

- "...as has been said before,"
- "..each and every,"
- "...point in time,"
- "...in order to,"

Highlight menu items and commands
---------------------------------
When documenting menus or commands, it helps to **bold** what is important.

For menu procedures, bold the menu names, button names, and so on to help the user find them on the GUI:

1. On the **File** menu, click **Open**.
2. Type a name in the **username** field.
3. In the **Open** dialog box, click **Save**.
4. On the toolbar, click the **Open File** icon.

For code or command snippets, use the RST `code-block directive <https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-code-block>`_:

.. code-block:: rst

   .. code-block:: bash

     ssh my_vyos_user@vyos.example.net
     show config
