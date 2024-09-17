# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: GPL-3.0-or-later

"""
CLI context objects
"""

from __future__ import annotations

import dataclasses
from functools import cached_property
from typing import TYPE_CHECKING, Any, ClassVar

import github
import github.Issue
import github.PullRequest
import github.Repository

if TYPE_CHECKING:
    from typing_extensions import TypeAlias

    from .github_utils import IssueOrPr

IssueOrPrCtx: TypeAlias = "IssueLabelerCtx | PRLabelerCtx"


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
