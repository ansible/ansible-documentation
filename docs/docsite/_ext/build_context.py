"""Sphinx extension for setting up the build settings."""

import subprocess
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from tomllib import loads as parse_toml_string
from typing import Literal

from sphinx.application import Sphinx
from sphinx.util import logging


logger = logging.getLogger(__name__)


DOCSITE_ROOT_DIR = Path(__file__).parents[1].resolve()
DOCSITE_EOL_CONFIG_PATH = DOCSITE_ROOT_DIR / 'end_of_life.toml'


@dataclass(frozen=True)
class Distribution:
    end_of_life: list[str]
    supported: list[str]

    @classmethod
    def from_dict(cls, raw_dist: dict[str, list[str]]) -> 'Distribution':
        return cls(
            **{
                kind.replace('-', '_'): versions
                for kind, versions in raw_dist.items()
            },
        )


EOLConfigType = dict[str, Distribution]


@cache
def _read_eol_data() -> EOLConfigType:
    raw_config_dict = parse_toml_string(DOCSITE_EOL_CONFIG_PATH.read_text())

    return {
        dist_name: Distribution.from_dict(dist_data)
        for dist_name, dist_data in raw_config_dict['distribution'].items()
    }


@cache
def _is_eol_build(git_branch: str, kind: str) -> bool:
    return git_branch in _read_eol_data()[kind].end_of_life


@cache
def _get_current_git_branch():
    git_branch_cmd = 'git', 'rev-parse', '--abbrev-ref', 'HEAD'

    try:
        return subprocess.check_output(git_branch_cmd, text=True).strip()
    except subprocess.CalledProcessError as proc_err:
        raise LookupError(
            f'Failed to locate current Git branch: {proc_err !s}',
        ) from proc_err


def _set_global_j2_context(app, config):
    if 'is_eol' in config.html_context:
        raise ValueError(
            '`is_eol` found in `html_context` unexpectedly. '
            'It should not be set in `conf.py`.',
        ) from None

    dist_name = (
        'ansible-core' if app.tags.has('core')
        else 'ansible' if app.tags.has('ansible')
        else None
    )

    if dist_name is None:
        return

    try:
        git_branch = _get_current_git_branch()
    except LookupError as lookup_err:
        logger.info(str(lookup_err))
        return

    config.html_context['is_eol'] = _is_eol_build(
        git_branch=git_branch, kind=dist_name,
    )


def setup(app: Sphinx) -> dict[str, bool | str]:
    """Initialize the extension.

    :param app: A Sphinx application object.
    :returns: Extension metadata as a dict.
    """

    # NOTE: `config-inited` is used because it runs once as opposed to
    # NOTE: `html-page-context` that runs per each page. The data we
    # NOTE: compute is immutable throughout the build so there's no need
    # NOTE: to have a callback that would be executed hundreds of times.
    app.connect('config-inited', _set_global_j2_context)

    return {
        'parallel_read_safe': True,
        'parallel_write_safe': True,
        'version': app.config.release,
    }
