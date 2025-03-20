.. _working_with_zos:


Managing z/OS UNIX hosts with Ansible
=====================================


Ansible can connect to `IBM z/OS UNIX System Services <https://www.ibm.com/docs/en/zos/latest?topic=descriptions-zos-unix-system-services>`_ to bring your Ansible Automation strategy to IBM z/OS.
This enables development and operations automation on IBM Z through a seamless, unified workflow orchestration with
configuration management, provisioning, and application deployment with Ansible.


Ansible and z/OS UNIX System Services
-------------------------------------
UNIX System Services can support the required dependencies for an Ansible managed node including running Python and
spawning interactive shell processes through SSH connections.
Ansible can target UNIX System Services nodes to modify files, directories, and so on, through ``ansible.builtin`` modules.
Further, anything that one can do by typing command(s) into the UNIX System Services shell can be captured
and automated in an Ansible playbook.


The z/OS landscape
------------------
While most systems process files in two modes - binary or text encoded in UTF-8,
IBM z/OS including UNIX System Services features an additional third mode - text encoded in EBCDIC.
Ansible has provisions to handle binary data and UTF-8 encoded textual data, but not EBCDIC encoded data.
This is not necessarily a limitation, it simply requires additional tasks that convert files to and from their original encodings.
It is up to the Ansible user managing z/OS UNIX nodes to understand the nature of the files in their automation.

The type (binary or text) and encoding of files can be stored in file "tags".
File tags is a z/OS UNIX System Services concept (part of Enhanced ASCII) designed to distinguish binary
files from UTF-8 encoded text files and EBCDIC-encoded text files.

Default behavior for an un-tagged file or stream is determined by the program, for example,
`IBM Open Enterprise SDK for Python <https://www.ibm.com/products/open-enterprise-python-zos>`__ defaults to the UTF-8 encoding.

Ansible modules will not read or recognize file tags. It is up to the user to determine the nature of remote data and tag it appropriately.
Data sent to remote z/OS UNIX hosts through Ansible is, by default, encoded in UTF-8 and not tagged.
Tagging a file is achievable with an additional task using the :ansplugin:`ansible.builtin.command#module` module.

.. code-block:: yaml

    - name: Tag my_file.txt as UTF-8.
      ansible.builtin.command: chtag -tc iso8859-1 my_file.txt


The `z/OS shell <https://www.ibm.com/docs/en/zos/latest?topic=shells-introduction-zos>`_ available on
z/OS UNIX System Services defaults to an EBCDIC encoding for un-tagged data streams.
Ansible sends untagged UTF-8 encoded textual data to the z/OS shell which expects untagged data to be encoded in EBCDIC.
This mismatch in data encodings can be resolved by setting the ``PYTHONSTDINENCODING`` environment variable,
which causes the pipe used by Python to be tagged with the specified encoding.
File and pipe tags can be used with automatic conversion between ASCII and EBCDIC, but only programs on
z/OS UNIX which are aware of tags will use them.


Using ``ansible.builtin`` modules with z/OS UNIX
------------------------------------------------

The ``ansible.builtin`` modules operate under the assumption that all textual data (files and pipes/streams) is UTF-8 encoded.
On z/OS, since textual data (file or stream) is sometimes encoded in EBCDIC and sometimes in UTF-8, special care must be taken to identify the correct encoding of target data.

Here are some notes / pro-tips when using the ``ansible.builtin`` modules with z/OS UNIX. This is by no means a comprehensive list.
Before using any Ansible modules, you must first :ref:`configure_zos_remote_environment`.

* :ansplugin:`ansible.builtin.command#module` / :ansplugin:`ansible.builtin.shell#module`
    The command and shell modules are excellent for automating tasks for which command line solutions already exist.
    The thing to keep in mind when using these modules is that depending on the system configuration, the z/OS shell (``/bin/sh``) may return output in EBCDIC.
    The LE environment variable configurations will correctly convert streams if they are tagged and return readable output to Ansible.
    However, some command line programs may return output in UTF-8 and not tag the pipe.
    In this case, the autoconversion may incorrectly assume output is in EBCDIC and attempt to convert it and yield unreadable data.
    If the source encoding is known, you can use the :ansplugin:`ansible.builtin.shell#module` module's capability to chain commands together through pipes,
    and pipe the output to ``iconv``. In this example, you may need to select other encodings for the 'to' and 'from' that represent your file encodings.

    .. code-block:: yaml

        ansible.builtin.shell: "some_pgm | iconv -f ibm-1047 -t iso8859-1"


