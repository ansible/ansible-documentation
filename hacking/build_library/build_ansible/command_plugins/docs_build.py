# coding: utf-8
# Copyright: (c) 2020, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function

import glob
import os
import os.path
import pathlib
import shutil
import subprocess
from tempfile import TemporaryDirectory

import yaml

from ansible.release import __version__ as ansible_core__version__

# Pylint doesn't understand Python3 namespace modules.
# pylint: disable=relative-beyond-top-level
from ..commands import Command
from ..errors import InvalidUserInput
# pylint: enable=relative-beyond-top-level


__metaclass__ = type


DEFAULT_TOP_DIR = pathlib.Path(__file__).parents[4]
DEFAULT_OUTPUT_DIR = pathlib.Path(__file__).parents[4] / 'docs/docsite'


class NoSuchFile(Exception):
    """An expected file was not found."""


#
# Helpers
#

def find_latest_ansible_dir(build_data_working) -> tuple[str, "packaging.version.Version"]:
    """Find the most recent ansible major version."""
    # imports here so that they don't cause unnecessary deps for all of the plugins
    from packaging.version import InvalidVersion, Version

    ansible_directories = glob.glob(os.path.join(build_data_working, '[0-9.]*'))

    # Find the latest ansible version directory
    latest_dir = None
    latest_ver = Version('0')
    for directory_name in (d for d in ansible_directories if os.path.isdir(d)):
        try:
            new_version = Version(os.path.basename(directory_name))
        except InvalidVersion:
            continue

        # For the devel build, we only need ansible.in, so make sure it's there
        if not os.path.exists(os.path.join(directory_name, 'ansible.in')):
            continue

        if new_version > latest_ver:
            latest_ver = new_version
            latest_dir = directory_name

    if latest_dir is None:
        raise NoSuchFile('Could not find an ansible data directory in {0}'.format(build_data_working))

    return latest_dir, latest_ver


def parse_deps_file(filename):
    """Parse an antsibull .deps file."""
    with open(filename, 'r', encoding='utf-8') as f:
        contents = f.read()
    lines = [c for line in contents.splitlines() if (c := line.strip()) and not c.startswith('#')]
    return dict([entry.strip() for entry in line.split(':', 1)] for line in lines)


def write_deps_file(filename, deps_data):
    """Write an antsibull .deps file."""
    with open(filename, 'w', encoding='utf-8') as f:
        for key, value in deps_data.items():
            f.write(f'{key}: {value}\n')


def find_latest_deps_file(build_data_working, ansible_version: str) -> tuple[str, "packaging.version.Version"]:
    """Find the most recent ansible deps file for the given ansible major version."""
    # imports here so that they don't cause unnecessary deps for all of the plugins
    from packaging.version import Version

    data_dir = os.path.join(build_data_working, ansible_version)
    deps_files = glob.glob(os.path.join(data_dir, '*.deps'))
    if not deps_files:
        raise Exception('No deps files exist for version {0}'.format(ansible_version))

    # Find the latest version of the deps file for this major version
    latest_deps_file = None
    latest_ver = Version('0')
    for filename in deps_files:
        deps_data = parse_deps_file(filename)
        new_version = Version(deps_data['_ansible_version'])
        if new_version > latest_ver:
            latest_ver = new_version
            latest_deps_file = filename

    if latest_deps_file is None:
        raise NoSuchFile('Could not find an ansible deps file in {0}'.format(data_dir))

    return latest_deps_file, latest_ver


#
# Subcommand core
#

def generate_core_docs(args):
    """Regenerate the documentation for all plugins listed in the plugin_to_collection_file."""
    # imports here so that they don't cause unnecessary deps for all of the plugins
    from antsibull_docs.cli import antsibull_docs

    with TemporaryDirectory() as tmp_dir:
        #
        # Construct a deps file with our version of ansible_core in it
        #
        modified_deps_file = os.path.join(tmp_dir, 'ansible.deps')

        # The _ansible_version doesn't matter since we're only building docs for core
        deps_file_contents = {'_ansible_version': ansible_core__version__,
                              '_ansible_core_version': ansible_core__version__}

        with open(modified_deps_file, 'w') as f:
            f.write(yaml.dump(deps_file_contents))

        # Generate the plugin rst
        full_command = [
            'antsibull-docs',
            'stable',
            '--deps-file',
            modified_deps_file,
            '--ansible-core-source',
            str(args.top_dir),
            '--dest-dir',
            args.output_dir,
        ]
        print(f"Running {full_command!r}:")
        return antsibull_docs.run(full_command)

        # If we make this more than just a driver for antsibull:
        # Run other rst generation
        # Run sphinx build


#
# Subcommand full
#

