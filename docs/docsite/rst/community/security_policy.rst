.. _security_policy:

***********************
Ansible security policy
***********************

.. contents::
   :local:

Commitment
==========

Red Hat is committed to maintaining the highest level of security and trust for all users.
Red Hat appreciates the Ansible community and security researchers' efforts in helping identify and address vulnerabilities responsibly.

Scope
=====

This policy applies to all Ansible projects that Red Hat hosts.

GitHub
------

Code contained in the following GitHub organizations:

* `ansible <https://github.com/ansible>`_
* `ansible-collections <https://github.com/ansible-collections>`_
* `ansible-community <https://github.com/ansible-community>`_
* `ansible-network <https://github.com/ansible-network>`_
* `ansible-security <https://github.com/ansible-security>`_
* `network-automation <https://github.com/network-automation>`_
* Any other Ansible related GitHub organizations that are managed by Red Hat

Release artifacts
-----------------

* Any Ansible collections from the preceding GitHub repositories.
* Any Ansible releases from the preceding GitHub repositories.
* `Ansible Community PyPI releases <https://pypi.org/org/ansible-community/>`_
* Ansible Community Package.
* Community execution environments.

Infrastructure
--------------

* `ansible.com`
* `docs.ansible.com`
* `forum.ansible.com`
* `*.ansible.com`

.. note::

   Third-party collections or plugins hosted outside the listed organizations are out of scope but are encouraged to adopt compatible practices.
   Red Hat works with maintainers of the repositories under the preceding GitHub organizations. Specifically, Red Hat helps triage and provide fixes for third-party collections in the ``ansible-collections`` GitHub organization.

Maintained versions
====================

Generally, only the latest release of a community project receives updates, including security patches.
Earlier versions may receive critical fixes on a best-effort basis but back-porting to unsupported versions is not guaranteed.
End-of-Life versions receive no backports unless extraordinary circumstances warrant an exception approved by the Ansible Security Team.

Some projects, such as Ansible Core, may backport security fixes into multiple supported versions depending on severity.
See :ref:`development_and_stable_version_maintenance_workflow` for details.

Reporting a vulnerability
=========================

How to report vulnerabilities
-----------------------------

All reports MUST be submitted by email to: `security@ansible.com <mailto:security@ansible.com>`_

Security vulnerabilities and security incidents MUST NOT be reported through any public method, including, but not limited to:

* Public GitHub issues.
* Pull requests.
* Ansible Forum.
* Ansible Matrix.
* Public forums or social media.

What to include in vulnerability reports
----------------------------------------

When submitting a vulnerability report, provide the following details:

* **Title** (required): Clear, descriptive summary.
* **Reporter details** (optional): Your name/handle and affiliation.
* **Impacted project** (required): Ideally link to the GitHub project.
* **Vulnerability description** (required): Technical details of the issue.
* **Affected versions** (required): All known affected version(s).
* **Reproduction steps** (required): Minimal example to reproduce the issue.
* **Impact assessment** (required): Potential exploit scenarios and severity.
* **Suggested fix** (optional): Proposed remediation, if any.
* **Disclosure status** (required): Whether this has been shared elsewhere.

What to report
--------------

Report if you have:

* Discovered a potential security vulnerability.
* Found an issue but are uncertain about its security impact.
* Identified vulnerabilities in dependencies not yet addressed.

What NOT to report
------------------

The following do not qualify as security vulnerabilities:

* Automated scanner output without analysis or reproduction steps.
* General support or usage questions. Use the `Ansible Community Forum <https://forum.ansible.com>`__ instead.
* Requests for help updating to newer versions.
* Bugs without security implications.

Bugs that have no security impact should be filed through the public issues tracker of the respective GitHub project.

Response process
================

The Ansible Security Team follows this process:

1. **Acknowledgment:** Confirms receipt of the report within one (1) business day.
2. **Triage:** Assesses validity and severity.
3. **Investigation:** Reproduces and analyzes the issue.
4. **Fix development:** Develops and tests a patch.
5. **Coordinated disclosure:** Coordinates release timing with the reporter.
6. **Public disclosure:** Publishes advisory and credits.

Severity classification
========================

The Ansible Security Team follows the `Red Hat severity ratings <https://access.redhat.com/security/updates/classification>`_.

Disclosure policy
=================

* The Ansible Security Team follows coordinated disclosure practices.
* Fixes are typically included in the next planned release.
* Critical vulnerabilities may warrant out-of-band releases.
* Public disclosure occurs through GitHub Security Advisories.
* Reporters are credited unless they prefer anonymity.

For detailed information on disclosure types, embargo periods, and researcher coordination, see the :ref:`vulnerability_management_policy`.

Security advisories
===================

Security advisories are published through:

* `Ansible Community Forum <https://forum.ansible.com/tag/security>`__.
* Official Ansible security page (`ansible.com/security <https://ansible.com/security>`__).
* CVE databases (NVD, OSV).

The ``SECURITY.md`` file
========================

``SECURITY.md`` is the standard location where users, developers, and security researchers can find information on how to report a potential vulnerability for a particular repository.
Projects SHOULD host a ``SECURITY.md`` file in the root directory of their GitHub repository, alongside ``README.md`` and ``LICENSE``.
This ensures high visibility and automatic integration with GitHub's security features.

Use the `SECURITY.md template <https://github.com/ansible-community/project-template/blob/main/SECURITY.md>`__ from the `ansible-community/project-template <https://github.com/ansible-community/project-template>`__ repository as a starting point for your project.

Recognition
===========

The Ansible Security Team may thank security researchers who help improve projects in the Ansible ecosystem through recognition in:

* Security advisories.
* `Ansible Community Forum <https://forum.ansible.com>`__.

Related documents
=================

* :ref:`vulnerability_management_policy` covers triage, remediation, coordinated disclosure, CVE management, and incident response processes.
* :ref:`secure_development_practices` indexes secure coding guidelines for Ansible modules, plugins, collections, and playbooks.

Policy updates
==============

This policy may be updated periodically.
Suggestions for improvement can be submitted through issues or pull requests to the `ansible-documentation <https://github.com/ansible/ansible-documentation>`_ repository.

For discussion about the EU Cyber Resilience Act and how it applies to the Ansible ecosystem, see the `CRA tag on the Ansible Forum <https://forum.ansible.com/tag/cra>`__.
To follow changes and suggest improvements to Ansible security practices, see the `infra-and-security tag on Ansible Forum <https://forum.ansible.com/tag/infra-and-security>`__.

Notes
=====

The key words "MUST", "MUST NOT", and "SHOULD" in this document are to be interpreted as described in :rfc:`2119`.
