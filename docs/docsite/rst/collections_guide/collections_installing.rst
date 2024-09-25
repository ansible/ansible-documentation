.. _collections_installing:

Installing collections
======================

.. note::

  If you install a collection manually as described in this paragraph, the collection will not be upgraded automatically when you upgrade the ``ansible`` package or ``ansible-core``.

Installing collections in containers
------------------------------------

You can install collections with their dependencies in containers known as Execution Environments.
See :ref:`getting_started_ee_index` for details.

Installing collections with ``ansible-galaxy``
----------------------------------------------


By default, ``ansible-galaxy collection install`` uses https://galaxy.ansible.com as the Galaxy server (as listed in the
:file:`ansible.cfg` file under :ref:`galaxy_server`). You do not need any further configuration.
By default, Ansible installs the collection in ``~/.ansible/collections`` under the ``ansible_collections`` directory.

See :ref:`Configuring the ansible-galaxy client <galaxy_server_config>` if you are using any other Galaxy server, such as Red Hat Automation Hub.

To install a collection hosted in Galaxy:

.. code-block:: bash

   ansible-galaxy collection install my_namespace.my_collection

To upgrade a collection to the latest available version from the Galaxy server you can use the ``--upgrade`` option:

.. code-block:: bash

   ansible-galaxy collection install my_namespace.my_collection --upgrade

You can also directly use the tarball from your build:

.. code-block:: bash

   ansible-galaxy collection install my_namespace-my_collection-1.0.0.tar.gz -p ./collections

You can build and install a collection from a local source directory. The ``ansible-galaxy`` utility builds the collection using the ``MANIFEST.json`` or ``galaxy.yml``
metadata in the directory.

.. code-block:: bash

   ansible-galaxy collection install /path/to/collection -p ./collections

You can also install multiple collections in a namespace directory.

.. code-block:: text

   ns/
   ├── collection1/
   │   ├── MANIFEST.json
   │   └── plugins/
   └── collection2/
       ├── galaxy.yml
       └── plugins/

.. code-block:: bash

   ansible-galaxy collection install /path/to/ns -p ./collections

.. note::
    The install command automatically appends the path ``ansible_collections`` to the one specified  with the ``-p`` option unless the
    parent directory is already in a folder called ``ansible_collections``.


When using the ``-p`` option to specify the install path, use one of the values configured in :ref:`COLLECTIONS_PATHS`, as this is
where Ansible itself will expect to find collections. If you don't specify a path, ``ansible-galaxy collection install`` installs
the collection to the first path defined in :ref:`COLLECTIONS_PATHS`, which by default is ``~/.ansible/collections``

.. _installing_signed_collections:

Installing collections with signature verification
---------------------------------------------------

If a collection has been signed by a :term:`distribution server`, the server will provide ASCII armored, detached signatures to verify the authenticity of the ``MANIFEST.json`` before using it to verify the collection's contents. This option is not available on all distribution servers. See :ref:`distributing_collections` for a table listing the servers that support collection signing.

To use signature verification for signed collections:

1. :ref:`Configured a GnuPG keyring <galaxy_gpg_keyring>` for ``ansible-galaxy``, or provide the path to the keyring with the ``--keyring`` option when you install the signed collection.
   

2. Import the public key from the distribution server into that keyring.
   
   .. code-block:: bash

     gpg --import --no-default-keyring --keyring ~/.ansible/pubring.kbx my-public-key.asc


3. Verify the signature when you install the collection.
   
   .. code-block:: bash

     ansible-galaxy collection install my_namespace.my_collection --keyring ~/.ansible/pubring.kbx

   The ``--keyring`` option is not necessary if you have :ref:`configured a GnuPG keyring <galaxy_gpg_keyring>`. 

4. Optionally, verify the signature at any point after installation to prove the collection has not been tampered with. See :ref:`verify_signed_collections` for details.


You can also include signatures in addition to those provided by the distribution server. Use the ``--signature`` option to verify the collection's ``MANIFEST.json`` with these additional signatures. Supplemental signatures should be provided as URIs.

.. code-block:: bash

   ansible-galaxy collection install my_namespace.my_collection --signature https://examplehost.com/detached_signature.asc --keyring ~/.ansible/pubring.kbx

GnuPG verification only occurs for collections installed from a distribution server. User-provided signatures are not used to verify collections installed from Git repositories, source directories, or URLs/paths to tar.gz files.

