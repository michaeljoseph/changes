import textwrap
from os.path import exists, expanduser, expandvars, join, curdir
import io
import os
import sys

import click
from pathlib import Path

import toml
import attr

import changes
from changes.models import GitRepository
from .commands import info, note


AUTH_TOKEN_ENVVAR = 'GITHUB_AUTH_TOKEN'

# via https://github.com/jakubroztocil/httpie/blob/6bdfc7a/httpie/config.py#L9
IS_WINDOWS = 'win32' in str(sys.platform).lower()
DEFAULT_CONFIG_FILE = str(os.environ.get(
    'CHANGES_CONFIG_FILE',
    expanduser('~/.changes') if not IS_WINDOWS else
    expandvars(r'%APPDATA%\\.changes')
))

PROJECT_CONFIG_FILE = '.changes.toml'
DEFAULT_RELEASES_DIRECTORY = 'docs/releases'


@attr.s
class Changes(object):
    auth_token = attr.ib()


def load_settings():
    tool_config_path = Path(str(os.environ.get(
        'CHANGES_CONFIG_FILE',
        expanduser('~/.changes') if not IS_WINDOWS else
        expandvars(r'%APPDATA%\\.changes')
    )))

    tool_settings = None
    if tool_config_path.exists():
        tool_settings = Changes(
            **(toml.load(tool_config_path.read_text())['changes'])
        )

    if not (tool_settings and tool_settings.auth_token):
        # prompt for auth token
        auth_token = os.environ.get(AUTH_TOKEN_ENVVAR)
        if auth_token:
            info('Found Github Auth Token in the environment')

        while not auth_token:
            info('No auth token found, asking for it')
            # to interact with the Git*H*ub API
            note('You need a Github Auth Token for changes to create a release.')
            click.pause('Press [enter] to launch the GitHub "New personal access '
                        'token" page, to create a token for changes.')
            click.launch('https://github.com/settings/tokens/new')
            auth_token = click.prompt('Enter your changes token')

        if not tool_settings:
            tool_settings = Changes(auth_token=auth_token)

        tool_config_path.write_text(
            toml.dumps({
                'changes': attr.asdict(tool_settings)
            })
        )

    return tool_settings


@attr.s
class Project(object):
    releases_directory = attr.ib()
    repository = attr.ib(default=None)
    bumpversion = attr.ib(default=None)
    towncrier = attr.ib(default=None)

    @property
    def bumpversion_configured(self):
        return isinstance(self.bumpversion, BumpVersion)

    @property
    def towncrier_configured(self):
        return isinstance(self.towncrier, TownCrier)


@attr.s
class BumpVersion(object):
    current_version = attr.ib()
    version_files_to_replace = attr.ib(default=attr.Factory(list))

    def write_to_file(self, config_path: Path):
        bumpversion_cfg = textwrap.dedent(
            """\
            [bumpversion]
            current_version = {current_version}

            """
        )
        bumpversion_files = '\n'.join([
            '[bumpversion:file:{}]'.format(file_name)
            for file_name in self.version_files_to_replace
        ])

        config_path.write_text(
            bumpversion_cfg + bumpversion_files
        )

def load_project_settings():
    changes_project_config_path = Path(PROJECT_CONFIG_FILE)

    project_settings = None
    if changes_project_config_path.exists():
        project_settings = Project(
            **(toml.load(changes_project_config_path.read_text())['changes'])
        )

    if not project_settings:
        project_settings = Project(
            releases_directory=str(Path(click.prompt(
                'Enter the directory to store your releases notes',
                DEFAULT_RELEASES_DIRECTORY,
                type=click.Path(exists=True, dir_okay=True)
            )))
        )
        # write config file
        changes_project_config_path.write_text(
            toml.dumps({
                'changes': attr.asdict(project_settings)
            })
        )

    # Initialise environment
    info('Indexing repository')
    project_settings.repository = GitRepository(
        auth_token=changes.settings.auth_token
    )

    # TODO: look in other locations / extract from bumpversion
    bumpversion_config_path = Path('.bumpversion.cfg')
    if not bumpversion_config_path.exists():
        # list of file paths
        ask_user_for_version_files = []

        done = False
        while not done:
            version_file_path = Path(click.prompt(
                'Enter a path to a file that contains a version number',
                type=click.Path(
                    exists=True,
                    dir_okay=True,
                    file_okay=True,
                    readable=True
                )
            ))
            if version_file_path == Path('.'):
                done = True
            else:
                ask_user_for_version_files.append(version_file_path)

        bumpversion = BumpVersion(
            current_version=project_settings.repository.latest_version,
            version_files_to_replace=ask_user_for_version_files,
        )
        bumpversion.write_to_file(bumpversion_config_path)

    project_settings.bumpversion = bumpversion

    return project_settings


DEFAULTS = {
    'changelog': 'CHANGELOG.md',
    'readme': 'README.md',
    'github_auth_token': None,
}


class Config:
    test_command = None
    pypi = None
    skip_changelog = None
    changelog_content = None
    repo = None

    def __init__(self, module_name, dry_run, debug, no_input, requirements,
                 new_version, current_version, repo_url, version_prefix):
        self.module_name = module_name
        # module_name => project_name => curdir
        self.dry_run = dry_run
        self.debug = debug
        self.no_input = no_input
        self.requirements = requirements
        self.new_version = (
            version_prefix + new_version
            if version_prefix
            else new_version
        )
        self.current_version = current_version


def project_config():
    """Deprecated"""
    project_name = curdir

    config_path = Path(join(project_name, PROJECT_CONFIG_FILE))

    if not exists(config_path):
        store_settings(DEFAULTS.copy())
        return DEFAULTS

    return toml.load(io.open(config_path)) or {}


def store_settings(settings):
    pass

