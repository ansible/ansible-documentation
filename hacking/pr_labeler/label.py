# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import dataclasses
import os
from collections.abc import Collection
from functools import cache
from pathlib import Path

import github
import github.Auth
import github.Repository
import github.PullRequest
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


@dataclasses.dataclass(frozen=True)
class LabelerCtx:
    client: github.Github
    repo: github.Repository.Repository
    pr: github.PullRequest.PullRequest
    dry_run: bool


@cache
def get_previously_labeled(ctx: LabelerCtx) -> frozenset[str]:
    previously_labeled: set[str] = set()
    for event in ctx.pr.get_issue_events():
        if event.event in ("labeled", "unlabeled"):
            assert event.label
            previously_labeled.add(event.label.name)
    return frozenset(previously_labeled)


def handle_codeowner_labels(ctx: LabelerCtx) -> None:
    labels = LABELS_BY_CODEOWNER.copy()
    owners = CodeOwners(CODEOWNERS)
    files = ctx.pr.get_files()
    for file in files:
        for owner in owners.of(file.filename):
            if labels_to_add := labels.pop(owner, None):
                add_label_if_new(ctx, labels_to_add)
        if not labels:
            return


def add_label_if_new(ctx: LabelerCtx, labels: Collection[str] | str) -> None:
    """
    Add a label to a PR if it wasn't added in the past
    """
    labels = {labels} if isinstance(labels, str) else labels
    previously_labeled = get_previously_labeled(ctx)
    print(f"Adding labels to {ctx.pr.number}:", *map(repr, labels))
    if not ctx.dry_run:
        ctx.pr.add_to_labels(*(set(labels) - previously_labeled))


APP = typer.Typer()


@APP.callback()
def cb():
    """
    Basic triager for ansible/ansible-documentation
    """


@APP.command()
def pr(pr_number: int, dry_run: bool = False) -> None:
    gclient = github.Github(
        auth=None if dry_run else github.Auth.Token(os.environ["GITHUB_TOKEN"]),
    )
    repo = gclient.get_repo(f"{OWNER}/{REPO}")
    pr = repo.get_pull(pr_number)
    if pr.state != "open":
        print("Refusing to process closed ticket")
        return
    ctx = LabelerCtx(gclient, repo, pr, dry_run)
    handle_codeowner_labels(ctx)
    add_label_if_new(ctx, "needs_triage")


if __name__ == "__main__":
    APP()
