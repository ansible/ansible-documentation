from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile


def main():
    base_dir = os.getcwd()

    keep_dirs = [
        'bin',
        'docs',
        'examples',
        'hacking',
        'lib',
        'packaging',
        'test/lib',
    ]

    keep_files = [
        'MANIFEST.in',
        'pyproject.toml',
        'requirements.txt',
    ]

    # The tests write to the source tree, which isn't permitted for sanity tests.
    # To work around this a temporary copy is used.

    current_dir = os.getcwd()

    with tempfile.TemporaryDirectory(prefix='docs-build-', suffix='-sanity') as temp_dir:
        for keep_dir in keep_dirs:
            shutil.copytree(os.path.join(base_dir, keep_dir), os.path.join(temp_dir, keep_dir), symlinks=True)

        for keep_file in keep_files:
            shutil.copy2(os.path.join(base_dir, keep_file), os.path.join(temp_dir, keep_file))

        paths = os.environ['PATH'].split(os.pathsep)
        paths = [f'{temp_dir}/bin' if path == f'{current_dir}/bin' else path for path in paths]

        # Fix up the environment so everything runs from the temporary copy.
        os.environ['PATH'] = os.pathsep.join(paths)
        os.environ['PYTHONPATH'] = f'{temp_dir}/lib'
        os.chdir(temp_dir)

        run_test()


def run_test():
    base_dir = os.getcwd() + os.path.sep
    docs_dir = os.path.abspath('docs/docsite')

    cmd = ['make', 'core_singlehtmldocs']
    sphinx = subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True, cwd=docs_dir, check=False, text=True)

    stdout = sphinx.stdout
    stderr = sphinx.stderr

    if sphinx.returncode != 0:
        sys.stderr.write("Command '%s' failed with status code: %d\n" % (' '.join(cmd), sphinx.returncode))

        if stdout.strip():
            stdout = simplify_stdout(stdout)

            sys.stderr.write("--> Standard Output\n")
            sys.stderr.write("%s\n" % stdout.strip())

        if stderr.strip():
            sys.stderr.write("--> Standard Error\n")
            sys.stderr.write("%s\n" % stderr.strip())

        sys.exit(1)

    with open('docs/docsite/rst_warnings', 'r') as warnings_fd:
        output = warnings_fd.read().strip()
        lines = output.splitlines()

    known_warnings = {
        'block-quote-missing-blank-line': r'^Block quote ends without a blank line; unexpected unindent.$',
        'literal-block-lex-error': r'^Could not lex literal_block as "[^"]*". Highlighting skipped.$',
        'duplicate-label': r'^duplicate label ',
        'undefined-label': r'undefined label: ',
        'unknown-document': r'unknown document: ',
        'toc-tree-missing-document': r'toctree contains reference to nonexisting document ',
        'reference-target-not-found': r'[^ ]* reference target not found: ',
        'not-in-toc-tree': r"document isn't included in any toctree$",
        'unexpected-indentation': r'^Unexpected indentation.$',
        'definition-list-missing-blank-line': r'^Definition list ends without a blank line; unexpected unindent.$',
        'explicit-markup-missing-blank-line': r'Explicit markup ends without a blank line; unexpected unindent.$',
        'toc-tree-glob-pattern-no-match': r"^toctree glob pattern '[^']*' didn't match any documents$",
        'unknown-interpreted-text-role': '^Unknown interpreted text role "[^"]*".$',
    }

    for line in lines:
        match = re.search('^(?P<path>[^:]+):((?P<line>[0-9]+):)?((?P<column>[0-9]+):)? (?P<level>WARNING|ERROR): (?P<message>.*)$', line)

        if not match:
            path = 'docs/docsite/rst/index.rst'
            lineno = 0
            column = 0
            code = 'unknown'
            message = line

            # surface unknown lines while filtering out known lines to avoid excessive output
            print('%s:%d:%d: %s: %s' % (path, lineno, column, code, message))
            continue

        path = match.group('path')
        lineno = int(match.group('line') or 0)
        column = int(match.group('column') or 0)
        level = match.group('level').lower()
        message = match.group('message')

        path = os.path.abspath(path)

        if path.startswith(base_dir):
            path = path[len(base_dir):]

        if path.startswith('rst/'):
            path = 'docs/docsite/' + path  # fix up paths reported relative to `docs/docsite/`

        if level == 'warning':
            code = 'warning'

            for label, pattern in known_warnings.items():
                if re.search(pattern, message):
                    code = label
                    break
        else:
            code = 'error'

        print('%s:%d:%d: %s: %s' % (path, lineno, column, code, message))


def simplify_stdout(value):
    """Simplify output by omitting earlier 'rendering: ...' messages."""
    lines = value.strip().splitlines()

    rendering = []
    keep = []

    def truncate_rendering():
        """Keep last rendering line (if any) with a message about omitted lines as needed."""
        if not rendering:
            return

        notice = rendering[-1]

        if len(rendering) > 1:
            notice += ' (%d previous rendering line(s) omitted)' % (len(rendering) - 1)

        keep.append(notice)
        # Could change to rendering.clear() if we do not support python2
        rendering[:] = []

    for line in lines:
        if line.startswith('rendering: '):
            rendering.append(line)
            continue

        truncate_rendering()
        keep.append(line)

    truncate_rendering()

    result = '\n'.join(keep)

    return result


if __name__ == '__main__':
    main()
