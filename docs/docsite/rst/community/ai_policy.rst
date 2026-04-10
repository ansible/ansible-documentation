.. _ai_policy:

******************************************************
Ansible Community Policy for AI-Assisted Contributions
******************************************************

This policy applies to the following projects and resources:

1. All projects under Ansible organizations on code version control platforms such as GitHub. For example, the `ansible <https://github.com/ansible>`_, `ansible-community <https://github.com/ansible-community>`_, `ansible-collections <https://github.com/ansible-collections>`_ organizations.
2. All projects which are hosted in third-party organizations and are part of Ansible-related distributions. For example, Ansible collections which are part of the Ansible community package.
3. Communication platforms and channels listed in the :ref:`Ansible communication guide<communication>` such as Ansible Forum, official Matrix channels, and GitHub discussions.

The above projects and resources **MAY have their own AI policies** which MAY expand or be more restrictive, but not contradicting this policy.

For the purposes of this document, "contribution submission" includes, but is not limited to, opening issues, pull requests with code or documentation changes, discussion, making comments, posts and alike.

1. Contributors MUST be real humans and MAY use assistance of AI tools for contributing to the above projects and resources, as long as they take full responsibility for their contributions and follow the principles described in this policy.
2. Contributors are always authors and are fully accountable for the contributions they make with or without AI assistance.

   a. A contributor, including a person who authorized an action initiated by an AI tool, MUST take responsibility for their contributions assisted by AI and AI-initiated actions.

   3. Contributions MUST NOT be submitted by AI agents.

   a. All autonomous contributions submitted by AI tools MAY be rejected by resource maintainers as violating this policy.
   b. An exception to this rule is AI tools usage by the resource maintainers for validation and automation purposes, for example, automatic releasing, testing, spam filtering, AI contribution detection. Such actions MUST be reviewed and manually authorized by resource maintainers.

4. The use of AI tools MUST be explicitly disclosed by the author when a significant part of the contribution is taken from the AI tools output without significant changes. Grammar, spelling, and stylistic corrections do not require disclosure.

   a. For code contributions, the contributor MUST use a commit message trailer.
   b. For other contributions, disclosure MUST include a preamble.
   c. The commit message trailers and preamble SHOULD use the following statement as a disclosure: ``Assisted-by:`` followed by the model name, its version, and tool name (optional), for example:

      i. Assisted-by: gpt-5.4
      ii. Assisted-by: Opus 4.6
      iii. Assisted-by: Claude Code (Opus 4.6)
      iv. Assisted-by: Cursor (Opus 4.6)

5. All contributions assisted by AI tools MUST meet a specific project’s or platform’s standards including code of conduct and license compliance.
6. AI MUST NOT be used as the sole arbiter to make final judgments and decisions on people or their contributions, for example, Code of Conduct matters, project board elections, package content acceptance.
7. This policy does not apply to major AI-driven changes to a specific project’s direction, workflows, codebase, or high-volume automated contributions. Such changes require separate discussion and approval by the leadership of the affected project.

Possible policy violations should be reported via ``ansible-community@redhat.com``.

The key words "MAY", "MUST", "MUST NOT", and "SHOULD" in this document are to be interpreted as described in :rfc:`2119`.

This AI policy was adapted from AI policies of other open source projects, including:

* The Fedora Project
* The Linux Foundation
