.. _secure_development_practices:

****************************
Secure development practices
****************************

.. contents::
   :local:

This page indexes secure development practices for Ansible projects.
Follow the linked documentation for full details.

For vulnerability reporting and disclosure processes, see the :ref:`security_policy` and the :ref:`vulnerability_management_policy`.
For the complete :ref:`developer_guide`, see the Ansible developer documentation.

Secure module and plugin development
=====================================

Follow these guidelines when developing Ansible modules and plugins to avoid common security pitfalls.

* :ref:`module_conventions` covers secure command execution (``run_command`` instead of ``subprocess``), masking sensitive data with ``no_log``, and input validation.
* :ref:`argument_spec` covers defining and validating module arguments to enforce type safety and reject unexpected input.
* :ref:`module_utils` documents secure utilities including ``fetch_url`` for TLS-verified HTTP requests and ``run_command`` for safe shell execution.
* :ref:`developing_modules_best_practices` covers conventions for error handling, return values, and idempotent operations.
* :ref:`developing_plugins` covers plugin development guidelines for all plugin types.
* :ref:`developing_secret_masking` covers registering secrets so they are masked in Ansible output, marking plugin options as ``secret``, and callback plugin responsibilities.

Secure collections
==================

* :ref:`developing_collections` covers collection development, including namespace requirements and packaging.
* :ref:`collection_structure` documents the required file structure for collections.

Secure playbooks and roles
==========================

* :ref:`vault_guide_index` covers encrypting sensitive data such as passwords, keys, and credentials with Ansible Vault.

Dependency management
=====================

See `GitHub supply chain security <https://docs.github.com/en/code-security/supply-chain-security>`__ for background on dependency graphs, advisories, and SBOM generation.

* Integrate automated vulnerability scanning (such as `Dependabot <https://docs.github.com/en/code-security/dependabot>`__) into CI/CD pipelines.
* Pin dependencies by hash in build and release pipelines to prevent supply-chain substitution attacks.
* Maintain a Software Bill of Materials (SBOM) for all released artifacts.
* Address Critical and High severity dependency vulnerabilities within the same timelines as first-party code.

GitHub workflow security
========================

See `Security hardening for GitHub Actions <https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions>`__ for the full GitHub guide on securing workflows.

* Pin GitHub Actions by commit SHA, not by mutable tag, to prevent supply-chain attacks through compromised actions.
* Use restricted permissions (least privilege) on workflow tokens by setting explicit ``permissions:`` blocks.
* Configure `GitHub Rulesets <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets>`_ (replacement for branch protections) and mandatory code review on all release branches.

Build and release integrity
===========================

See `GitHub artifact attestations <https://docs.github.com/en/actions/security-for-github-actions/using-artifact-attestations>`__ for GitHub's built-in SLSA provenance support.

* Follow `SLSA Level 1 or higher <https://slsa.dev/spec/v1.0/levels>`__ practices for build artifact provenance.
* Execute builds in hosted, ephemeral environments and generate provenance metadata alongside artifacts.
* Sign all releases with project-controlled keys.
* Collections should be built using automation, such as GitHub Actions or Zuul, and triggered by Git tag events. Do not build manually.
* Enable `GitHub immutable releases <https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases>`_.

Project security posture
========================

* Maintain a ``SECURITY.md`` file in the root directory of all project repositories documenting the vulnerability reporting process.
  Use the `SECURITY.md template <https://github.com/ansible-community/project-template/blob/main/SECURITY.md>`__ from the ``ansible-community/project-template`` repository.
* Pursue `OpenSSF Best Practices Badge <https://openssf.org/projects/best-practices-badge/>`__ certification for ansible-core and key collections.
* Run `OpenSSF Scorecard <https://openssf.org/projects/scorecard/>`__ regularly and address findings to maintain a strong security posture.
* Follow the `OpenSSF CRA Readiness Guide <https://best.openssf.org/CRA-Brief-Guide-for-OSS-Developers>`__ for practical security practices aligned with the EU Cyber Resilience Act.

Community
=========

For discussion about the EU Cyber Resilience Act and how it applies to the Ansible ecosystem, see the `CRA tag on Ansible Forum <https://forum.ansible.com/tag/cra>`__.

To follow changes and suggest improvements to Ansible security practices, see the `infra-and-security tag on Ansible Forum <https://forum.ansible.com/tag/infra-and-security>`__.