def generate_full_docs(args):
    """Regenerate the documentation for all plugins listed in the plugin_to_collection_file."""
    # imports here so that they don't cause unnecessary deps for all of the plugins
    from antsibull_docs.cli import antsibull_docs

    with TemporaryDirectory() as tmp_dir:
        subprocess.run(
            ['git', 'clone', 'https://github.com/ansible-community/ansible-build-data'],
            check=True,
            cwd=tmp_dir,
        )
        # If we want to validate that the ansible version and ansible-core branch version match,
        # this would be the place to do it.

        build_data_working = os.path.join(tmp_dir, 'ansible-build-data')
        if args.ansible_build_data:
            build_data_working = args.ansible_build_data

        ansible_version: str = args.ansible_version
        if ansible_version is None:
            devel_dir, devel_version = find_latest_ansible_dir(build_data_working)
            params = ['devel', '--pieces-file', 'ansible.in', '--major-version', str(devel_version.major)]
            cwd = str(devel_dir)
        else:
            latest_deps_file, ansible_version_ver = find_latest_deps_file(build_data_working, ansible_version)
            deps_dir = os.path.dirname(latest_deps_file)

            # Make a copy of the deps file so that we can set the ansible-core version we'll use
            modified_deps_file = os.path.join(tmp_dir, 'ansible.deps')
            shutil.copyfile(latest_deps_file, modified_deps_file)

            # Make a copy of collection-meta.yaml
            shutil.copyfile(os.path.join(deps_dir, 'collection-meta.yaml'), os.path.join(tmp_dir, 'collection-meta.yaml'))

            # Put our version of ansible-core into the deps file
            deps_data = parse_deps_file(modified_deps_file)

            deps_data['_ansible_core_version'] = ansible_core__version__

            write_deps_file(modified_deps_file, deps_data)

            params = ['stable', '--deps-file', 'ansible.deps', '--version', str(ansible_version_ver)]
            cwd = str(tmp_dir)

        old_cwd = os.getcwd()
        try:
            os.chdir(cwd)
            # Generate the plugin rst
            full_command = ['antsibull-docs'] + params + [
                '--ansible-core-source',
                os.path.join(old_cwd, str(args.top_dir)),
                '--dest-dir',
                os.path.join(old_cwd, args.output_dir),
            ]
            print(f"Running {full_command!r} in {cwd!r}:")
            return antsibull_docs.run(full_command)
        finally:
            os.chdir(old_cwd)

        # If we make this more than just a driver for antsibull:
        # Run other rst generation
        # Run sphinx build


class CollectionPluginDocs(Command):
    name = 'docs-build'
    _ACTION_HELP = """Action to perform.
        full: Regenerate the rst for the full ansible website.
        core: Regenerate the rst for plugins in ansible-core and then build the website.
    """

    @classmethod
    def init_parser(cls, add_parser):
        parser = add_parser(cls.name,
                            description='Generate documentation for plugins in collections.'
                            ' Plugins in collections will have a stub file in the normal plugin'
                            ' documentation location that says the module is in a collection and'
                            ' point to generated plugin documentation under the collections/'
                            ' hierarchy.')
        # I think we should make the actions a subparser but need to look in git history and see if
        # we tried that and changed it for some reason.
        parser.add_argument('action', action='store', choices=('full', 'core'),
                            default='full', help=cls._ACTION_HELP)
        parser.add_argument("-o", "--output-dir", action="store", dest="output_dir",
                            default=DEFAULT_OUTPUT_DIR,
                            help="Output directory for generated doc files")
        parser.add_argument("-t", "--top-dir", action="store", dest="top_dir",
                            default=DEFAULT_TOP_DIR,
                            help="Toplevel directory of this ansible-core checkout or expanded"
                            " tarball.")
        parser.add_argument("-l", "--limit-to-modules", '--limit-to', action="store",
                            dest="limit_to", default=None,
                            help="Limit building module documentation to comma-separated list of"
                            " plugins. Specify non-existing plugin name for no plugins.")
        parser.add_argument('--ansible-version', action='store',
                            dest='ansible_version', default=None,
                            help='The version of the ansible package to make documentation for.'
                            '  This only makes sense when used with full.')
        parser.add_argument('--ansible-build-data', action='store',
                            dest='ansible_build_data', default=None,
                            help='A checkout of the ansible-build-data repo.  Useful for'
                            ' debugging.')

    @staticmethod
    def main(args):
        # normalize and validate CLI args

        if args.ansible_version and args.action != 'full':
            raise InvalidUserInput('--ansible-version is only for use with "full".')

        if not args.output_dir:
            args.output_dir = os.path.abspath(str(DEFAULT_OUTPUT_DIR))

        if args.action == 'full':
            return generate_full_docs(args)

        if args.action == 'core':
            return generate_core_docs(args)

        raise NotImplementedError('New actions have to be explicitly supported by the code')

        # return 0
