# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import dataclasses
import json
import os
import re
from collections.abc import Callable, Collection
from contextlib import suppress
from functools import cached_property
from pathlib import Path
from typing import Any, ClassVar, Union

import github
import github.Auth
import github.Issue
import github.PullRequest
import github.Repository
import typer
from codeowners import CodeOwners, OwnerTuple
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape

OWNER = "ansible"
REPO = "ansible-documentation"
LABELS_BY_CODEOWNER: dict[OwnerTuple, list[str]] = {
    ("TEAM", "@ansible/steering-committee"): ["sc_approval"],
}
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CODEOWNERS = (ROOT / ".github/CODEOWNERS").read_text("utf-8")
JINJA2_ENV = Environment(
    loader=FileSystemLoader(HERE / "data"),
    autoescape=select_autoescape(),
    trim_blocks=True,
    undefined=StrictUndefined,
)
NEW_CONTRIBUTOR_LABEL = "new_contributor"

IssueOrPrCtx = Union["IssueLabelerCtx", "PRLabelerCtx"]
IssueOrPr = Union["github.Issue.Issue", "github.PullRequest.PullRequest"]


# TODO: If we end up needing to log more things with more granularity,
# switch to something like `logging`
def log(ctx: IssueOrPrCtx, *args: object) -> None:
    print(f"{ctx.member.number}:", *args)


def get_repo(
    args: GlobalArgs, authed: bool = True
) -> tuple[github.Github, github.Repository.Repository]:
    gclient = github.Github(
        auth=github.Auth.Token(os.environ["GITHUB_TOKEN"]) if authed else None,
    )
    repo_obj = gclient.get_repo(args.full_repo)
    return gclient, repo_obj


def get_event_info() -> dict[str, Any]:
    event_json = os.environ.get("event_json")
    if not event_json:
        return {}
    with suppress(json.JSONDecodeError):
        return json.loads(event_json)
    return {}


@dataclasses.dataclass()
class GlobalArgs:
    owner: str
    repo: str
    use_author_association: bool

    @property
    def full_repo(self) -> str:
        return f"{self.owner}/{self.repo}"


@dataclasses.dataclass()
class LabelerCtx:
    client: github.Github
    repo: github.Repository.Repository
    dry_run: bool
    event_info: dict[str, Any]
    issue: github.Issue.Issue
    global_args: GlobalArgs

    TYPE: ClassVar[str]

    @property
    def member(self) -> IssueOrPr:
        raise NotImplementedError

    @property
    def event_member(self) -> dict[str, Any]:
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

    TYPE = "issue"

    @property
    def member(self) -> IssueOrPr:
        return self.issue

    @property
    def event_member(self) -> dict[str, Any]:
        return self.event_info.get("issue", {})


@dataclasses.dataclass()
class PRLabelerCtx(LabelerCtx):
    pr: github.PullRequest.PullRequest

    TYPE = "pull request"

    @property
    def member(self) -> IssueOrPr:
        return self.pr

    @property
    def event_member(self) -> dict[str, Any]:
        return self.event_info.get("pull_request", {})


def create_comment(ctx: IssueOrPrCtx, body: str) -> None:
    if ctx.dry_run:
        return
    if isinstance(ctx, IssueLabelerCtx):
        ctx.issue.create_comment(body)
    else:
        ctx.pr.create_issue_comment(body)


def get_data_file(name: str, **kwargs: Any) -> str:
    """
    Template a data file
    """
    return JINJA2_ENV.get_template(name).render(**kwargs).rstrip("\n")


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


def no_body_nag(ctx: IssueOrPrCtx) -> None:
    """
    Complain if a non-bot user creates a PR or issue without body text
    """
    if ctx.member.user.login.endswith("[bot]") or (ctx.member.body or "").strip():
        return
    create_boilerplate_comment(ctx, "no_body_nag.md")


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

    gclient, repo = get_repo(global_args, authed)
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
    gclient, repo = get_repo(global_args, authed)
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
