from pathlib import Path

import click

import changes
from changes.commands import info
from changes.models import BumpVersion


def publish():
    repository = changes.project_settings.repository

    release = changes.release_from_pull_requests()

    if release.version == str(repository.latest_version):
        info('No staged release to publish')
        return

    info(f'Publishing release {release.version}')

    files_to_add = BumpVersion.read_from_file(
        Path('.bumpversion.cfg')
    ).version_files_to_replace
    files_to_add += ['.bumpversion.cfg', str(release.release_file_path)]

    info(f"Running: git add {' '.join(files_to_add)}")
    repository.add(files_to_add)

    commit_message = release.release_file_path.read_text(encoding='utf-8')
    info(f'Running: git commit --message="{commit_message}"')
    repository.commit(commit_message)

    info(f'Running: git tag {release.version}')
    repository.tag(release.version)

    if click.confirm(f'Happy to publish release {release.version}'):
        info('Running: git push --tags')
        repository.push()

        info('Creating GitHub Release')
        repository.create_release(release)

        info(f'Published release {release.version}')
