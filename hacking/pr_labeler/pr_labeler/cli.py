# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: GPL-3.0-or-later

"""
CLI entrypoints
"""

from __future__ import annotations

import typer

from .actions import (
    add_label_if_new,
    handle_codeowner_labels,
    new_contributor_welcome,
    no_body_nag,
    warn_porting_guide_change,
)
from .cli_context import GlobalArgs, IssueLabelerCtx, PRLabelerCtx
from .constants import OWNER, REPO
from .github_utils import get_event_info, get_repo
from .utils import log

APP = typer.Typer()


@APP.callback()
def cb(
    *,
    click_ctx: typer.Context,
    owner: str = OWNER,
    repo: str = REPO,
    use_author_association: bool = False,
):
    """
    Basic triager for ansible/ansible-documentation
    """
    click_ctx.obj = GlobalArgs(owner, repo, use_author_association)


@APP.command(name="pr")
def process_pr(
    *,
    click_ctx: typer.Context,
    pr_number: int,
    dry_run: bool = False,
    authed_dry_run: bool = False,
    force_process_closed: bool = False,
) -> None:
    global_args = click_ctx.ensure_object(GlobalArgs)

    authed = not dry_run
    if authed_dry_run:
        dry_run = True
        authed = True

    gclient, repo = get_repo(global_args.full_repo, authed)
    pr = repo.get_pull(pr_number)
    ctx = PRLabelerCtx(
        client=gclient,
        repo=repo,
        pr=pr,
        dry_run=dry_run,
        event_info=get_event_info(),
        issue=pr.as_issue(),
        global_args=global_args,
    )
    if not force_process_closed and pr.state != "open":
        log(ctx, "Refusing to process closed ticket")
        return

    handle_codeowner_labels(ctx)
    new_contributor_welcome(ctx)
    no_body_nag(ctx)
    warn_porting_guide_change(ctx)


@APP.command(name="issue")
def process_issue(
    *,
    click_ctx: typer.Context,
    issue_number: int,
    dry_run: bool = False,
    authed_dry_run: bool = False,
    force_process_closed: bool = False,
) -> None:
    global_args = click_ctx.ensure_object(GlobalArgs)

    authed = not dry_run
    if authed_dry_run:
        dry_run = True
        authed = True
    gclient, repo = get_repo(global_args.full_repo, authed)
    issue = repo.get_issue(issue_number)
    ctx = IssueLabelerCtx(
        client=gclient,
        repo=repo,
        issue=issue,
        dry_run=dry_run,
        event_info=get_event_info(),
        global_args=global_args,
    )
    if not force_process_closed and issue.state != "open":
        log(ctx, "Refusing to process closed ticket")
        return

    add_label_if_new(ctx, "needs_triage")
    new_contributor_welcome(ctx)
    no_body_nag(ctx)


if __name__ == "__main__":
    APP()
