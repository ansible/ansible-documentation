#!/usr/bin/env python
"""
Clone relevant portions of ansible-core from ansible/ansible into the current
source tree to facilitate building docs.
"""

from __future__ import annotations

import argparse
import dataclasses
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
DEFAULT_BRANCH = (ROOT / "docs" / "ansible-core-branch.txt").read_text().strip()
DEFAULT_ANSIBLE_CORE_REPO = "https://github.com/ansible/ansible"

KEEP_DIRS = (
    "bin",
    "lib",
    "packaging",
    "test/lib",
)

KEEP_FILES = (
    "MANIFEST.in",
    "pyproject.toml",
    "requirements.txt",
)


@dataclasses.dataclass()
class Args:
    branch: str | None
    repo: str
    check: bool


def parse_args(args: list[str] | None = None) -> Args:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-b",
        "--branch",
        help="Set the branch of ansible-core to clone."
        " Defaults to current branch (%(default)s)",
        default=DEFAULT_BRANCH,
    )
    parser.add_argument(
        "--no-branch",
        help="Checkout the default git branch of --remote."
        " This is useful when cloning a local ansible-core fork",
        dest="branch",
        action="store_const",
        const=None,
    )
    parser.add_argument(
        "--repo",
        help="ansible-core repository to check out. Default: %(default)s",
        default=DEFAULT_ANSIBLE_CORE_REPO,
    )
    parser.add_argument(
        "--check",
        action=argparse.BooleanOptionalAction,
        help="Ensure that the necessary files exist."
        " If they don't clone new ones from ansible-core."
        " Otherwise, leave the existing versions alone.",
    )
    return Args(**vars(parser.parse_args(args)))


def main(args: Args) -> None:
    if (
        args.check
        and all(pathlib.Path(file).is_file() for file in KEEP_FILES)
        and all(pathlib.Path(directory).is_dir() for directory in KEEP_DIRS)
    ):
        print("The necessary core files already exist.")
        print("Run 'nox -e clone-core' without --check to update the core files.")
        return

    with tempfile.TemporaryDirectory() as temp_dir:
        cmd: list[str] = ["git", "clone", args.repo, "--depth=1"]
        if args.branch is not None:
            cmd.append(f"--branch={args.branch}")
        cmd.append(temp_dir)
        subprocess.run(cmd, check=True)

        for keep_dir in KEEP_DIRS:
            src = pathlib.Path(temp_dir, keep_dir)
            dst = pathlib.Path.cwd() / keep_dir

            print(f"Updating {keep_dir!r} ...", file=sys.stderr, flush=True)

            if dst.exists():
                shutil.rmtree(dst)

            shutil.copytree(src, dst, symlinks=True)

            (dst / ".gitignore").write_text("*")

        for keep_file in KEEP_FILES:
            src = pathlib.Path(temp_dir, keep_file)
            dst = pathlib.Path.cwd() / keep_file

            print(f"Updating {keep_file!r} ...", file=sys.stderr, flush=True)

            shutil.copyfile(src, dst)


if __name__ == "__main__":
    main(parse_args())
