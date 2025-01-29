"""Sanity test using rstcheck-core and sphinx."""
from __future__ import annotations

from rstcheck_core.runner import RstcheckMainRunner
from rstcheck_core.config import RstcheckConfig
import pathlib
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

    # Define the configuration for rstcheck
    config = RstcheckConfig(
        ignore_roles=[
            "ansplugin", "ansopt", "ansretval", "ansval", "ansenvvar", "ansenvvarref"
        ],
        ignore_substitutions=["br"],
        report_level="warning",  # Adjust report level as needed: "info", "warning", "error", "severe", "none"
        recursive=True,          # Set to True to check directories recursively
    )

    # Initialize the runner
    runner = RstcheckMainRunner(
        check_paths=paths,
        rstcheck_config=config,
        overwrite_config=True,
    )
    
    # Run the checks
    exit_code = runner.run()
    
    # Exit with the appropriate code
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
