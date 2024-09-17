from __future__ import annotations

import os
import shlex
from argparse import ArgumentParser, BooleanOptionalAction
from glob import iglob
from pathlib import Path
from typing import cast

import nox

LINT_FILES: tuple[str, ...] = (
    "hacking/pr_labeler/pr_labeler",
    "hacking/tagger/tag.py",
    "noxfile.py",
    *iglob("docs/bin/*.py"),
)
PINNED = os.environ.get("PINNED", "true").lower() in {"1", "true"}
nox.options.sessions = ("clone-core", "lint", "checkers", "make")


def _set_env_verbose(session: nox.Session, **env: str) -> dict[str, str]:
    """
    Helper function to verbosely set environment variables
    """
    final_env: dict[str, str] = {}
    for key, value in env.items():
        final_env[key] = value
        session.log(f"export {key}={shlex.quote(value)}")
    return final_env


def install(session: nox.Session, *args, req: str, **kwargs):
    if PINNED:
        pip_constraint = f"tests/{req}.txt"
        # Set constraint environment variables for both pip and uv to support
        # the nox uv backend
        env = _set_env_verbose(
            session,
            PIP_CONSTRAINT=pip_constraint,
            UV_CONSTRAINT=pip_constraint,
            UV_BUILD_CONSTRAINT=pip_constraint,
        )
        kwargs.setdefault("env", {}).update(env)
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


@nox.session(name="pip-compile", python=["3.11"])
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
    session.run_always("python", "docs/bin/clone-core.py", *session.posargs)


checker_tests = [
    path.with_suffix("").name for path in Path("tests/checkers/").glob("*.py")
]


def _clone_core_check(session: nox.Session) -> None:
    """
    Helper function to run the clone-core script with "--check"
    """
    session.run("python", "docs/bin/clone-core.py", "--check")


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
    _clone_core_check(session)
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
    _clone_core_check(session)
    make_args: list[str] = [
        f"PYTHON={_env_python(session)}",
        *(args.make_args or ("clean", "coredocs")),
    ]
    session.run("make", "-C", "docs/docsite", *make_args, external=True)


@nox.session
def tag(session: nox.Session):
    """
    Check the core repo for new releases and create tags in ansible-documentation
    """
    install(session, req="tag")
    args = list(session.posargs)

    # If run without any arguments, default to "tag"
    if not any(arg.startswith(("hash", "mantag", "new-tags", "tag")) for arg in args):
        args.append("tag")

    session.run("python", "hacking/tagger/tag.py", *args)
