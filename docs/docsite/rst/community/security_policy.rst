.. _security_policy:

***********************
Ansible Security Policy
***********************

.. contents:: Topics

Our Commitment
==============

Ansible takes security seriously. We are committed to maintaining the highest level of security and trust for our users. We appreciate the security research community's efforts in helping us identify and address vulnerabilities responsibly.

Supported Versions
==================

Only the latest release receives regular security patches. Earlier versions may receive critical fixes on a best-effort basis, but we cannot guarantee back-porting to unsupported versions.

Security Model
==============

Security assumptions and threat model
--------------------------------------

Ansible is designed to [describe intended use]. Users should be aware:

- **Untrusted inputs**: [Describe which inputs are safe/unsafe]
- **Trust boundaries**: [Define what the project does/does not protect against]
- **Safe data formats**: [List formats with strong security track records]
- **Unsafe operations**: [List operations requiring sandboxing or caution]

Reporting a Vulnerability
=========================

How to Report
-------------

Please report security vulnerabilities privately through one of these channels:

**Email**

- Send to: `security@ansible.com <mailto:security@ansible.com>`_

Do **NOT** report security vulnerabilities through:

- Public GitHub issues
- Pull requests
- Ansible Forum
- Ansible Matrix
- Public forums or social media

What to Include
---------------

Please provide the following information:

- **Title**: Clear, descriptive summary
- **Reporter details**: Your name/handle and affiliation (optional)
- **Vulnerability description**: Technical details of the issue
- **Affected versions**:

  - Mandatory: known, affected version
  - Good to have: identification of all affected versions

- **Reproduction steps**: Minimal example to reproduce the issue
- **Impact assessment**: Potential exploit scenarios and severity
- **Suggested fix**: If you have recommendations (optional)
- **Disclosure status**: Whether this has been shared elsewhere

What to Report
--------------

Please report if you have:

- Discovered a potential security vulnerability
- Found an issue but are uncertain about its security impact
- Identified vulnerabilities in dependencies not yet addressed

What NOT to Report
------------------

The following do not qualify as security vulnerabilities:

- Automated scanner output without analysis or reproduction steps
- General support or usage questions
- Requests for help updating to newer versions
- Bugs without security implications
- Issues outside our documented threat model

Response Process
================

Timeline
--------

.. list-table::
   :header-rows: 1
   :widths: auto

   * - Stage
     - Timeframe
   * - Acknowledgment
     - Within 1 business days
   * - Initial assessment
     - Within 60 business days(max)
   * - Resolution target
     - Within 90 business days(max)

Our Process
-----------

1. **Acknowledgment** -- We confirm receipt of your report
2. **Triage** -- We assess validity and severity
3. **Investigation** -- We reproduce and analyze the issue
4. **Fix Development** -- We develop and test a patch
5. **Coordinated Disclosure** -- We coordinate release timing with you
6. **Public Disclosure** -- We publish advisory and credits

Severity Classification
========================

.. list-table::
   :header-rows: 1
   :widths: auto

   * - Level
     - Description
   * - Critical
     - Immediate threat, easy exploitation
   * - High
     - Significant impact
   * - Medium
     - Moderate impact, harder to exploit
   * - Low
     - Limited impact

Disclosure Policy
=================

- We follow coordinated disclosure practices
- Fixes are typically included in the next planned release
- Critical vulnerabilities may warrant out-of-band releases
- Public disclosure occurs via GitHub Security Advisories
- Reporters are credited unless they prefer anonymity

Security Advisories
===================

Published advisories are available at: [link]

- GitHub Security Advisories: [link]
- Ansible Security Page: [link]

Safe Usage Guidelines
=====================

To use Ansible securely:

1. **Keep updated**: Always use supported versions
2. **Validate inputs**: [Specific input validation guidance]
3. **Sandbox untrusted data**: [When sandboxing is needed]
4. **Follow best practices**: [Link to security documentation]

Scope
=====

In Scope
--------

- Core Ansible codebase
- Official packages and distributions
- Documentation that could lead to insecure usage

Out of Scope
------------

- Third-party plugins or extensions
- User-implemented code
- Issues requiring physical access
- Social engineering attacks
- Denial of service through resource exhaustion

Recognition
===========

We thank security researchers who help improve Ansible. Contributors are acknowledged in:

- Security advisories
- CONTRIBUTORS.md
- Ansible forum badge

The ``SECURITY.md`` File
========================

What is ``SECURITY.md``?
------------------------

``SECURITY.md`` is the place where users, developers, security researchers, and the community at large can find information on how to communicate and report a potential vulnerability about a particular repository and the overall Ansible project. The file serves as the first point of reference for security-related inquiries, ensuring that the community has a clear, standardized path for disclosure. By providing transparent contact methods and expectations, it upholds the security ethos and procedural standards defined in this Vulnerability Management Policy.

Where to host ``SECURITY.md``
------------------------------

Host the ``SECURITY.md`` file in the root directory of the GitHub repository, alongside other essential project files like ``README.md`` and ``LICENSE``. This ensures high visibility and automatic integration with GitHub's security features.

Contents of ``SECURITY.md``
-----------------------------

The file **must** contain the following:

- Contact information
- Timeline
- Link to the Vulnerability Management Policy on ``docs.ansible.com``
- What to include in the report

``SECURITY.md`` Template
-------------------------

Use the following template for the ``SECURITY.md`` file in your repository:

.. code-block:: markdown

   # Reporting a Security Vulnerability or Incident

   Please do not report security vulnerabilities or security incidents via public GitHub issues.
   To ensure a coordinated disclosure, submit your findings via email to: `security@ansible.com`

   ## Submission Guidelines

   To help us triage and resolve the issue efficiently, please include the following in your report:

   - **Title**: A concise, descriptive summary of the issue.
   - **Reporter Details**: Your name/handle and affiliation (optional).
   - **Technical Description**: Detailed information regarding the vulnerability.
   - **Affected Versions**: The specific version(s) or range(s) of software tested.
   - **Reproduction Steps**: A minimal, functional example to reproduce the issue.
   - **Impact Assessment**: Potential exploit scenarios and perceived severity.
   - **Suggested Fix**: Any proposed patches or mitigations (optional).
   - **Disclosure Status**: Whether this has been shared with other parties or published and your plan for future sharing (e.g., at a conference).

   ## Response Timeline

   We aim to provide an initial acknowledgment of your report within one business day.

   ## Resolution Timeline

   Our goal is to assess the report, coordinate fix and disclosure as quickly as possible.
   All confirmed security vulnerabilities and incidents will be addressed according to
   severity level and impact on the Ansible Project.

   ## Contact Information

   Direct all security questions and vulnerability reports to:

   - **Email**: security@ansible.com
   - **Ansible Security Policy**: [https://www.ansible.com/security](https://www.ansible.com/security)

   ## EU Cyber Resilience Act — Open-Source Steward Statement

   This project is stewarded by Red Hat, Inc., an open source software steward as defined
   in Article 3(14) of the EU Cyber Resilience Act (Regulation 2024/2847).

   - **Contact**: cra-steward@redhat.com

Policy Updates
==============

This policy may be updated periodically. Suggestions for improvement can be submitted via issues or pull requests.