* :ansplugin:`ansible.builtin.raw#module`
    The raw module, by design, ignores all remote environment settings. However, z/OS UNIX System Services managed nodes require some base configurations.
    To use this module with UNIX System Services, configure the minimum environment variables as a chain of export statements before the desired command.

    .. code-block:: yaml

        ansible.builtin.raw: |
            export _BPXK_AUTOCVT: "ON" ;
            export _CEE_RUNOPTS: "FILETAG(AUTOCVT,AUTOTAG) POSIX(ON)" ;
            export _TAG_REDIR_ERR: "txt" ;
            export _TAG_REDIR_IN: "txt" ;
            export _TAG_REDIR_OUT: "txt" ;
            echo "hello world!"

    Alternatively, consider using the :ansplugin:`ansible.builtin.command#module` or :ansplugin:`ansible.builtin.shell#module` modules mentioned above,
    which set up the configured remote environment for each task.


* :ansplugin:`ansible.builtin.copy#module` / :ansplugin:`ansible.builtin.fetch#module`
    The ``ansible.builtin`` modules will NOT automatically tag files, nor will existing file tags be honored nor preserved.
    You can treat files as binaries when running copy/fetch operations, there is no issue in terms of data integrity,
    but remember to restore the file tag once the file is returned to z/OS UNIX, as tags are not preserved. Use the command module
    to set the file tag:

    .. code-block:: yaml

        - name: Tag my_file.txt as UTF-8.
          ansible.builtin.command: chtag -tc iso8859-1 my_file.txt

* :ansplugin:`ansible.builtin.blockinfile#module` / :ansplugin:`ansible.builtin.lineinfile#module`
    These modules process all data in UTF-8. Ensure target files are UTF-8 encoded beforehand and re-tag the files afterwards.

* :ansplugin:`ansible.builtin.script#module`
    The built in script module copies a local script file to a temp file on the remote target and runs it.
    The issue that z/OS UNIX System Services targets run into is that when the underlying z/OS shell attempts to read
    the script file, since the file does not get tagged as UTF-8 text, the shell assumes that the file is encoded in EBCDIC,
    and fails to correctly read or run the script.
    One work-around is to manually copy local files to managed nodes (:ansplugin:`ansible.builtin.copy#module` ) and convert or tag files (with the :ansplugin:`ansible.builtin.command#module` module).
    With this work-around, some of the conveniences of the script module are lost, such as automatically cleaning up the script file once it is run,
    but it is trivial to perform those steps as additional playbook tasks.

    .. code-block:: yaml

        - name: Copy local script file to remote node.
          ansible.builtin.copy:
            src: "{{ playbook_dir }}/local/scripts/sample.sh"
            dest: /u/ibmuser/scripts/

        - name: Tag remote script file.
          ansible.builtin.command: "chtag -tc ISO8859-1 /u/ibmuser/scripts/sample.sh"

        - name: Run script.
          ansible.builtin.command: "/u/ibmuser/scripts/sample.sh"

    Another work-around is to store local script files in EBCDIC.
    They may be unreadable on the ansible control node, but they will copy correctly to z/OS UNIX System Services targets in EBCDIC,
    and the script will run. This approach takes advantage of the built-in conveniences of the script module,
    but managing unreadable EBCDIC files locally makes maintaining those script files more difficult.

.. _configure_zos_remote_environment:

Configure the remote environment
--------------------------------

Certain Language Environment (LE) configurations enable automatic encoding conversion and automatic file tagging functionality
required by Python on z/OS UNIX systems (`IBM Open Enterprise SDK for Python <https://www.ibm.com/products/open-enterprise-python-zos>`_ ).

Include the following configurations when setting the remote environment for any z/OS UNIX managed nodes:

