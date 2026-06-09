"""Sanity test using rstcheck-core and sphinx."""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys


def main():
    # Read input paths from CLI arguments or stdin
    if sys.argv[1:]:
        raw_paths = sys.argv[1:]
    else:
        raw_paths = sys.stdin.read().splitlines()

    # Convert to pathlib.Path objects
    paths = [pathlib.Path(p) for p in raw_paths]

    # Handle case where no paths are provided
    if not paths:
        print("No files or directories provided for checking.", file=sys.stderr)
        sys.exit(1)

    cmd = "rstcheck "
    cmd += " --report-level=none"
    cmd += " --ignore-roles=ansplugin,ansopt,ansretval,ansval,ansenvvar,ansenvvarref,ansoptref,anscollection,ansretvalref"
    cmd += " --ignore-substitutions=br"
    cmd += " --ignore-messages='.*vault.*|.*unsafe.*'"
    cmd += " --recursive "
    cmd += " ".join(str(path) for path in paths)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    _, stderr = process.communicate()
    if process.returncode != 0:
        pattern = re.compile(r'^(?P<path>[^:]*):(?P<line>[0-9]+): \((?P<level>INFO|WARNING|ERROR|SEVERE)/[0-4]\) (?P<message>.*)$')
        results = parse_to_list_of_dict(pattern, stderr)
        if results:
            for result in results:
                print('%s:%s:%s: %s' % (result['path'], result['line'], 0, result['message']))
            sys.exit(1)
    sys.exit(0)


def parse_to_list_of_dict(pattern, value):
    matched = []
    unmatched = []

    for line in value.splitlines():
        if line.startswith(('Error!', 'Success!',)):
            continue
        match = re.search(pattern, line)

        if match:
            matched.append(match.groupdict())
        else:
            unmatched.append(line)

    if unmatched:
        raise Exception('Pattern "%s" did not match values:\n%s' % (pattern, '\n'.join(unmatched)))

    return matched

if __name__ == '__main__':
    main()
