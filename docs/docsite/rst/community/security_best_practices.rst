.. _security_best_practices:

*************************
Security Best Practices
*************************

.. contents:: Topics

The following controls reduce the attack surface and limit the impact of vulnerabilities in deployed Ansible environments. While enforcement of these controls is the responsibility of operators, this policy documents them as recommended baselines.

Access Control
==============

- **Minimize administrative accounts.** Restrict root, superuser, and AWX administrator access to essential personnel only.
- **Enforce least privilege.** Use Role-Based Access Control (RBAC) to grant the minimum permissions required for each role.
- **Use Teams for group-based permissions** rather than individual user grants.
- **Leverage external authentication** (LDAP, SAML 2.0, OAuth) to centralize identity management and reduce manual errors.

Credential Management
=====================

- Store credentials **exclusively within AWX/Controller** credential stores -- never in playbooks, inventory files, or version control.
- **Restrict credential use** to specific network addresses where possible.
- **Separate credentials by function** (for example, patching credentials vs. application deployment credentials) to limit blast radius and enable granular auditing.
- Enforce **password complexity policies** (minimum 9 characters, no common passwords, no user-attribute reuse).

Network and Platform Hardening
==============================

- **Do not expose** AWX or Automation Controller directly to the public internet.
- **Maintain SELinux** in enforcing mode on all control plane hosts.
- **Enable AWX's multi-tenant containment** to isolate job execution environments.
- Treat playbooks, inventory, and credentials as **source of truth once launched** -- enforce all security controls (code review, approval workflows, source control) before automation execution.

Monitoring and Logging
======================

- Deploy **centralized logging** (Elastic Stack, Splunk, Sumologic, or equivalent) rather than relying on local log review.
- Monitor the **AWX Activity Stream** for all administrative and configuration changes.
- Retain security-relevant logs for a minimum of **12 months** in accordance with organizational retention policies.
- Alert on anomalous activity: unexpected credential usage, privilege escalation attempts, and configuration changes outside maintenance windows.

Secure Development and Software Supply Chain Integrity Practices
================================================================

To ensure overall quality and to meet expectations of our users, open source repositories under the Ansible Project umbrella are encouraged to follow good secure development practices. Consider applying at least those measures.

Dependency Management
---------------------

- Maintain a **Software Bill of Materials (SBOM)** for all released artifacts.
- **Pin dependencies by hash** in build and release pipelines to prevent supply-chain substitution attacks.
- Integrate **automated vulnerability scanning** (for example, Dependabot, or equivalent) into CI/CD pipelines.
- Monitor dependency health metrics and **address Critical/High severity dependency vulnerabilities** within the same timelines as first-party code.

Build and Release Integrity
----------------------------

- Follow **SLSA Level 1 or higher** practices for build artifact provenance:

  - Builds are executed in hosted, ephemeral environments.
  - Build provenance metadata is generated and distributed alongside artifacts.

- All releases are **signed** with project-controlled keys.
- Enable **branch protection and mandatory code review** on all release branches.

Project Security Posture
-------------------------

- Maintain a **SECURITY.md** file in all project repositories documenting the vulnerability reporting process.
- Pursue `OpenSSF Best Practices Badge <https://openssf.org/projects/best-practices-badge/>`__ certification for ansible-core and key collections.
- Run tools like `OpenSSF Scorecard <https://openssf.org/projects/scorecard/>`__ regularly and address findings to maintain a strong security posture.

Other Secure Practices
-----------------------

There are many great materials and frameworks for open source maintainers to achieve and support the good security posture in the most meaningful and developer-friendly way, including tools and automation recommendations, educational materials, and templates. One example is `OpenSSF Best Practices <https://openssf.org/resources/guides/>`__.

Consider following the `OpenSSF CRA Readiness Guide for Maintainers and Developers <https://best.openssf.org/CRA-Brief-Guide-for-OSS-Developers>`__. It is in fact not just a voluntary compliance checklist, but also makes sense from the software development and open source security practices that are widely recognized as good engineering and security hygiene. Implementing those practices and documenting them sends a healthy signal to Ansible downstream users.
