# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import dataclasses
import os
from collections.abc import Collection
from functools import cached_property
from pathlib import Path
from typing import Union

import github
import github.Auth
import github.Issue
import github.PullRequest
import github.Repository
import typer
from codeowners import CodeOwners, OwnerTuple

OWNER = "ansible"
REPO = "ansible-documentation"
LABELS_BY_CODEOWNER: dict[OwnerTuple, list[str]] = {
    ("TEAM", "@ansible/steering-committee"): ["sc_approval"],
}
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CODEOWNERS = (ROOT / ".github/CODEOWNERS").read_text("utf-8")

IssueOrPrCtx = Union["IssueLabelerCtx", "PRLabelerCtx"]
IssueOrPr = Union["github.Issue.Issue", "github.PullRequest.PullRequest"]


# TODO: If we end up needing to log more things with more granularity,
# switch to something like `logging`
def log(ctx: IssueOrPrCtx, *args: object) -> None:
    print(f"{ctx.member.number}:", *args)


def get_repo(authed: bool = True) -> tuple[github.Github, github.Repository.Repository]:
    gclient = github.Github(
        auth=github.Auth.Token(os.environ["GITHUB_TOKEN"]) if authed else None,
    )
    repo = gclient.get_repo(f"{OWNER}/{REPO}")
    return gclient, repo


@dataclasses.dataclass()
class LabelerCtx:
    client: github.Github
    repo: github.Repository.Repository
    dry_run: bool

    @property
    def member(self) -> IssueOrPr:
        raise NotImplementedError

    @cached_property
    def previously_labeled(self) -> frozenset[str]:
        labels: set[str] = set()
        events = (
            self.member.get_events()
            if isinstance(self.member, github.Issue.Issue)
            else self.member.get_issue_events()
        )
        for event in events:
            if event.event in ("labeled", "unlabeled"):
                assert event.label
                labels.add(event.label.name)
        return frozenset(labels)


@dataclasses.dataclass()
class IssueLabelerCtx(LabelerCtx):
    issue: github.Issue.Issue

    @property
    def member(self) -> IssueOrPr:
        return self.issue


@dataclasses.dataclass()
class PRLabelerCtx(LabelerCtx):
    pr: github.PullRequest.PullRequest

    @property
    def member(self) -> IssueOrPr:
        return self.pr


def create_comment(ctx: IssueOrPrCtx, body: str) -> None:
    if ctx.dry_run:
        return
    if isinstance(ctx, IssueLabelerCtx):
        ctx.issue.create_comment(body)
    else:
        ctx.pr.create_issue_comment(body)


def get_data_file(name: str) -> str:
    """
    Get a data file
    """
    return (HERE / "data" / name).read_text("utf-8")


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


def new_contributor_welcome(ctx: IssueOrPrCtx) -> None:
    """
    Welcome a new contributor to the repo with a message and a label
    """
    # This contributor has already been welcomed!
    if "new_contributor" in ctx.previously_labeled:
        return
    log(ctx, "author_association is", ctx.member.raw_data["author_association"])
    if ctx.member.raw_data["author_association"] not in {
        "FIRST_TIMER",
        "FIRST_TIME_CONTRIBUTOR",
    }:
        return
    log(ctx, "Welcoming new contributor")
    add_label_if_new(ctx, "new_contributor")
    create_comment(ctx, get_data_file("docs_team_info.md"))


APP = typer.Typer()


@APP.callback()
def cb():
    """
    Basic triager for ansible/ansible-documentation
    """


@APP.command(name="pr")
def process_pr(
    pr_number: int, dry_run: bool = False, authed_dry_run: bool = False
) -> None:
    authed = not dry_run
    if authed_dry_run:
        dry_run = True
        authed = True
    gclient, repo = get_repo(authed=authed)
    pr = repo.get_pull(pr_number)
    ctx = PRLabelerCtx(client=gclient, repo=repo, pr=pr, dry_run=dry_run)
    if pr.state != "open":
        log(ctx, "Refusing to process closed ticket")
        return

    handle_codeowner_labels(ctx)
    add_label_if_new(ctx, "needs_triage")
    new_contributor_welcome(ctx)


@APP.command(name="issue")
def process_issue(
    issue_number: int, dry_run: bool = False, authed_dry_run: bool = False
) -> None:
    authed = not dry_run
    if authed_dry_run:
        dry_run = True
        authed = True
    gclient, repo = get_repo(authed=authed)
    issue = repo.get_issue(issue_number)
    ctx = IssueLabelerCtx(client=gclient, repo=repo, issue=issue, dry_run=dry_run)
    if issue.state != "open":
        log(ctx, "Refusing to process closed ticket")
        return

    add_label_if_new(ctx, "needs_triage")
    new_contributor_welcome(ctx)


if __name__ == "__main__":
    APP()
