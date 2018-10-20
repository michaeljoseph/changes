import re
import textwrap
from configparser import RawConfigParser
from enum import Enum
from pathlib import Path

import attr
import click


class ReleaseType(str, Enum):
    NO_CHANGE = 'no-changes'
    BREAKING_CHANGE = 'breaking'
    FEATURE = 'feature'
    FIX = 'fix'


@attr.s
class Release(object):
    release_date = attr.ib()
    version = attr.ib()
    description = attr.ib(default=attr.Factory(str))
    name = attr.ib(default=attr.Factory(str))
    notes = attr.ib(default=attr.Factory(dict))
    release_file_path = attr.ib(default='')

    bumpversion_part = attr.ib(default=None)
    release_type = attr.ib(default=None)

    @property
    def title(self):
        return '{version} ({release_date})'.format(
            version=self.version, release_date=self.release_date
        ) + ((' ' + self.name) if self.name else '')

    @property
    def release_note_filename(self):
        return '{version}-{release_date}'.format(
            version=self.version, release_date=self.release_date
        ) + (('-' + self.name) if self.name else '')

    @classmethod
    def generate_notes(cls, project_labels, pull_requests_since_latest_version):
        for label, properties in project_labels.items():
            pull_requests_with_label = [
                pull_request
                for pull_request in pull_requests_since_latest_version
                if label in pull_request.label_names
            ]

            project_labels[label]['pull_requests'] = pull_requests_with_label

        return project_labels


@attr.s
class BumpVersion(object):
    DRAFT_OPTIONS = [
        '--dry-run',
        '--verbose',
        '--no-commit',
        '--no-tag',
        '--allow-dirty',
    ]
    STAGE_OPTIONS = ['--verbose', '--allow-dirty', '--no-commit', '--no-tag']

    current_version = attr.ib()
    version_files_to_replace = attr.ib(default=attr.Factory(list))

    @classmethod
    def load(cls, latest_version):
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
                        exists=True, dir_okay=True, file_okay=True, readable=True
                    ),
                )

                if version_file_path_answer != input_terminator:
                    user_supplied_versioned_file_paths.append(version_file_path_answer)

            bumpversion = cls(
                current_version=latest_version,
                version_files_to_replace=user_supplied_versioned_file_paths,
            )
            bumpversion.write_to_file(bumpversion_config_path)

        return bumpversion

    @classmethod
    def read_from_file(cls, config_path: Path):
        config = RawConfigParser('')
        config.readfp(config_path.open('rt', encoding='utf-8'))

        current_version = config.get("bumpversion", 'current_version')

        filenames = []
        for section_name in config.sections():

            section_name_match = re.compile("^bumpversion:(file|part):(.+)").match(
                section_name
            )

            if not section_name_match:
                continue

            section_prefix, section_value = section_name_match.groups()

            if section_prefix == "file":
                filenames.append(section_value)

        return cls(current_version=current_version, version_files_to_replace=filenames)

    def write_to_file(self, config_path: Path):
        bumpversion_cfg = textwrap.dedent(
            """\
            [bumpversion]
            current_version = {current_version}

            """
        ).format(**attr.asdict(self))

        bumpversion_files = '\n\n'.join(
            [
                '[bumpversion:file:{}]'.format(file_name)
                for file_name in self.version_files_to_replace
            ]
        )

        config_path.write_text(bumpversion_cfg + bumpversion_files)
