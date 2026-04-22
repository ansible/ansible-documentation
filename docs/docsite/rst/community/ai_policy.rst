.. _ai_policy:

******************************************************
Ansible Community Policy for AI-Assisted Contributions
******************************************************

This policy uses the term "AI" to apply to any assistive technology as well as autonomous and semi-autonomous tooling that is generally built using the machine learning approach. Examples of such AI include large language models (LLMs), text or image generators, and agentic systems that are available as a service or trained locally.

This policy applies to the following projects and resources:

1. All public projects under Ansible organizations on code version control platforms such as GitHub. For example, the `ansible <https://github.com/ansible>`_, `ansible-community <https://github.com/ansible-community>`_, `ansible-collections <https://github.com/ansible-collections>`_ organizations.
2. Public communication platforms and channels listed in the :ref:`Ansible communication guide<communication>` such as Ansible Forum, official Matrix channels, and GitHub discussions.

The above projects and resources **MAY have their own AI policies** which MAY expand or be more restrictive than this policy.

For the purposes of this document, "contribution submission" includes, but is not limited to, opening issues, pull requests with code or documentation changes, discussion, making comments, posts and alike.

1. Contributors MUST be real humans and MAY use assistance of AI tools for contributing to the above projects and resources, as long as they take full responsibility for their contributions and follow the principles described in this policy.

2. All contributions assisted by AI tools MUST meet a specific project’s or platform’s standards, conventions and contributing guidelines, including code of conduct and license compliance. This document seeks to clarify tool-specific considerations but in no way replaces the governing documents and good contributing practices.

3. Contributors are fully accountable for the contributions they make with or without AI assistance. This also applies to persons who authorized an action initiated by AI tools.

4. All autonomous contributions submitted by AI tools MAY be rejected by resource maintainers without any justification.

   a. Autonomous actions performed by AI tools used by resource maintainers for validation and automation purposes (for example, automatic releasing, testing, spam filtering, and AI contribution detection) SHOULD be reviewed and manually authorized by the maintainers.

5. The use of AI tools SHOULD be explicitly disclosed by the author when a significant part of the contribution is taken from the AI tools output without significant changes. Grammar, spelling, and stylistic corrections do not need disclosure.

   a. For code contributions, the contributor MAY use a short commit message trailer.
   b. For other contributions, disclosure MAY include a short preamble.
   c. We recommend using the following statement as a disclosure: Assisted-by: followed by any information about the contributor’s use of AI tools that they consider useful to disclose, for example:

      i. Assisted-by: gpt-5.4
      ii. Assisted-by: Opus 4.6
      iii. Assisted-by: locally trained model

Possible policy violations should be reported via ``ansible-community@redhat.com``.

The key words "MAY", "MUST", "MUST NOT", and "SHOULD" in this document are to be interpreted as described in :rfc:`2119`.

This AI policy was adapted from AI policies of other open source projects, including:

* The Fedora Project
* The Linux Foundation
