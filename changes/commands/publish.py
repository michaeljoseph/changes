from pathlib import Path

import click
from datetime import date

import changes
from changes.commands import info
from changes.config import BumpVersion
from changes.models import changes_to_release_type, Release


def publish():
    _, _, proposed_version = changes_to_release_type(
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
    repository.add(files_to_add)

    commit_message = release_notes_path.read_text(encoding='utf-8')
    info('Running: git commit --message="{}"'.format(commit_message))
    repository.commit(commit_message)

    info('Running: git tag {}'.format(release.version))
    repository.tag(release.version)

    if click.confirm('Happy to publish release {}'.format(release.version)):
        info('Running: git push --tags')
        repository.push()

        info('Creating GitHub Release')
        repository.create_release(release)

        info('Published release {}'.format(release.version))