You can also include additional signatures in the collection ``requirements.yml`` file under the ``signatures`` key.

.. code-block:: yaml

   # requirements.yml
   collections:
     - name: ns.coll
       version: 1.0.0
       signatures:
         - https://examplehost.com/detached_signature.asc
         - file:///path/to/local/detached_signature.asc

See :ref:`collection requirements file <collection_requirements_file>` for details on how to install collections with this file.

By default, verification is considered successful if a minimum of 1 signature successfully verifies the collection. The number of required signatures can be configured with ``--required-valid-signature-count`` or :ref:`GALAXY_REQUIRED_VALID_SIGNATURE_COUNT`. All signatures can be required by setting the option to ``all``. To fail signature verification if no valid signatures are found, prepend the value with ``+``, such as ``+all`` or ``+1``.

.. code-block:: bash

   export ANSIBLE_GALAXY_GPG_KEYRING=~/.ansible/pubring.kbx
   export ANSIBLE_GALAXY_REQUIRED_VALID_SIGNATURE_COUNT=2
   ansible-galaxy collection install my_namespace.my_collection --signature https://examplehost.com/detached_signature.asc --signature file:///path/to/local/detached_signature.asc

Certain GnuPG errors can be ignored with ``--ignore-signature-status-code`` or :ref:`GALAXY_REQUIRED_VALID_SIGNATURE_COUNT`. :ref:`GALAXY_REQUIRED_VALID_SIGNATURE_COUNT` should be a list, and ``--ignore-signature-status-code`` can be provided multiple times to ignore multiple additional error status codes.

This example requires any signatures provided by the distribution server to verify the collection except if they fail due to NO_PUBKEY:

.. code-block:: bash

   export ANSIBLE_GALAXY_GPG_KEYRING=~/.ansible/pubring.kbx
   export ANSIBLE_GALAXY_REQUIRED_VALID_SIGNATURE_COUNT=all
   ansible-galaxy collection install my_namespace.my_collection --ignore-signature-status-code NO_PUBKEY

If verification fails for the example above, only errors other than NO_PUBKEY will be displayed.

If verification is unsuccessful, the collection will not be installed. GnuPG signature verification can be disabled with ``--disable-gpg-verify`` or by configuring :ref:`GALAXY_DISABLE_GPG_VERIFY`.


.. _collections_older_version:

Installing an older version of a collection
-------------------------------------------

.. include:: ../shared_snippets/installing_older_collection.txt

.. _collection_requirements_file:

Install multiple collections with a requirements file
-----------------------------------------------------

.. include:: ../shared_snippets/installing_multiple_collections.txt

.. _collection_offline_download:

Downloading a collection for offline use
-----------------------------------------

.. include:: ../shared_snippets/download_tarball_collections.txt

.. _collection_local_install:

Installing collections adjacent to playbooks
--------------------------------------------

You can install collections locally next to your playbooks inside your project instead of in a global location on your system or on AWX.

Using locally installed collections adjacent to playbooks has some benefits, such as:

* Ensuring that all users of the project use the same collection version.
* Using self-contained projects makes it easy to move across different environments. Increased portability also reduces overhead when setting up new environments. This is a benefit when deploying Ansible playbooks in cloud environments.
* Managing collections locally lets you version them along with your playbooks.
* Installing collections locally isolates them from global installations in environments that have multiple projects.

Here is an example of keeping a collection adjacent to the current playbook, under a ``collections/ansible_collections/`` directory structure.

.. code-block:: text

    ./
    ├── play.yml
    ├── collections/
    │   └── ansible_collections/
    │               └── my_namespace/
    │                   └── my_collection/<collection structure lives here>


See :ref:`collection_structure` for details on the collection directory structure.

Installing a collection from source files
-----------------------------------------

.. include:: ../shared_snippets/installing_collections_file.rst

Installing a collection from a Git repository
---------------------------------------------

.. include:: ../shared_snippets/installing_collections_git_repo.txt

.. _galaxy_server_config:

Configuring the ``ansible-galaxy`` client
------------------------------------------

.. include:: ../shared_snippets/galaxy_server_list.txt


Removing a collection
=====================

If you no longer need a collection, simply remove the installation directory from your filesystem. 
The path can be different depending on your operating system:

.. code-block:: bash

  rm -rf ~/.ansible/collections/ansible_collections/community/general
  rm -rf ./venv/lib/python3.9/site-packages/ansible_collections/community/general
