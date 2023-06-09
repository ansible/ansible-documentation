#!/usr/bin/env python
"""Clone relevant portions of ansible-core from ansible/ansible into the current source tree to facilitate building docs."""

from __future__ import annotations

import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent


def main() -> None:
    paths = (
        'MANIFEST.in',
        'README.rst',
        'bin',
        'examples',
        'hacking',
        'lib',
        'packaging',
        'pyproject.toml',
        'requirements.txt',
        'setup.cfg',
        'setup.py',
        'test/lib',
        'test/sanity',
    )

    branch = (ROOT / 'docs' / 'ansible-core-branch.txt').read_text().strip()

    with tempfile.TemporaryDirectory() as temp_dir:
        subprocess.run(['git', 'clone', 'https://github.com/ansible/ansible', '--depth=1', '-b', branch, temp_dir], check=True)

        for path in paths:
            src = pathlib.Path(temp_dir, path)
            dst = pathlib.Path.cwd() / path

            print(f'Updating {path!r} ...', file=sys.stderr, flush=True)

            if src.is_dir():
                if dst.exists():
                    shutil.rmtree(dst)

                shutil.copytree(src, dst)

                (dst / '.gitignore').write_text('*')
            else:
                shutil.copyfile(src, dst)


if __name__ == '__main__':
    main()
