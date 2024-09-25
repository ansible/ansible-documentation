:orphan:

**********
httptester
**********

.. contents:: Topics

Overview
========

``httptester`` is a docker container used to host certain resources required by :ref:`testing_integration`. This is to avoid CI tests requiring external resources (such as Git or package repos) which, if temporarily unavailable, would cause tests to fail.

HTTP Testing endpoint which provides the following capabilities:

* httpbin
* nginx
* SSL
* SNI
* Negotiate Authentication


Source files can be found in the `http-test-container <https://github.com/ansible/http-test-container>`_ repository.

Extending httptester
====================

If you have sometime to improve ``httptester``, open an issue in the 
`http-test-container <https://github.com/ansible/http-test-container>`_ repository.