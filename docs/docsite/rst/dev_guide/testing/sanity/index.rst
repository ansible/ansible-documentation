.. _all_sanity_tests:

Sanity Tests
============

The following sanity tests are available as ``--test`` options for ``ansible-test sanity`` when testing Ansible Collections.
This list is also available using ``ansible-test sanity --list-tests --allow-disabled``.

For information on how to run these tests, see :ref:`sanity testing guide <testing_sanity>`.

.. toctree::
   :maxdepth: 1

   action-plugin-docs
   ansible-doc
   changelog
   compile
   empty-init
   ignores
   import
   line-endings
   no-assert
   no-basestring
   no-dict-iteritems
   no-dict-iterkeys
   no-dict-itervalues
   no-get-exception
   no-illegal-filenames
   no-main-display
   no-smart-quotes
   no-unicode-literals
   pep8
   pslint
   pylint
   replace-urlopen
   runtime-metadata
   shebang
   shellcheck
   symlinks
   use-argspec-type-path
   use-compat-six
   validate-modules
   yamllint

Additional tests are available when testing Ansible Core:

.. toctree::
   :maxdepth: 1

   ansible-requirements
   bin-symlinks
   boilerplate
   integration-aliases
   mypy
   no-unwanted-files
   obsolete-files
   package-data
   pymarkdown
   release-names
   required-and-default-attributes
   test-constraints
