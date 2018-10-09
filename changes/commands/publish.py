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

    info('Publishing release {}'.format(release.version))

    files_to_add = BumpVersion.read_from_file(
        Path('.bumpversion.cfg')
    ).version_files_to_replace
    files_to_add += ['.bumpversion.cfg', str(release.release_file_path)]

    info('Running: git add {}'.format(' '.join(files_to_add)))
    repository.add(files_to_add)

    commit_message = release.release_file_path.read_text(encoding='utf-8')
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
