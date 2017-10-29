from pathlib import Path

import click
from datetime import date

import changes
from changes.commands import error, info
from changes.config import BumpVersion
from changes.models import changes_to_release_type, Release, GitRepository


def publish():
    bumpversion_part, release_type, proposed_version = changes_to_release_type(
        changes.project_settings.repository
    )
    release = Release(
        release_date=date.today().isoformat(),
        version=str(proposed_version),
    )

    if release.version == str(changes.project_settings.repository.latest_version):
        info('No staged release to publish')
        return

    info('Publishing release {}'.format(release.version))

    files_to_add = BumpVersion.read_from_file(Path('.bumpversion.cfg')).version_files_to_replace
    release_notes_path = Path(changes.project_settings.releases_directory).joinpath(
        '{}.md'.format(release.version)
    )

    files_to_add += [
        '.bumpversion.cfg',
        str(release_notes_path)
    ]

    info('Running: git add {}'.format(' '.join(files_to_add)))
    GitRepository.add(files_to_add)

        # tag => release format string

        # git push --tags

        # github release [artifacts?]

    # Release done

    # Verifying

    # install from release (gh
    #     verify release
