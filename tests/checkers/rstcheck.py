from rstcheck_core.runner import RstcheckMainRunner
from rstcheck_core.config import RstcheckConfig
import pathlib
import sys

def main():
    # Define the paths to check (passed as CLI arguments or from stdin)
    paths = [pathlib.Path(p) for p in (sys.argv[1:] or sys.stdin.read().splitlines())]

    # Define the configuration for rstcheck
    config = RstcheckConfig(
        ignore_roles=[
            "ansplugin", "ansopt", "ansretval", "ansval", "ansenvvar", "ansenvvarref"
        ],
        ignore_substitutions=["br"],
        report_level="warning",  # Adjust report level as needed -> ["info": 1, "warning": 2, "error": 3,"severe": 4, "none": 5,]
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

if __name__ == "__main__":
    main()
