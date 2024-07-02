from __future__ import annotations

import os
from argparse import ArgumentParser, BooleanOptionalAction
from glob import iglob
from pathlib import Path
from shutil import rmtree, which
from typing import cast

import nox

LINT_FILES: tuple[str, ...] = (
    "hacking/pr_labeler/label.py",
    "hacking/tagger/tag.py",
    "noxfile.py",
    *iglob("docs/bin/*.py"),
)
PINNED = os.environ.get("PINNED", "true").lower() in {"1", "true"}
nox.options.sessions = ("clone-core", "lint", "checkers", "make")


def install(session: nox.Session, *args, req: str, **kwargs):
    if PINNED:
        pip_constraint = f"tests/{req}.txt"
        kwargs.setdefault("env", {})["PIP_CONSTRAINT"] = pip_constraint
        session.log(f"export PIP_CONSTRAINT={pip_constraint!r}")
    session.install("-r", f"tests/{req}.in", *args, **kwargs)


@nox.session
def static(session: nox.Session):
    """
    Run static checkers
    """
    install(session, req="static")
    session.run("ruff", "check", *session.posargs, *LINT_FILES)


@nox.session
def formatters(session: nox.Session):
    """
    Reformat code
    """
    install(session, req="formatters")
    session.run("isort", *session.posargs, *LINT_FILES)
    session.run("black", *session.posargs, *LINT_FILES)


@nox.session
def formatters_check(session: nox.Session):
    """
    Check code formatting without making changes
    """
    install(session, req="formatters")
    session.run("isort", "--check", *session.posargs, *LINT_FILES)
    session.run("black", "--check", *session.posargs, *LINT_FILES)


@nox.session
def typing(session: nox.Session):
    install(session, req="typing")
    session.run("mypy", *session.posargs, *LINT_FILES)


@nox.session
def spelling(session: nox.Session):
    """
    Spell check RST documentation
    """
    install(session, req="spelling")
    session.run(
        "codespell",
        "docs/docsite",
        *session.posargs,
    )


@nox.session
def lint(session: nox.Session):
    session.notify("typing")
    session.notify("static")
    session.notify("formatters")
    session.notify("spelling")


requirements_files = list(
    {path.name.replace(".in", "") for path in Path("tests").glob("*in")}
    - {"constraints", "constraints-base"}
)


@nox.session(name="pip-compile", python=["3.10"])
@nox.parametrize(["req"], requirements_files, requirements_files)
def pip_compile(session: nox.Session, req: str):
    # .pip-tools.toml was introduced in v7
    session.install("pip-tools >= 7")

    # Use --upgrade by default unless a user passes -P.
    args = list(session.posargs)
    if not any(
        arg.startswith(("-P", "--upgrade-package", "--no-upgrade")) for arg in args
    ):
        args.append("--upgrade")

    # fmt: off
    session.run(
        "pip-compile",
        "--output-file", f"tests/{req}.txt",
        *args,
        f"tests/{req}.in",
    )
    # fmt: on


@nox.session(name="clone-core")
def clone_core(session: nox.Session):
    """
    Clone relevant portions of ansible-core from ansible/ansible into the current
    source tree to facilitate building docs.
    """
    session.run_always("python", "docs/bin/clone-core.py")


checker_tests = [
    path.with_suffix("").name for path in Path("tests/checkers/").glob("*.py")
]


def _relaxed_parser(session: nox.Session) -> ArgumentParser:
    """
    Generate an argument parser with a --relaxed option.
    """
    parser = ArgumentParser(prog=f"nox -e {session.name} --")
    parser.add_argument(
        "--relaxed",
        default=False,
        action=BooleanOptionalAction,
        help="Whether to use requirements-relaxed file. (Default: %(default)s)",
    )
    return parser


def _env_python(session: nox.Session) -> str:
    """
    Get the full path to an environment's python executable
    """
    out = cast(
        str,
        session.run("python", "-c", "import sys; print(sys.executable)", silent=True),
    )
    return out.strip()


@nox.session
@nox.parametrize(["test"], checker_tests, checker_tests)
def checkers(session: nox.Session, test: str):
    """
    Run docs build checkers
    """
    args = _relaxed_parser(session).parse_args(session.posargs)

    install(session, req="requirements-relaxed" if args.relaxed else "requirements")
    session.run("make", "-C", "docs/docsite", "clean", external=True)
    session.run("python", "tests/checkers.py", test)


@nox.session
def make(session: nox.Session):
    """
    Generate HTML from documentation source using the Makefile
    """
    parser = _relaxed_parser(session)
    parser.add_argument(
        "make_args", nargs="*", help="Specify make targets as arguments"
    )
    args = parser.parse_args(session.posargs)

    install(session, req="requirements-relaxed" if args.relaxed else "requirements")
    make_args: list[str] = [
        f"PYTHON={_env_python(session)}",
        *(args.make_args or ("clean", "coredocs")),
    ]
    session.run("make", "-C", "docs/docsite", *make_args, external=True)


def _rm_tmpdir(tmpdir):
    rmtree(tmpdir, ignore_errors=True)


@nox.session
def tag(session: nox.Session):
    """
    Check the core repo for new releases and create tags in ansible-documentation
    """
    install(session, req="tag")

    CORE_REPO = "https://github.com/ansible/ansible"
    DOCS_REPO = "https://github.com/ansible/ansible-documentation"

    args = list(session.posargs)
    tmpdir = None

    if not any(arg.startswith(("--core", "--docs")) for arg in args):
        if not which("git"):
            session.error("git is not installed or not found int PATH")

        tmpdir = session.create_tmp()
        core_dir = "".join((str(tmpdir), "/ansible"))
        docs_dir = "".join((str(tmpdir), "/ansible-docs"))

        try:
            session.run(
                "git",
                "clone",
                "--quiet",
                CORE_REPO,
                core_dir,
                external=True,
            )
            args.extend(["--core", core_dir])
        except Exception as e:
            session.error(f"Could not update core repository: {e}")
        try:
            session.run(
                "git",
                "clone",
                "--quiet",
                DOCS_REPO,
                docs_dir,
                external=True,
            )
            args.extend(["--core", docs_dir])
        except Exception as e:
            session.error(f"Could not update docs repository: {e}")

    # If run without any commands, default to "tag"
    if not any(arg.startswith(("hash", "mantag", "new-tags", "tag")) for arg in args):
        args.append("tag")

    try:
        session.run("python", "hacking/tagger/tag.py", *args)
    finally:
        if tmpdir:
            _rm_tmpdir(tmpdir)
