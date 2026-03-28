.. _collection_quickstart:

*******************************************
Creating your first collection pull request
*******************************************

This guide describes how to create a patch and submit a pull request for an Ansible collection.

.. _collection_prepare_local:

Prepare your environment
========================

These steps assume a Linux work environment with ``git`` installed.

1. Install ``podman``. Running tests in a container ensures proper isolation and a consistent environment.

2. :ref:`Install ansible-core <installation_guide>`. You need the ``ansible-test`` utility, which this package provides.

3. Create the following directories in your home directory:

  .. code-block:: bash

    $ mkdir -p ~/ansible_collections/NAMESPACE/COLLECTION_NAME


  For example, if the collection is ``community.mysql``, it would be:

  .. code-block:: bash

    $ mkdir -p ~/ansible_collections/community/mysql


4. Fork the collection repository through the GitHub web interface.

5. Clone the forked repository from your profile to the path you created:

  .. code-block:: bash

    $ git clone https://github.com/YOURACC/COLLECTION_REPO.git ~/ansible_collections/NAMESPACE/COLLECTION_NAME

  Alternatively, use the SSH protocol:

  .. code-block:: bash

    $ git clone git@github.com:YOURACC/COLLECTION_REPO.git ~/ansible_collections/NAMESPACE/COLLECTION_NAME

6. Navigate to the repository you cloned:

  .. code-block:: bash

    $ cd ~/ansible_collections/NAMESPACE/COLLECTION_NAME

7. Verify that you are on the default branch, typically ``main``:

  .. code-block:: bash

    $ git status

8. Display the remotes. You should see only the ``origin`` repository:

  .. code-block:: bash

    $ git remote -v

9. Add the ``upstream`` repository. This is the repository from which you forked:

  .. code-block:: bash

    $ git remote add upstream https://github.com/ansible-collections/COLLECTION_REPO.git

10. Update your local default branch. If your default branch is ``main``, run:

  .. code-block:: bash

    $ git fetch upstream
    $ git rebase upstream/main

11. Create a branch for your changes:

  .. code-block:: bash

    $ git checkout -b name_of_my_branch

Change the code
===============

Do not combine multiple unrelated bug fixes or features in a single pull request. Instead, use separate pull requests for different changes.

Start by writing integration and unit tests, if applicable. These tests can verify that a bug exists before you apply your code fix and confirm that your code fixed the bug once the tests pass.

Add integration tests
---------------------

.. note::

  * Some collections do not have integration tests. In such cases, unit tests are highly recommended.
  * If you have difficulty writing or running tests, or you are unsure if a case can be covered, skip this step. Other contributors can help you with tests later if needed.

All integration tests reside in ``tests/integration/targets`` subdirectories.

Navigate to the subdirectory that contains the name of the module you plan to change.
For example, if you are fixing the ``mysql_user`` module in the ``community.mysql`` collection, its tests are in ``tests/integration/targets/test_mysql_user/tasks``.

The ``main.yml`` file contains test tasks and includes other test files.
Look for a suitable existing test file to integrate your tests, or create and include a dedicated test file.
You can use an existing test file as a template.

When you fix a bug, write a task that reproduces the bug from the reported issue.
Then run integration tests by using the following command:

.. code-block:: bash

  $ ansible-test integration TEST_TARGET_DIRECTORY_NAME --docker -v

For example, if you want to run tasks residing in ``tests/integration/targets/test_mysql_user/``, the command is:

.. code-block:: bash

  $ ansible-test integration test_mysql_user --docker -v

You can use the ``-vv`` or ``-vvv`` argument for more detailed output.

The examples above automatically download and use the default test image to create and run a test container.
Use the default test image for platform-independent integration tests.

If you need to run tests against a specific distribution, see the :ref:`list of supported container images <test_container_images>`. For example:

.. code-block:: bash

  $ ansible-test integration TEST_TARGET_DIRECTORY_NAME --docker fedora40 -v

If you are unsure whether to use the default image or a specific image for testing, skip this step. The community can assist you later. You can also inspect the collection repository's CI to determine which containers it uses.

If the tests run successfully, two outcomes are possible:

* If the bug has not appeared and the tests passed, ask the reporter for more details. The issue might not be a bug, or it might relate to a specific software version or the reporter's local environment configuration.
* The bug appeared, and the tests failed as expected, showing the reported symptoms.

Add unit tests
--------------

