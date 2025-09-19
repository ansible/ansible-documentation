from __future__ import annotations

import os
import shlex
import shutil
from contextlib import suppress
from glob import iglob
from pathlib import Path
from typing import cast

import nox

LINT_FILES: tuple[str, ...] = (
    "hacking/pr_labeler/pr_labeler",
    "hacking/tagger/tag.py",
    "noxfile.py",
    *iglob("docs/bin/*.py"),
    *iglob("tests/checkers/rst-yamllint*.py"),  # TODO: also lint others
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


CONTAINER_ENGINES = ("podman", "docker")
CHOSEN_CONTAINER_ENGINE = os.environ.get("CONTAINER_ENGINE")
ACTIONLINT_IMAGE = "docker.io/rhysd/actionlint"


def _get_container_engine(session: nox.Session) -> str:
    path: str | None = None
    if CHOSEN_CONTAINER_ENGINE:
        path = shutil.which(CHOSEN_CONTAINER_ENGINE)
        if not path:
            session.error(
                f"CONTAINER_ENGINE {CHOSEN_CONTAINER_ENGINE!r} does not exist!"
            )
        return path
    for engine in CONTAINER_ENGINES:
        if path := shutil.which(engine):
            return path
    session.error(
        f"None of the following container engines were found: {CONTAINER_ENGINES}."
        f" {session.name} requires a container engine installed."
    )


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
def actionlint(session: nox.Session) -> None:
    """
    Run actionlint to lint Github Actions workflows.
    The actionlint tool is run in a Podman/Docker container.
    """
    engine = _get_container_engine(session)
    session.run_always(engine, "pull", ACTIONLINT_IMAGE, external=True)
    session.run(
        engine,
        "run",
        "--rm",
        # fmt: off
        "--volume", f"{Path.cwd()}:/pwd:z",
        "--workdir", "/pwd",
        # fmt: on
        ACTIONLINT_IMAGE,
        *session.posargs,
        external=True,
    )


@nox.session
def lint(session: nox.Session):
    session.notify("typing")
    session.notify("static")
    session.notify("formatters")
    session.notify("spelling")
    session.notify("actionlint")


requirements_files = list(
    {path.name.replace(".in", "") for path in Path("tests").glob("*in")}
    - {"constraints", "constraints-base"}
)


@nox.session(name="pip-compile", python="3.12")
@nox.parametrize(["req"], requirements_files, requirements_files)
def pip_compile(session: nox.Session, req: str):
    """
    Update dependency lockfiles in tests/ directory with uv pip compile.
    In addition to the usual flags supported by uv pip compile,
    this nox session implements two custom custom flags:

        --no-upgrade
            By default, the noxfile passes --upgrade to uv pip compile which
            updates all package versions in the lockfiles.
            Pass --no-upgrade to keep existing package versions as they are and
            only make the most minimal changes to sync the lockfiles with the input
            (.in) files.
        --check
            Run uv pip compile without --upgrade and fail if any changes were made.
            This ensures the lockfiles are in sync with the input files.
    """
    install(session, req="pip-compile")

    args = list(session.posargs)
    check_mode = "--check" in args
    if check_mode:
        # Remove from args, as pip compile doesn't actually support --check.
        args.remove("--check")
    elif not any(
        arg.startswith(("-P", "--upgrade-package", "--no-upgrade")) for arg in args
    ):
        # Use --upgrade by default unless the user passes a conflicting flag.
        args.append("--upgrade")
    # Like --check, also remove --no-upgrade from args if it's present.
    with suppress(ValueError):
        args.remove("--no-upgrade")

    # fmt: off
    session.run(
        "uv", "pip", "compile",
        "--universal",
        "--quiet",
        "--output-file", f"tests/{req}.txt",
        *args,
        f"tests/{req}.in",
    )
    # fmt: on

    if check_mode and session.run("git", "diff", "tests", silent=True, external=True):
        session.error("Check mode: files were changed")


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

    install(session, req="requirements")
    _clone_core_check(session)
    session.run("make", "-C", "docs/docsite", "clean", external=True)
    session.run("python", "tests/checkers.py", test)


@nox.session
def make(session: nox.Session):
    """
    Generate HTML from documentation source using the Makefile
    """
    make_args = session.posargs or ["clean", "coredocs"]

    install(session, req="requirements")
    _clone_core_check(session)
    session.run(
        "make",
        "-C",
        "docs/docsite",
        f"PYTHON={_env_python(session)}",
        *make_args,
        external=True,
    )


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
