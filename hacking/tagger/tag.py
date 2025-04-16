#!/usr/bin/env python3

# Copyright (C) 2024 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: GPL-3.0-or-later
# GNU General Public License v3.0+
# (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Script to handle tagging versions in the ansible-documentation repo in sync
with ansible-core.
"""

from __future__ import annotations

import datetime
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from string import Template
from types import SimpleNamespace
from typing import Any, List, NamedTuple, NoReturn, Optional

import click
import git
import git.objects.util
import typer

from packaging.version import Version

MESSAGE = Template(
    """\
${version_str}

This tag contains a snapshot of the ansible-documentation ${branch} branch
at the time of the ansible-core ${version_str} release.
"""
)
# hacking/tagger
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent

DEFAULT_ANSIBLE_CORE_CHECKOUT = ROOT.parent.joinpath("ansible")
DEFAULT_REMOTE = "origin"
DEFAULT_ACTIVE_BRANCHES: tuple[str, ...] = (
    "stable-2.16",
    "stable-2.17",
    "stable-2.18",
    "stable-2.19",
)


def get_tags(repo: git.Repo) -> list[str]:
    """
    Args:
        repo:
            A repo object
    Returns:
        A list of tag names as strings
    """
    return [tag.name.removeprefix("refs/tags/") for tag in repo.tags]


def filter_tags(tags: Iterable[str], major_minor: str) -> dict[str, Version]:
    """
    Args:
        tags:
            Iterable of tag names as strings
        major_minor:
            `{version.major}.{version.minor}` of an ansible-core branch
    Returns:
        Sorted (newest->oldest) dict of tag names that are part of
        `major_minor` mapped to parsed `packaging.version.Version`s
    """
    tags = {
        tag: Version(stripped)
        for tag in tags
        if (stripped := tag.lstrip("v")).startswith(major_minor)
    }
    return dict(sorted(tags.items(), reverse=True, key=lambda x: x[1]))


def get_tag_datetime(tag: git.TagReference) -> datetime.datetime:
    """
    Args:
        tag:
            Lightweight tag reference
    Returns:
        A `datetime.datetime` of the tagged date or the committed date for a
        non-annotated tag
    """
    if tag.tag:
        return git.objects.util.from_timestamp(
            tag.tag.tagged_date, tag.tag.tagger_tz_offset
        )
    return tag.commit.committed_datetime


def _get_last_commit_before(
    commits: Iterable[git.objects.Commit], before: datetime.datetime
) -> git.objects.Commit:
    for commit in commits:
        if commit.committed_datetime <= before:
            return commit
    raise ValueError("No commit found!")


def get_last_hash(
    docs_repo: git.Repo, core_tag: git.TagReference, branch: str, remote: str
) -> str:
    """
    Get the last commit before the datetime of ansible-core's release of TAG.

    Args:
        docs_repo:
            ansible-documentation `git.Repo` object
        core_tag:
            `git.TagReference` for the corresponding tag in ansible-core
        branch:
            Branch name in which to search for the properly timed commit

    Returns:
        Commit hash

    Raises:
        ValueError:
            No commit was found before the datetime of ansible-core's release of TAG
    """
    return _get_last_commit_before(
        commits=docs_repo.iter_commits(f"{remote}/{branch}", first_parent=True),
        before=get_tag_datetime(core_tag),
    )


def get_branch(tag_name: str, /) -> str:
    """
    Determine a `stable-XX.XX` branch name based on `tag_name`
    """
    version = Version(tag_name.lstrip("v"))
    major_minor = f"{version.major}.{version.minor}"
    return "stable-" + major_minor


def v_prefix_tag(name: str, /) -> str:
    """
    Ensure a tag/version has a `v` prefix
    """
    return "v" + name.lstrip("v")


# START: typer CLI code

app = typer.Typer()


def fatal(__msg: object, /, *, returncode: int = 1) -> NoReturn:
    typer.secho(f"! {__msg}", err=True, fg="red")
    raise typer.Exit(returncode)


def msg(__msg: object, not_on_quiet: bool = True, /, **kwargs: Any) -> None:
    if not_on_quiet:
        try:
            quiet = click.get_current_context().ensure_object(Args).quiet
        except Exception:
            quiet = False
        if quiet:
            return
    kwarg: dict[str, Any] = {"err": True, "fg": "blue"} | kwargs
    typer.secho(f"* {__msg}", **kwarg)


@dataclass(kw_only=True)
class Args:
    """
    Context for global arguments
    """

    docs_repo_path: Path
    docs_repo: git.Repo
    docs_remote: str
    core_repo_path: Path
    core_repo: git.Repo
    core_remote: str
    quiet: bool


def ensure_tag(tag: git.TagReference) -> None:
    """
    Ensure a `git.TagReference` actually object
    """
    try:
        _ = tag.object
    except ValueError:
        name = tag.name.removeprefix("refs/tags/")
        fatal(f"Tag {name} does not exist in core!")


def get_new_tags(args: Args, branch: str) -> dict[str, Version]:
    """
    Returns:
        Sorted (newest->oldest) dict of new tag names mapped to parsed
        `packaging.version.Version`s
    """
    core_tags, our_tags = get_tags(args.core_repo), get_tags(args.docs_repo)
    core_filtered_tags = filter_tags(core_tags, branch.removeprefix("stable-"))
    our_filtered_tags = filter_tags(our_tags, branch.removeprefix("stable-"))
    missing_tags: dict[str, Version] = {}
    for tag, version in core_filtered_tags.items():
        if tag in our_filtered_tags:
            break
        missing_tags[tag] = version
    return missing_tags


class BranchTagRef(NamedTuple):
    branch: str
    tag: str
    ref: str


def branch_tag_ref(
    args: Args, branch: str | None, tag: str, ref: str | None
) -> BranchTagRef:
    tag = v_prefix_tag(tag)
    branch = branch or get_branch(tag)
    core_tag = args.core_repo.tag(tag)
    ensure_tag(core_tag)
    if not ref:
        ref = get_last_hash(args.docs_repo, core_tag, branch, args.docs_remote)
    return BranchTagRef(branch, tag, ref)


def create_tag(
    args: Args, branch: str, tag: str, ref: str, *, push: bool
) -> git.TagReference:
    """
    Create and push a tag with the proper message

    Args:
        args:
            CLI context `Args` object
        branch:
            Branch name
        tag:
            Tag name
        ref:
            Reference to tag
    """
    message = MESSAGE.substitute(version_str=tag.lstrip("v"), branch=branch)
    msg(f"Tagging {ref} as {tag}")
    tag_ref = git.TagReference.create(args.docs_repo, tag, ref, message)
    if push:
        print(f"Pushing {tag} to {args.docs_remote}")
        args.docs_repo.remote(args.docs_remote).push(tag)
    return tag_ref


PARAMS = SimpleNamespace(
    branches=typer.Option(
        None,
        "-b",
        "--branch",
        help="Branches in which to search for tags."
        " Can be specified multiple times."
        f" Defaults to {DEFAULT_ACTIVE_BRANCHES}",
    ),
    branch=typer.Option(
        None,
        "-b",
        "--branch",
        help="Branch name. Autodetect based on --tag by deafult.",
    ),
    tag_required=typer.Option(
        ...,
        "-t",
        "--tag",
        help="Tag name",
    ),
    ref=typer.Option(
        ...,
        "-r",
        "--ref",
        help="Tag reference",
    ),
)


@app.callback(help=__doc__)
def callback(
    ctx: typer.Context,
    docs_repo_path: Path = typer.Option(
        ROOT,
        "--docs",
        help="Path to ansible-documentation checkout",
        dir_okay=True,
        file_okay=False,
        exists=True,
    ),
    core_repo_path: Path = typer.Option(
        DEFAULT_ANSIBLE_CORE_CHECKOUT,
        "--core",
        help="Path to core checkout",
        dir_okay=True,
        file_okay=False,
        exists=True,
    ),
    remote: Optional[str] = typer.Option(
        None,
        help="Git Remote name for ansible-core and ansible-documentation checkouts."
        f" Default: {DEFAULT_REMOTE}",
    ),
    core_remote: Optional[str] = typer.Option(
        None, help="Override remote name for core checkout"
    ),
    docs_remote: Optional[str] = typer.Option(
        None, help="Override remote name for docs checkout"
    ),
    fetch: bool = typer.Option(True, help="Whether to fetch repos"),
    quiet: bool = typer.Option(False, help="Silence logging"),
):
    """
    Process global CLI arguments and create a context object to store them
    """
    core_remote = core_remote or remote or DEFAULT_REMOTE
    docs_remote = docs_remote or remote or DEFAULT_REMOTE
    docs_repo = git.Repo(docs_repo_path)
    core_repo = git.Repo(core_repo_path)
    args = Args(
        docs_repo_path=docs_repo_path,
        docs_repo=docs_repo,
        docs_remote=docs_remote,
        core_repo_path=core_repo_path,
        core_repo=core_repo,
        core_remote=core_remote,
        quiet=quiet,
    )
    ctx.obj = args
    if fetch:
        fetch_all(args)


def fetch_all(args: Args) -> None:
    remotes = {
        "docs": (args.docs_repo, args.docs_remote),
        "core": (args.core_repo, args.core_remote),
    }
    for name, (repo, cur_remote) in remotes.items():
        msg(f"Fetching {cur_remote} from {name} repo...")
        repo.remote(cur_remote).fetch()


@app.command(name="new-tags")
def new_tags_command(
    ctx: typer.Context, branches: Optional[List[str]] = PARAMS.branches
) -> None:
    """
    List new tags in ansible-core that are not tagged here
    """
    args = ctx.ensure_object(Args)
    branches = branches or list(DEFAULT_ACTIVE_BRANCHES)
    missing_tags = [tag for branch in branches for tag in get_new_tags(args, branch)]
    if missing_tags:
        print("\n".join(missing_tags))
    ctx.exit(0 if missing_tags else 1)


@app.command(name="hash")
def hash_command(
    ctx: typer.Context,
    tag: str = PARAMS.tag_required,
    branch: Optional[str] = PARAMS.branch,
) -> None:
    """
    Get the last commit hash before the datetime of ansible-core's release of TAG.
    """
    args = ctx.ensure_object(Args)
    _, _, ref = branch_tag_ref(args, branch, tag, None)
    print(ref)


@app.command(name="mantag")
def mantag_command(
    ctx: typer.Context,
    tag: str = PARAMS.tag_required,
    ref: str = PARAMS.ref,
    branch: Optional[str] = PARAMS.branch,
    push: bool = True,
) -> None:
    """
    Manually tag a release
    """
    args = ctx.ensure_object(Args)
    triplet = branch_tag_ref(args, branch, tag, ref)
    create_tag(args, *triplet, push=push)


@app.command(name="tag")
def tag_command(
    ctx: typer.Context,
    branches: Optional[List[str]] = PARAMS.branches,
    push: bool = True,
):
    """
    Determine the missing ansible-core releases from `--branch`, create
    corresponding tags for each release in the ansible-documentation repo, and
    push them.
    """
    args = ctx.ensure_object(Args)
    branches = branches or list(DEFAULT_ACTIVE_BRANCHES)
    triplets: list[BranchTagRef] = [
        branch_tag_ref(args, branch, tag, None)
        for branch in branches
        for tag in get_new_tags(args, branch)
    ]

    for triplet in triplets:
        create_tag(args, *triplet, push=push)


if __name__ == "__main__":
    app()
