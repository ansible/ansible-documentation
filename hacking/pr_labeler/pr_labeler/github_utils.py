# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Utilities for working with the Github API
"""

from __future__ import annotations

import json
import os
from contextlib import suppress
from typing import TYPE_CHECKING, Any

import github
import github.Auth
import github.Issue
import github.PullRequest
import github.Repository

from .cli_context import IssueLabelerCtx, IssueOrPrCtx
from .utils import log

if TYPE_CHECKING:
    from typing_extensions import TypeAlias


IssueOrPr: TypeAlias = "github.Issue.Issue | github.PullRequest.PullRequest"


def get_repo(
    full_repo: str,
    authed: bool = True,
) -> tuple[github.Github, github.Repository.Repository]:
    """
    Create a Github client and return a `github.Repository.Repository` object

    Args:
        full_repo: OWNER/NAME of the repository
        authed:
            Whether to create an authenticated Github client with the
            `$GITHUB_TOKEN` environment variable as the key
    """
    gclient = github.Github(
        auth=github.Auth.Token(os.environ["GITHUB_TOKEN"]) if authed else None,
    )
    repo_obj = gclient.get_repo(full_repo)
    return gclient, repo_obj


def get_event_info() -> dict[str, Any]:
    """
    Load Github event JSON data from `$event_data`
    """
    event_json = os.environ.get("event_json")
    if not event_json:
        return {}
    with suppress(json.JSONDecodeError):
        return json.loads(event_json)
    return {}


# Operations


def get_team_members(ctx: IssueOrPrCtx, team: str) -> list[str]:
    """
    Get the members of a Github team
    """
    return [
        user.login
        for user in ctx.client.get_organization(ctx.repo.organization.login)
        .get_team_by_slug(team)
        .get_members()
    ]


def create_comment(ctx: IssueOrPrCtx, body: str) -> None:
    if ctx.dry_run:
        return
    if isinstance(ctx, IssueLabelerCtx):
        ctx.issue.create_comment(body)
    else:
        ctx.pr.create_issue_comment(body)


def is_new_contributor_assoc(ctx: IssueOrPrCtx) -> bool:
    """
    Determine whether a user has previously contributed.
    Requires authentication as a regular user and does not work with an app
    token.
    """
    author_association = ctx.event_member.get(
        "author_association", ctx.member.raw_data["author_association"]
    )
    log(ctx, "author_association is", author_association)
    return author_association in {"FIRST_TIMER", "FIRST_TIME_CONTRIBUTOR"}


def is_new_contributor_manual(ctx: IssueOrPrCtx) -> bool:
    """
    Determine whether a user has previously opened an issue or PR in this repo
    without needing special API access.
    """
    query_data = {
        "repo": "ansible/ansible-documentation",
        "author": ctx.issue.user.login,
        # Avoid potential race condition where a new contributor opens multiple
        # PRs or issues at once.
        # Better to welcome twice than not at all.
        "is": "closed",
    }
    issues = ctx.client.search_issues("", **query_data)
    for issue in issues:
        if issue.number != ctx.issue.number:
            return False
    return True
