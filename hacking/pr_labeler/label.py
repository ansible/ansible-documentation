# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import os
from pathlib import Path

import github
import github.Auth
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


def handle_codeowner_labels(pr: github.PullRequest.PullRequest) -> None:
    labels = LABELS_BY_CODEOWNER.copy()
    owners = CodeOwners(CODEOWNERS)
    files = pr.get_files()
    for file in files:
        for owner in owners.of(file.filename):
            if labels_to_add := labels.pop(owner, None):
                print("Adding labels to", f"{pr.id}:", *map(repr, labels_to_add))
                pr.add_to_labels(*labels_to_add)
        if not labels:
            return


APP = typer.Typer()


@APP.callback()
def cb():
    """
    Basic triager for ansible/ansible-documentation
    """


@APP.command()
def pr(pr_number: int) -> None:
    gclient = github.Github(auth=github.Auth.Token(os.environ["GITHUB_TOKEN"]))
    repo = gclient.get_repo(f"{OWNER}/{REPO}")
    pr = repo.get_pull(pr_number)
    if pr.state != "open":
        print("Refusing to process closed ticket")
        return
    handle_codeowner_labels(pr)


if __name__ == "__main__":
    APP()