.. code-block:: yaml

    _BPXK_AUTOCVT: "ON"
    _CEE_RUNOPTS: "FILETAG(AUTOCVT,AUTOTAG) POSIX(ON)"

    _TAG_REDIR_ERR: "txt"
    _TAG_REDIR_IN: "txt"
    _TAG_REDIR_OUT: "txt"


Ansible can be configured with remote environment variables in these options:


    * inventory - inventory.yml, group_vars/all.yml, or host_vars/all.yml
    * playbook - ``environment`` variable at top of playbook.
    * block or task - ``environment`` key word.

For more details, see :ref:`playbooks_environment`.

Configure the remote Python interpreter
---------------------------------------

Ansible requires a Python interpreter to run most modules on the remote host, and it checks for Python at the 'default' path ``/usr/bin/python``.

On z/OS UNIX, the Python3 interpreter (from `IBM Open Enterprise SDK for Python <https://www.ibm.com/products/open-enterprise-python-zos>`_)
is often installed to a different path, typically something like: ``/usr/lpp/cyp/v3r12/pyz``.

The path to the Python interpreter can be configured with the Ansible inventory variable ``ansible_python_interpreter``.
For example:

.. code-block:: ini

    zos1 ansible_python_interpreter:/usr/lpp/cyp/v3r12/pyz

When the path to the Python interpreter is not found in the default location on the target host,
an error containing the following message may result: ``/usr/bin/python: FSUM7351 not found``

For more details, see: :ref:`python_interpreters`.

Configure the remote shell
--------------------------
The z/OS UNIX System Services managed node includes several shells.
Currently the only supported shell is the z/OS Shell located in path ``/bin/sh``.
To configure which shell the Ansible control node uses on the target node, set inventory variable
:ref:`ansible_shell_executable<ansible_shell_executable>`. For example:

.. code-block:: ini

    zos1 ansible_shell_executable=/bin/sh

Enable Ansible pipelining
-------------------------
Enable :ref:`ANSIBLE_PIPELINING` in the ansible.cfg file.

When Ansible pipelining is enabled, Ansible passes any module code to the remote target node
through Python's stdin pipe and runs it in all in a single call rather than copying data to temporary files first and then reading from those files.
For more details on pipelining, see: :ref:`flow_pipelining`.

Enabling this behavior is encouraged because Python will tag its pipes with the proper encoding, so there is less chance of encountering encoding errors.
Further, using Python stdin pipes is more performant than file I/O.


Include the following in the environment for any tasks performed on z/OS UNIX managed nodes.

.. code-block:: yaml

    PYTHONSTDINENCODING: "cp1047"

When Ansible pipelining is enabled but the ``PYTHONSTDINENCODING`` property is not correctly set, the following error may result.
Note, the hex ``'\x81'`` below may vary depending on the source causing the error:

.. code-block:: text

    SyntaxError: Non-UTF-8 code starting with '\\x81' in file <stdin> on line 1, but no encoding declared; see https://peps.python.org/pep-0263/ for details


Unreadable characters
---------------------

Seeing unreadable characters in playbook output is most typically an EBCDIC encoding mix up.
Double check that the remote environment is set up properly.
Also check the expected file encodings, both on the remote node and the control node.
``ansible.builtin`` modules will assume all textual data is UTF-8 encoded, while z/OS UNIX may be using EBCDIC.
On many z/OS UNIX systems, the default encoding for untagged files is EBCDIC.
This variation in default settings can easily lead to data being misinterpreted with the wrong encoding,
whether that is failing to auto convert EBCDIC to UTF-8 or erroneously attempting to convert data that is already in UTF-8.

.. _zos_as_control_node:

Using z/OS as a control node
----------------------------

The z/OS operating system currently cannot be configured to run as an Ansible control node.
z/OS UNIX System Services interface also cannot be configured to run as an Ansible control node, despite being POSIX-compliant.

There are options available on the IBM Z platform to use it as a control node:

* IBM z/OS Container Extensions (zCX)
* Red Hat OpenShift on IBM zSystems and LinuxONE
* Linux on IBM Z