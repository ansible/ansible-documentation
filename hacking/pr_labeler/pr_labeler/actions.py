# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Triager action functions
"""

from __future__ import annotations

import re
from collections.abc import Callable, Collection
from typing import TYPE_CHECKING

import github
from codeowners import CodeOwners

from .constants import CODEOWNERS, LABELS_BY_CODEOWNER, NEW_CONTRIBUTOR_LABEL
from .github_utils import (
    create_comment,
    get_team_members,
    is_new_contributor_assoc,
    is_new_contributor_manual,
)
from .jinja import get_data_file
from .utils import log

if TYPE_CHECKING:
    from .cli_context import IssueOrPrCtx, PRLabelerCtx


def create_boilerplate_comment(ctx: IssueOrPrCtx, name: str, **kwargs) -> None:
    """
    Add a boilerplate comment if it hasn't already been added
    """
    tmpl = get_data_file(name, ctx=ctx, **kwargs)
    tmpl_lines = tmpl.splitlines()
    last = tmpl_lines[-1]
    if not (last.startswith("<!--- boilerplate: ") and last.endswith(" --->")):
        raise ValueError(
            "Last line must of the template"
            " must have an identifying boilerplate comment"
        )
    for comment in ctx.issue.get_comments():
        if comment.body.splitlines()[-1] == last:
            log(ctx, name, "boilerplate was already commented")
            return
    msg = f"Templating {name} boilerplate"
    if kwargs:
        msg += f" with {kwargs}"
    log(ctx, msg)
    create_comment(ctx, tmpl)


def add_label_if_new(ctx: IssueOrPrCtx, labels: Collection[str] | str) -> None:
    """
    Add a label to a PR if it wasn't added in the past
    """
    labels = {labels} if isinstance(labels, str) else labels
    labels = set(labels) - ctx.previously_labeled
    if not labels:
        return
    log(ctx, "Adding labels", *map(repr, labels))
    if not ctx.dry_run:
        ctx.member.add_to_labels(*labels)


def handle_codeowner_labels(ctx: PRLabelerCtx) -> None:
    labels = LABELS_BY_CODEOWNER.copy()
    owners = CodeOwners(CODEOWNERS)
    files = ctx.pr.get_files()
    for file in files:
        for owner in owners.of(file.filename):
            if labels_to_add := labels.pop(owner, None):
                add_label_if_new(ctx, labels_to_add)
        if not labels:
            return


def new_contributor_welcome(ctx: IssueOrPrCtx) -> None:
    """
    Welcome a new contributor to the repo with a message and a label
    """
    is_new_contributor: Callable[[IssueOrPrCtx], bool] = (
        is_new_contributor_assoc
        if ctx.global_args.use_author_association
        else is_new_contributor_manual
    )
    if (
        # Contributor has already been welcomed
        NEW_CONTRIBUTOR_LABEL in ctx.previously_labeled
        #
        or not is_new_contributor(ctx)
    ):
        return
    log(ctx, "Welcoming new contributor")
    add_label_if_new(ctx, NEW_CONTRIBUTOR_LABEL)
    create_comment(ctx, get_data_file("docs_team_info.md"))


def warn_porting_guide_change(ctx: PRLabelerCtx) -> None:
    """
    Complain if a non-bot user outside of the Release Management WG changes
    porting_guide
    """
    user = ctx.pr.user.login
    if user.endswith("[bot]"):
        return

    # If the API token does not have permisisons to view teams in the ansible
    # org, fall back to an empty list.
    members = []
    try:
        members = get_team_members(ctx, "release-management-wg")
    except github.UnknownObjectException:
        log(ctx, "Failed to get members of @ansible/release-management-wg")
    if user in members:
        return

    matches: list[str] = []
    for file in ctx.pr.get_files():
        if re.fullmatch(
            # Match community porting guides but not core porting guides
            r"docs/docsite/rst/porting_guides/porting_guide_\d.*.rst",
            file.filename,
        ):
            matches.append(file.filename)
    if not matches:
        return
    create_boilerplate_comment(ctx, "porting_guide_changes.md", changed_files=matches)


def no_body_nag(ctx: IssueOrPrCtx) -> None:
    """
    Complain if a non-bot user creates a PR or issue without body text
    """
    if ctx.member.user.login.endswith("[bot]") or (ctx.member.body or "").strip():
        return
    create_boilerplate_comment(ctx, "no_body_nag.md")
