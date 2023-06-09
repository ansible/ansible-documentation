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
    keep_dirs = [
        'bin',
        'lib',
        'packaging',
        'test/lib',
        'test/sanity',
    ]

    keep_files = [
        'MANIFEST.in',
        'pyproject.toml',
        'requirements.txt',
        'setup.cfg',
        'setup.py',
    ]

    branch = (ROOT / 'docs' / 'ansible-core-branch.txt').read_text().strip()

    with tempfile.TemporaryDirectory() as temp_dir:
        subprocess.run(['git', 'clone', 'https://github.com/ansible/ansible', '--depth=1', '-b', branch, temp_dir], check=True)

        for keep_dir in keep_dirs:
            src = pathlib.Path(temp_dir, keep_dir)
            dst = pathlib.Path.cwd() / keep_dir

            print(f'Updating {keep_dir!r} ...', file=sys.stderr, flush=True)

            if dst.exists():
                shutil.rmtree(dst)

            shutil.copytree(src, dst, symlinks=True)

            (dst / '.gitignore').write_text('*')

        for keep_file in keep_files:
            src = pathlib.Path(temp_dir, keep_file)
            dst = pathlib.Path.cwd() / keep_file

            print(f'Updating {keep_file!r} ...', file=sys.stderr, flush=True)

            shutil.copyfile(src, dst)


if __name__ == '__main__':
    main()
