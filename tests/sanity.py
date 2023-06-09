#!/usr/bin/env python
"""Simple test runner."""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parent.parent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('test', nargs='+')

    args = parser.parse_args()
    tests: list[str] = args.test
    failed = False

    for test in tests:
        if run_test(test):
            failed = True

    if failed:
        sys.exit(1)


def run_test(name: str) -> bool:
    print(f'Running {name!r} checker ...', file=sys.stderr, flush=True)

    checker_path = ROOT / 'tests' / 'checkers' / f'{name}.py'
    checker_json = checker_path.with_suffix('.json')

    try:
        config = json.loads(checker_json.read_text())
    except FileNotFoundError:
        config = {}

    paths = []
    extensions = set(config.get('extensions', []))

    for root, dir_names, file_names in os.walk(ROOT / 'docs'):
        for file_name in file_names:
            path = os.path.join(root, file_name)
            ext = os.path.splitext(path)[1]

            if ext in extensions:
                paths.append(path)

    cmd = [sys.executable, checker_path] + paths
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)

    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)

    return bool(result.stdout or result.stderr)


if __name__ == '__main__':
    main()
