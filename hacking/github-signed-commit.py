#!/usr/bin/env python
"""Create a signed commit via the GitHub API and push it to a branch.

Commits created via the API are automatically signed by GitHub,
producing a Verified badge on the commit.

Usage:
    # Commit all staged files (no --files filter):
    python github_signed_commit.py \\
        --repo ansible/ansible-documentation \\
        --branch deps/update-pins \\
        --base-branch main \\
        --message "chore: refresh pinned dependencies"

    # Create a new branch (or fail if it already exists):
    python github_signed_commit.py \\
        --repo ansible/ansible-documentation \\
        --branch deps/update-pins \\
        --base-branch main \\
        --message "chore: refresh pinned dependencies" \\
        --files "tests/*.txt"

    # Force-update an existing branch:
    python github_signed_commit.py \\
        --repo ansible/ansible-documentation \\
        --branch deps/update-pins \\
        --base-branch main \\
        --message "chore: refresh pinned dependencies" \\
        --files "tests/*.txt" \\
        --force

Requires the GITHUB_TOKEN environment variable to be set.
"""

from __future__ import annotations

import argparse
import glob
import os
import pathlib
import subprocess

from github import Auth, Github
from github.GithubException import GithubException
from github.InputGitTreeElement import InputGitTreeElement


def get_repo_root() -> pathlib.Path:
    """Return the absolute path of the git repository root."""
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True,
    )
    return pathlib.Path(result.stdout.strip()).resolve()


def get_staged_files(patterns: list[str] | None, repo_root: pathlib.Path) -> list[str]:
    """Return git staged files, optionally filtered by glob patterns.

    When *patterns* is ``None`` all staged files are returned. When patterns
    are provided only staged files matching at least one pattern are included.

    Only files within the repository root are included; paths that escape
    the root (e.g. via '../../') raise ValueError.
    """
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True,
        check=True,
        cwd=repo_root,
    )
    staged = set(result.stdout.strip().splitlines())
    if not staged:
        return []

    if patterns is None:
        for path in staged:
            resolved = (repo_root / path).resolve()
            if not resolved.is_relative_to(repo_root):
                raise ValueError(
                    f"File path escapes repository root: {path!r} → {resolved}"
                )
        return sorted(staged)

    matched = []
    for pattern in patterns:
        for path in glob.glob(pattern, recursive=True):
            resolved = pathlib.Path(path).resolve()
            if not resolved.is_relative_to(repo_root):
                raise ValueError(
                    f"File path escapes repository root: {path!r} → {resolved}"
                )
            if path in staged:
                matched.append(path)
    return matched


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "--repo", required=True, help="owner/repo (e.g. ansible/ansible-documentation)"
    )
    p.add_argument("--branch", required=True, help="Branch to push the commit to")
    p.add_argument(
        "--base-branch", required=True, help="Branch the commit should be based on"
    )
    p.add_argument("--message", required=True, help="Commit message")
    p.add_argument(
        "--files",
        required=False,
        default=None,
        help="Glob pattern(s) for files to commit (space-separated). Omit to commit all staged files.",
    )
    p.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force update the branch if it already exists (required to overwrite)",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN environment variable is not set")

    repo_root = get_repo_root()
    patterns = args.files.split() if args.files is not None else None
    files = get_staged_files(patterns, repo_root)
    if not files:
        print("Nothing to commit — no staged files matched the given patterns.")
        return

    print(f"Files to commit: {files}")

    gh = Github(auth=Auth.Token(token))

    try:
        repo = gh.get_repo(args.repo)

        base_branch = repo.get_branch(args.base_branch)
        base_commit = base_branch.commit
        base_tree = base_commit.commit.tree

        # Build the new tree from staged file contents
        tree_elements = [
            InputGitTreeElement(
                path=path,
                mode="100644",
                type="blob",
                content=pathlib.Path(path).read_text(encoding="utf-8"),
            )
            for path in files
        ]
        new_tree = repo.create_git_tree(tree_elements, base_tree)

        # Create the commit — GitHub signs it automatically
        new_commit = repo.create_git_commit(
            args.message, new_tree, [base_commit.commit]
        )
        print(f"Created commit: {new_commit.sha}")

        # Update or create the PR branch
        try:
            ref = repo.get_git_ref(f"heads/{args.branch}")
            if not args.force:
                raise RuntimeError(
                    f"Branch '{args.branch}' already exists. Pass --force to overwrite it."
                )
            ref.edit(new_commit.sha, force=True)
            print(f"Updated branch '{args.branch}' → {new_commit.sha}")
        except GithubException as exc:
            if exc.status != 404:
                raise
            repo.create_git_ref(f"refs/heads/{args.branch}", new_commit.sha)
            print(f"Created branch '{args.branch}' → {new_commit.sha}")

    except GithubException as exc:
        raise RuntimeError(f"GitHub API error {exc.status}: {exc.message}") from exc
    finally:
        gh.close()


if __name__ == "__main__":
    main()
