import difflib
from pathlib import Path

import bumpversion
import click
import pkg_resources
from jinja2 import Template

import changes
from changes.models import BumpVersion, Release

from . import STYLES, debug, error, info


def discard(release_name='', release_description=''):
    repository = changes.project_settings.repository

    release = changes.release_from_pull_requests()
    if release.version == str(repository.latest_version):
        info('No staged release to discard')
        return

    info('Discarding currently staged release {}'.format(release.version))

    bumpversion = BumpVersion.read_from_file(Path('.bumpversion.cfg'))
    git_discard_files = bumpversion.version_files_to_replace + [
        # 'CHANGELOG.md',
        '.bumpversion.cfg'
    ]

    info('Running: git {}'.format(' '.join(['checkout', '--'] + git_discard_files)))
    repository.discard(git_discard_files)

    if release.release_file_path.exists():
        info('Running: rm {}'.format(release.release_file_path))
        release.release_file_path.unlink()


def stage(draft, release_name='', release_description=''):
    repository = changes.project_settings.repository

    release = changes.release_from_pull_requests()
    release.name = release_name
    release.description = release_description

    if not repository.pull_requests_since_latest_version:
        error("There aren't any changes to release since {}".format(release.version))
        return

    info(
        'Staging [{}] release for version {}'.format(
            release.release_type, release.version
        )
    )

    # Bumping versions
    if BumpVersion.read_from_file(Path('.bumpversion.cfg')).current_version == str(
        release.version
    ):
        info('Version already bumped to {}'.format(release.version))
    else:
        bumpversion_arguments = (
            BumpVersion.DRAFT_OPTIONS if draft else BumpVersion.STAGE_OPTIONS
        ) + [release.bumpversion_part]

        info('Running: bumpversion {}'.format(' '.join(bumpversion_arguments)))
        bumpversion.main(bumpversion_arguments)

    # Release notes generation
    info('Generating Release')
    release.notes = Release.generate_notes(
        changes.project_settings.labels, repository.pull_requests_since_latest_version
    )

    # TODO: if project_settings.release_notes_template is None
    release_notes_template = pkg_resources.resource_string(
        changes.__name__, 'templates/release_notes_template.md'
    ).decode('utf8')

    release_notes = Template(release_notes_template).render(release=release)

    releases_directory = Path(changes.project_settings.releases_directory)
    if not releases_directory.exists():
        releases_directory.mkdir(parents=True)

    release_notes_path = releases_directory.joinpath(
        '{}.md'.format(release.release_note_filename)
    )

    if draft:
        info('Would have created {}:'.format(release_notes_path))
        debug(release_notes)
    else:
        info('Writing release notes to {}'.format(release_notes_path))
        if release_notes_path.exists():
            release_notes_content = release_notes_path.read_text(encoding='utf-8')
            if release_notes_content != release_notes:
                info(
                    '\n'.join(
                        difflib.unified_diff(
                            release_notes_content.splitlines(),
                            release_notes.splitlines(),
                            fromfile=str(release_notes_path),
                            tofile=str(release_notes_path),
                        )
                    )
                )
                if click.confirm(
                    click.style(
                        '{} has modified content, overwrite?'.format(
                            release_notes_path
                        ),
                        **STYLES['error']
                    )
                ):
                    release_notes_path.write_text(release_notes, encoding='utf-8')
        else:
            release_notes_path.write_text(release_notes, encoding='utf-8')
