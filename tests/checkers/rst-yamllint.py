"""Sanity test using rstcheck and sphinx."""

from __future__ import annotations

import io
import pathlib
import sys
import traceback
import typing as t

from antsibull_docutils.rst_code_finder import find_code_blocks
from yamllint import linter
from yamllint.config import YamlLintConfig
from yamllint.linter import PROBLEM_LEVELS

REPORT_LEVELS: set[PROBLEM_LEVELS] = {
    "warning",
    "error",
}

ALLOWED_LANGUAGES = {
    "ansible-output",
    "bash",
    "console",
    "csharp",
    "diff",
    "ini",
    "jinja",
    "json",
    "md",
    "none",
    "powershell",
    "python",
    "rst",
    "sh",
    "shell",
    "shell-session",
    "text",
}


def create_warn_unknown_block(
    results: list[dict[str, t.Any]], path: str
) -> t.Callable[[int | str, int, str, bool], None]:
    def warn_unknown_block(
        line: int | str, col: int, content: str, unknown_directive: bool
    ) -> None:
        if unknown_directive:
            results.append(
                {
                    "path": path,
                    "line": line,
                    "col": col,
                    "message": (
                        "Warning: found unknown literal block! Check for double colons '::'."
                        " If that is not the cause, please report this warning."
                        " It might indicate a bug in the checker or an unsupported Sphinx directive."
                        f" Content: {content!r}"
                    ),
                }
            )
        else:
            allowed_languages = ", ".join(sorted(ALLOWED_LANGUAGES))
            results.append(
                {
                    "path": path,
                    "line": line,
                    "col": 0,
                    "message": (
                        "Warning: literal block (check for double colons '::')."
                        " Please convert this to a regular code block with an appropriate language."
                        f" Allowed languages: {allowed_languages}"
                    ),
                }
            )

    return warn_unknown_block


def main() -> None:
    paths = sys.argv[1:] or sys.stdin.read().splitlines()
    results: list[dict[str, t.Any]] = []

    # TODO: should we handle the 'literalinclude' directive? maybe check file directly if right extension?
    # (https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-literalinclude)

    repo_root = pathlib.Path(__file__).resolve().parent.parent.parent
    docs_root = repo_root / "docs" / "docsite" / "rst"

    with open(repo_root / ".yamllint", encoding="utf-8") as f:
        yamllint_config = YamlLintConfig(f.read())

    for path in paths:
        with open(path, "rt", encoding="utf-8") as f:
            content = f.read()

        try:
            for code_block in find_code_blocks(
                content,
                path=path,
                root_prefix=docs_root,
                warn_unknown_block_w_unknown_info=create_warn_unknown_block(
                    results, path
                ),
            ):
                # Now that we have the offsets, we can actually do some processing...
                if code_block.language not in {
                    "YAML",
                    "yaml",
                    "yaml+jinja",
                    "YAML+Jinja",
                }:
                    if code_block.language is None:
                        allowed_languages = ", ".join(sorted(ALLOWED_LANGUAGES))
                        results.append(
                            {
                                "path": path,
                                "line": code_block.row_offset + 1,
                                "col": code_block.col_offset + 1,
                                "message": (
                                    "Literal block without language!"
                                    f" Allowed languages are: {allowed_languages}."
                                ),
                            }
                        )
                        return
                    if code_block.language not in ALLOWED_LANGUAGES:
                        allowed_languages = ", ".join(sorted(ALLOWED_LANGUAGES))
                        results.append(
                            {
                                "path": path,
                                "line": code_block.row_offset + 1,
                                "col": code_block.col_offset + 1,
                                "message": (
                                    f"Warning: literal block with disallowed language: {code_block.language}."
                                    " If the language should be allowed, the checker needs to be updated."
                                    f" Currently allowed languages are: {allowed_languages}."
                                ),
                            }
                        )
                    continue

                # So we have YAML. Let's lint it!
                try:
                    problems = linter.run(
                        io.StringIO(code_block.content),
                        yamllint_config,
                        path,
                    )
                    for problem in problems:
                        if problem.level not in REPORT_LEVELS:
                            continue
                        msg = f"{problem.level}: {problem.desc}"
                        if problem.rule:
                            msg += f"  ({problem.rule})"
                        results.append(
                            {
                                "path": path,
                                "line": code_block.row_offset + problem.line,
                                "col": code_block.col_offset + problem.column,
                                "message": msg,
                            }
                        )
                except Exception as exc:
                    error = str(exc).replace("\n", " / ")
                    results.append(
                        {
                            "path": path,
                            "line": code_block.row_offset + 1,
                            "col": code_block.col_offset + 1,
                            "message": (
                                f"Internal error while linting YAML: exception {type(exc)}:"
                                f" {error}; traceback: {traceback.format_exc()!r}"
                            ),
                        }
                    )
        except Exception as exc:
            error = str(exc).replace("\n", " / ")
            results.append(
                {
                    "path": path,
                    "line": 0,
                    "col": 0,
                    "message": f"Cannot process document: {type(exc)} {error}; traceback: {traceback.format_exc()!r}",
                }
            )

    for result in sorted(
        results,
        key=lambda result: (
            result["path"],
            result["line"],
            result["col"],
            result["message"],
        ),
    ):
        print("{path}:{line}:{col}: {message}".format(**result))


if __name__ == "__main__":
    main()
