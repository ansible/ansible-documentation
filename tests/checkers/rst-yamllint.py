"""Sanity test using rstcheck and sphinx."""

from __future__ import annotations

import io
import pathlib
import sys
import traceback

from docutils import nodes
from docutils.core import Publisher
from docutils.io import StringInput
from docutils.parsers.rst import Directive
from docutils.parsers.rst.directives import register_directive
from docutils.parsers.rst.directives import unchanged as directive_param_unchanged
from docutils.utils import Reporter, SystemMessage
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


class IgnoreDirective(Directive):
    has_content = True

    def run(self) -> list:
        return []


class CodeBlockDirective(Directive):
    has_content = True
    optional_arguments = 1

    # These are all options Sphinx allows for code blocks.
    # We need to have them here so that docutils successfully parses this extension.
    option_spec = {
        "caption": directive_param_unchanged,
        "class": directive_param_unchanged,
        "dedent": directive_param_unchanged,
        "emphasize-lines": directive_param_unchanged,
        "name": directive_param_unchanged,
        "force": directive_param_unchanged,
        "linenos": directive_param_unchanged,
        "lineno-start": directive_param_unchanged,
    }

    def run(self) -> list[nodes.literal_block]:
        code = "\n".join(self.content)
        literal = nodes.literal_block(code, code)
        literal["classes"].append("code-block")
        literal["ansible-code-language"] = self.arguments[0] if self.arguments else None
        literal["ansible-code-block"] = True
        literal["ansible-code-lineno"] = self.lineno
        return [literal]


class YamlLintVisitor(nodes.SparseNodeVisitor):
    def __init__(
        self,
        document: nodes.document,
        path: str,
        results: list[dict],
        content: str,
        yamllint_config: YamlLintConfig,
    ):
        super().__init__(document)
        self.__path = path
        self.__results = results
        self.__content_lines = content.splitlines()
        self.__yamllint_config = yamllint_config

    def visit_system_message(self, node: nodes.system_message) -> None:
        raise nodes.SkipNode

    def visit_error(self, node: nodes.error) -> None:
        raise nodes.SkipNode

    def visit_literal_block(self, node: nodes.literal_block) -> None:
        if "ansible-code-block" not in node.attributes:
            if node.attributes["classes"]:
                self.__results.append(
                    {
                        "path": self.__path,
                        "line": node.line or "unknown",
                        "col": 0,
                        "message": (
                            "Warning: found unknown literal block! Check for double colons '::'."
                            " If that is not the cause, please report this warning."
                            " It might indicate a bug in the checker or an unsupported Sphinx directive."
                            f" Node: {node!r}; attributes: {node.attributes}; content: {node.rawsource!r}"
                        ),
                    }
                )
            raise nodes.SkipNode

        language = node.attributes["ansible-code-language"]
        lineno = node.attributes["ansible-code-lineno"]

        # Ok, we have to find both the row and the column offset for the actual code content
        row_offset = lineno
        found_empty_line = False
        found_content_lines = False
        content_lines = node.rawsource.count("\n") + 1
        min_indent = None
        for offset, line in enumerate(self.__content_lines[lineno:]):
            stripped_line = line.strip()
            if not stripped_line:
                if not found_empty_line:
                    row_offset = lineno + offset + 1
                    found_empty_line = True
            elif not found_content_lines:
                found_content_lines = True
                row_offset = lineno + offset

            if found_content_lines and content_lines > 0:
                if stripped_line:
                    indent = len(line) - len(line.lstrip())
                    if min_indent is None or min_indent > indent:
                        min_indent = indent
                content_lines -= 1
            elif not content_lines:
                break

        min_source_indent = None
        for line in node.rawsource.split("\n"):
            stripped_line = line.lstrip()
            if stripped_line:
                indent = len(line) - len(line.lstrip())
                if min_source_indent is None or min_source_indent > indent:
                    min_source_indent = indent

        col_offset = max(0, (min_indent or 0) - (min_source_indent or 0))

        # Now that we have the offsets, we can actually do some processing...
        if language not in {"YAML", "yaml", "yaml+jinja", "YAML+Jinja"}:
            if language is None:
                allowed_languages = ", ".join(sorted(ALLOWED_LANGUAGES))
                self.__results.append(
                    {
                        "path": self.__path,
                        "line": row_offset + 1,
                        "col": col_offset + 1,
                        "message": (
                            "Literal block without language!"
                            f" Allowed languages are: {allowed_languages}."
                        ),
                    }
                )
                return
            if language not in ALLOWED_LANGUAGES:
                allowed_languages = ", ".join(sorted(ALLOWED_LANGUAGES))
                self.__results.append(
                    {
                        "path": self.__path,
                        "line": row_offset + 1,
                        "col": col_offset + 1,
                        "message": (
                            f"Warning: literal block with disallowed language: {language}."
                            " If the language should be allowed, the checker needs to be updated."
                            f" Currently allowed languages are: {allowed_languages}."
                        ),
                    }
                )
            raise nodes.SkipNode

        # So we have YAML. Let's lint it!
        try:
            problems = linter.run(
                io.StringIO(node.rawsource.rstrip() + "\n"),
                self.__yamllint_config,
                self.__path,
            )
            for problem in problems:
                if problem.level not in REPORT_LEVELS:
                    continue
                msg = f"{problem.level}: {problem.desc}"
                if problem.rule:
                    msg += f"  ({problem.rule})"
                self.__results.append(
                    {
                        "path": self.__path,
                        "line": row_offset + problem.line,
                        "col": col_offset + problem.column,
                        "message": msg,
                    }
                )
        except Exception as exc:
            error = str(exc).replace("\n", " / ")
            self.__results.append(
                {
                    "path": self.__path,
                    "line": row_offset + 1,
                    "col": col_offset + 1,
                    "message": (
                        f"Internal error while linting YAML: exception {type(exc)}:"
                        f" {error}; traceback: {traceback.format_exc()!r}"
                    ),
                }
            )

        raise nodes.SkipNode


