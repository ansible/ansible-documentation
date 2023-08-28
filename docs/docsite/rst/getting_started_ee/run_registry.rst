.. _running_local_registry:

Running local podman registry for EEs
=====================================

After building an execution environment, you can push it to a registry and use on your other machines with ``ansible-navigator`` or in Ansible AWX/Automation controller jobs.

This guide will show you how to set up a basic local podman registry for your execution environments as a systemd unit run on behalf of a non-root user.

Setting up a registry server
----------------------------

Log in to your machine as a non-root user with the ``sudo`` permission.

1. Install the required packages:

.. code-block:: bash

  sudo dnf install podman httpd-tools

2. Create directories on the host system which will be later mounted in the container running your registry:

.. code-block:: bash

  mkdir -p ~/registry/{auth,data}

3. Generate a file containing credentials for accessing the registry:

.. code-block:: bash

  htpasswd -bBc ~/registry/auth/htpasswd myuser mypassword

In the command above, ``myuser`` and ``mypassword`` can be replaced with any value you want to use as credentials to log in to to the registry.

4. Create a directory to store a systemd unit for the registry container you are about to create and change your location to the directory:

.. code-block:: bash

  mkdir -p ~/.config/systemd/user && ~/.config/systemd/user

5. Run the registry container:

.. code-block:: bash

  podman run -d --rm --name myregistry -p 5000:5000 \
  -v ~/registry/data:/var/lib/registry:z \
  -v ~/registry/auth:/auth:z \
  -e "REGISTRY_AUTH=htpasswd" \
  -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" \
  -e "REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd" \
  docker.io/library/registry:latest

6. Generate a systemd unit file based on the running ``myregistry`` container you created in the previous step:

.. code-block:: bash

  podman generate systemd --name myregistry --files --new

7. Stop the ``myregistry`` container:

.. code-block:: bash

  podman stop myregistry

8. Reload systemd and start your registry container as a systemd unit:

.. code-block:: bash

  systemctl --user --daemon-reload
  systemctl --user enable --now container-myregistry.service
  systemctl --user status container-myregistry.service
  loginctl enable-linger

From now on, your registry container will start automatically after system reboot on behalf of your current regular user.

9. Open port 5000 in your firewall:

.. code-block:: bash

  sudo firewall-cmd --add-port=5000/tcp --permanent
  sudo firewall-cmd --reload

10. Reboot your machine and check if systemd has started the unit:

.. code-block:: bash

   systemctl --user status container-myregistry.service

11. Check the container is running:

.. code-block:: bash

   podman ps

   CONTAINER ID  IMAGE                              COMMAND               CREATED        STATUS          PORTS                   NAMES
   31ef59550685  docker.io/library/registry:latest  /etc/docker/regis...  2 seconds ago  Up 3 seconds    0.0.0.0:5000->5000/tcp  myregistry

Your registry now is available by using the ``myregistry:5000`` URL.

Pushing your execution environment to the registry
--------------------------------------------------

1. Log in to your machine where you :ref:`built your execution environment<building_execution_environments>`.

2. Make sure ``myregistry`` is resolvable by DNS or the ``/etc/hosts`` file from your client to the IP address of your registry machine.

3. Create the ``registries.conf`` file  and put the following content in it:

.. code-block:: bash

  mkdir -p ~/.config/containers/
  
  cat > ~/.config/containers/registries.conf<<EOF
  [[registry]]
  location="myregistry:5000"
  insecure=true
  EOF

4. Log in to the registry:

.. code-block:: bash

  podman login myregistry:5000

The command will ask you a login and password. Use those you passed to the ``htpasswd`` command when setting up the registry.

5. We assume, you have the following execution environment :ref:`built locally<building_execution_environments>`:

.. code-block:: bash

  podman images

  REPOSITORY                                  TAG         IMAGE ID      CREATED      SIZE
  localhost/postgresql_ee                     latest      1d39f6a0fbeb  2 weeks ago  388 MB

6. Add tags associated with the registry to the image:

.. code-block:: bash

  podman tag localhost/postgresql_ee myregistry:5000/postgresql_ee:1.0
  podman tag localhost/postgresql_ee myregistry:5000/postgresql_ee:latest

7. Push the execution environments to the registry:

.. code-block:: bash

  podman push myregistry:5000/postgresql_ee:1.0
  podman push myregistry:5000/postgresql_ee:latest

8. List the tags for the image available in the registry:

.. code-block:: bash

  podman search --list-tags myregistry:5000/postgresql_ee

  NAME                           TAG
  myregistry:5000/postgresql_ee  1.0
  myregistry:5000/postgresql_ee  latest

Now you can similarly log in to the registry from your other machines and run the execution environment with :ref:`ansible-navigator<running_execution_environments>` or in your `Ansible AWX/Automation Controller jobs <https://docs.ansible.com/automation-controller/latest/html/userguide/execution_environments.html#use-an-execution-environment-in-jobs>`_.