.. note::

  * Some collections do not have unit tests. In such cases, focus on integration tests.
  * If you have difficulty writing or running tests, or you are unsure if a case can be covered, skip this step. Other contributors can help you with tests later if needed.

We recommend that you cover all changes with unit tests.

* **Location**: All unit tests are located in the ``tests/unit/`` directory.
* **Adding Tests**:

  * Find an existing test file that corresponds to the code you are modifying.
  * If a relevant file doesn't exist, create a new one.
  * Use ``Pytest`` as testing framework.

See the :ref:`test_your_changes` section for detailed instructions on how to run the unit tests.

.. _test_your_changes:

Test your changes
=================

To test your changes, complete the following steps:

1. Install ``flake8``.

2. Run ``flake8`` against a changed file:

  .. code-block:: bash

    $ flake8 path/to/changed_file.py

  This command identifies unused imports, which sanity tests do not show, and other common issues.
  Optionally, you can use the ``--max-line-length=160`` command-line argument.

3. Run sanity tests:

  .. code-block:: bash

    $ ansible-test sanity path/to/changed_file.py --docker -v

  If the tests fail, carefully examine the output; it provides informative details that help you quickly identify the problem line.
  Sanity failures typically relate to incorrect code and documentation formatting.

4. Run integration tests:

  .. code-block:: bash

    $ ansible-test integration TEST_TARGET_DIRECTORY_NAME --docker -v

  For example, if your changed test files are in ``tests/integration/targets/test_mysql_user/``, the command is:

  .. code-block:: bash

    $ ansible-test integration test_mysql_user --docker -v

  You can use the ``-vv`` or ``-vvv`` argument if you need more detailed output.

Two possible outcomes are:

* The tests failed. Examine the command's output. Fix the problem in the code and run the tests again. Repeat this cycle until the tests pass.
* The tests passed. If they originally failed, you have successfully fixed the bug.

5. In addition to integration tests, you can also cover your changes with unit tests. This is often necessary when integration tests do not apply to the collection.

We use `pytest <https://docs.pytest.org/en/latest/>`_ as a testing framework.

Unit test files are in the ``tests/unit/plugins/`` directory. To run unit tests, for example, for ``tests/unit/plugins/test_myclass.py``, use the following command:

.. code-block:: bash

  $ ansible-test units tests/unit/plugins/test_myclass.py --docker

To run all available unit tests in the collection, run:

.. code-block:: bash

  $ ansible-test units --docker

Submit a pull request
=====================

To submit a pull request, complete the following steps:

1. Commit your changes with a concise and informative commit message:

  .. code-block:: bash

    $ git add /path/to/changed/file
    $ git commit -m "module_name_you_fixed: fix crash when ..."

2. Push the branch to ``origin`` (your fork):

  .. code-block:: bash

    $ git push origin name_of_my_branch

3. In a browser, navigate to the ``upstream`` repository (http://github.com/ansible-collections/COLLECTION_REPO).

4. Click the :guilabel:`Pull requests` tab.

  GitHub tracks your fork and should automatically offer to create a pull request for your new branch. If GitHub does not do this, click the :guilabel:`New pull request` button yourself. Then, under the :guilabel:`Compare changes` title, choose :guilabel:`compare across forks`.

5. Choose your repository and the new branch you pushed in the right drop-down list. Confirm.

  a. Complete the pull request template with all relevant information.
  b. Add ``Fixes + link to the issue`` in the pull request's description.
  c. Click :guilabel:`Create pull request`.

6. Add a :ref:`changelog fragment <collection_changelog_fragments>` to the ``changelogs/fragments`` directory. This fragment will be published in the release notes, informing users about the fix.

  a. Run the sanity test for the fragment:

    .. code-block:: bash

      $ ansible-test sanity changelogs/fragments/ --docker -v


  b. If the tests passed, commit and push the changes:

    .. code-block:: bash

      $ git add changelogs/fragments/myfragment.yml
      $ git commit -m "Add changelog fragment"
      $ git push origin name_of_my_branch

7. Verify that the CI tests, which run automatically on Red Hat infrastructure, are successful.

  You will see the CI status at the bottom of your pull request. If the tests are green and you do not plan to add more commits, add a "Ready for review" comment.

8. If the pull request looks good to the community, committers will merge it. You can mention them explicitly.

For more detailed information on this process, see the :ref:`Ansible developer guide <developer_guide>`.