def main():
    paths = sys.argv[1:] or sys.stdin.read().splitlines()
    results = []

    for directive in (
        "code",
        "code-block",
        "sourcecode",
    ):
        register_directive(directive, CodeBlockDirective)

    # The following docutils directives should better be ignored:
    for directive in ("parsed-literal",):
        register_directive(directive, IgnoreDirective)

    # TODO: should we handle the 'literalinclude' directive? maybe check file directly if right extension?
    # (https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-literalinclude)

    repo_root = pathlib.Path(__file__).resolve().parent.parent.parent
    docs_root = repo_root / "docs" / "docsite" / "rst"

    with open(repo_root / ".yamllint", encoding="utf-8") as f:
        yamllint_config = YamlLintConfig(f.read())

    for path in paths:
        with open(path, "rt", encoding="utf-8") as f:
            content = f.read()

        # We create a Publisher only to have a mechanism which gives us the settings object.
        # Doing this more explicit is a bad idea since the classes used are deprecated and will
        # eventually get replaced. Publisher.get_settings() looks like a stable enough API that
        # we can 'just use'.
        publisher = Publisher(source_class=StringInput)
        publisher.set_components("standalone", "restructuredtext", "pseudoxml")
        override = {
            "root_prefix": docs_root,
            "input_encoding": "utf-8",
            "file_insertion_enabled": False,
            "raw_enabled": False,
            "_disable_config": True,
            "report_level": Reporter.ERROR_LEVEL,
            "warning_stream": io.StringIO(),
        }
        publisher.process_programmatic_settings(None, override, None)
        publisher.set_source(content, path)

        # Parse the document
        try:
            doc = publisher.reader.read(
                publisher.source, publisher.parser, publisher.settings
            )
        except SystemMessage as exc:
            error = str(exc).replace("\n", " / ")
            results.append(
                {
                    "path": path,
                    "line": 0,
                    "col": 0,
                    "message": f"Cannot parse document: {error}",
                }
            )
            continue
        except Exception as exc:
            error = str(exc).replace("\n", " / ")
            results.append(
                {
                    "path": path,
                    "line": 0,
                    "col": 0,
                    "message": f"Cannot parse document, unexpected error {type(exc)}: {error}; traceback: {traceback.format_exc()!r}",
                }
            )
            continue

        # Process the document
        try:
            visitor = YamlLintVisitor(doc, path, results, content, yamllint_config)
            doc.walk(visitor)
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
