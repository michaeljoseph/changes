import re
import textwrap
from collections import OrderedDict
from configparser import RawConfigParser
from os.path import exists, expanduser, expandvars, join, curdir
import io
import os
import sys

import click
from pathlib import Path

import inflect
import toml
import attr

import changes
from changes.models import GitRepository
from .commands import info, note, debug, error

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

    @classmethod
    def load(cls):
        tool_config_path = Path(str(os.environ.get(
            'CHANGES_CONFIG_FILE',
            expanduser('~/.changes') if not IS_WINDOWS else
            expandvars(r'%APPDATA%\\.changes')
        )))

        tool_settings = None
        if tool_config_path.exists():
            tool_settings = Changes(
                **(toml.load(tool_config_path.open())['changes'])
            )

        # envvar takes precedence over config file settings
        auth_token = os.environ.get(AUTH_TOKEN_ENVVAR)
        if auth_token:
            info('Found Github Auth Token in the environment')
            tool_settings = Changes(auth_token=auth_token)
        elif not (tool_settings and tool_settings.auth_token):
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
    labels = attr.ib(default=attr.Factory(dict))

    @classmethod
    def load(cls):
        repository = GitRepository(
            auth_token=changes.settings.auth_token
        )

        project_settings = configure_changes(repository)
        project_settings.repository = repository
        project_settings.bumpversion = BumpVersion.load(repository.latest_version)

        return project_settings


@attr.s
class BumpVersion(object):
    DRAFT_OPTIONS = [
        '--dry-run', '--verbose',
        '--no-commit', '--no-tag',
        '--allow-dirty',
    ]
    STAGE_OPTIONS = [
        '--verbose', '--allow-dirty',
        '--no-commit', '--no-tag',
    ]

    current_version = attr.ib()
    version_files_to_replace = attr.ib(default=attr.Factory(list))

    @classmethod
    def load(cls, latest_version):
        return configure_bumpversion(latest_version)

    @classmethod
    def read_from_file(cls, config_path: Path):
        config = RawConfigParser('')
        config.readfp(config_path.open('rt', encoding='utf-8'))

        current_version = config.get("bumpversion", 'current_version')

        filenames = []
        for section_name in config.sections():

            section_name_match = re.compile("^bumpversion:(file|part):(.+)").match(section_name)

            if not section_name_match:
                continue

            section_prefix, section_value = section_name_match.groups()

            if section_prefix == "file":
                filenames.append(section_value)

        return cls(
            current_version=current_version,
            version_files_to_replace=filenames,
        )

    def write_to_file(self, config_path: Path):
        bumpversion_cfg = textwrap.dedent(
            """\
            [bumpversion]
            current_version = {current_version}

            """
        ).format(**attr.asdict(self))

        bumpversion_files = '\n\n'.join([
            '[bumpversion:file:{}]'.format(file_name)
            for file_name in self.version_files_to_replace
        ])

        config_path.write_text(
            bumpversion_cfg + bumpversion_files
        )


def configure_changes(repository):
    changes_project_config_path = Path(PROJECT_CONFIG_FILE)
    project_settings = None
    if changes_project_config_path.exists():
        # releases_directory, labels
        project_settings = Project(
            **(toml.load(changes_project_config_path.open())['changes'])
        )

    if not project_settings:
        releases_directory = Path(click.prompt(
            'Enter the directory to store your releases notes',
            DEFAULT_RELEASES_DIRECTORY,
            type=click.Path(exists=True, dir_okay=True)
        ))

        if not releases_directory.exists():
            debug('Releases directory {} not found, creating it.'.format(releases_directory))
            releases_directory.mkdir(parents=True)

        # FIXME: GitHub(repository).labels()
        project_settings = Project(
            releases_directory=str(releases_directory),
            labels=configure_labels(repository.github_labels()),
        )
        # write config file
        changes_project_config_path.write_text(
            toml.dumps({
                'changes': attr.asdict(project_settings)
            })
        )

    return project_settings


def configure_bumpversion(latest_version):
    # TODO: look in other supported bumpversion config locations
    bumpversion = None
    bumpversion_config_path = Path('.bumpversion.cfg')
    if not bumpversion_config_path.exists():
        user_supplied_versioned_file_paths = []

        version_file_path_answer = None
        input_terminator = '.'
        while not version_file_path_answer == input_terminator:
            version_file_path_answer = click.prompt(
                'Enter a path to a file that contains a version number '
                "(enter a path of '.' when you're done selecting files)",
                type=click.Path(
                    exists=True,
                    dir_okay=True,
                    file_okay=True,
                    readable=True
                )
            )

            if version_file_path_answer != input_terminator:
                user_supplied_versioned_file_paths.append(version_file_path_answer)

        bumpversion = BumpVersion(
            current_version=latest_version,
            version_files_to_replace=user_supplied_versioned_file_paths,
        )
        bumpversion.write_to_file(bumpversion_config_path)

    return bumpversion


def configure_labels(github_labels):
    labels_keyed_by_name = {}
    for label in github_labels:
        labels_keyed_by_name[label['name']] = label

    # TODO: streamlined support for github defaults: enhancement, bug
    changelog_worthy_labels = choose_labels([
        properties['name']
        for _, properties in labels_keyed_by_name.items()
    ])

    # TODO: apply description transform in labels_prompt function
    described_labels = {}
    # auto-generate label descriptions
    for label_name in changelog_worthy_labels:
        label_properties = labels_keyed_by_name[label_name]
        # Auto-generate description as pluralised titlecase label name
        label_properties['description'] = inflect.engine().plural(label_name.title())

        described_labels[label_name] = label_properties

    return described_labels


def choose_labels(alternatives):
    """
    Prompt the user select several labels from the provided alternatives.

    At least one label must be selected.

    :param list alternatives: Sequence of options that are available to select from
    :return: Several selected labels
    """
    if not alternatives:
        raise ValueError

    if not isinstance(alternatives, list):
        raise TypeError

    choice_map = OrderedDict(
      ('{}'.format(i), value) for i, value in enumerate(alternatives, 1)
    )
    # prepend a termination option
    input_terminator = '0'
    choice_map.update({input_terminator: '<done>'})
    choice_map.move_to_end('0', last=False)

    choice_indexes = choice_map.keys()

    choice_lines = ['{} - {}'.format(*c) for c in choice_map.items()]
    prompt = '\n'.join((
        'Select labels:',
        '\n'.join(choice_lines),
        'Choose from {}'.format(', '.join(choice_indexes))
    ))

    user_choices = set()
    user_choice = None

    while not user_choice == input_terminator:
        if user_choices:
            note('Selected labels: [{}]'.format(', '.join(user_choices)))

        user_choice = click.prompt(
            prompt,
            type=click.Choice(choice_indexes),
            default=input_terminator,
        )
        done = user_choice == input_terminator
        new_selection = user_choice not in user_choices
        nothing_selected = not user_choices

        if not done and new_selection:
            user_choices.add(choice_map[user_choice])

        if done and nothing_selected:
            error('Please select at least one label')
            user_choice = None

    return user_choices

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

