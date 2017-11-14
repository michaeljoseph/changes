"""Generates a github changelog, tags and uploads your python library"""
from datetime import date
from pathlib import Path

from changes.config import Changes, Project
from changes.models import Release, ReleaseType
from changes.models.repository import GitHubRepository

__version__ = '0.7.0'
__url__ = 'https://github.com/michaeljoseph/changes'
__author__ = 'Michael Joseph'
__email__ = 'michaeljoseph@gmail.com'


from .cli import main  # noqa

settings = None
project_settings = None


def initialise():
    """
    Detects, prompts and initialises the project.

    Stores project and tool configuration in the `changes` module.
    """
    global settings, project_settings

    # Global changes settings
    settings = Changes.load()

    # Project specific settings
    project_settings = Project.load(
        GitHubRepository(
            auth_token=settings.auth_token
        )
    )


def release_from_pull_requests():
    global project_settings

    repository = project_settings.repository

    pull_requests = repository.pull_requests_since_latest_version

    labels = set([
        label_name
        for pull_request in pull_requests
        for label_name in pull_request.label_names
    ])

    descriptions = [
        '\n'.join([
            pull_request.title, pull_request.description
        ])
        for pull_request in pull_requests
    ]

    bumpversion_part, release_type, proposed_version = determine_release(
        repository.latest_version,
        descriptions,
        labels
    )

    releases_directory = Path(project_settings.releases_directory)
    if not releases_directory.exists():
        releases_directory.mkdir(parents=True)

    release = Release(
        release_date=date.today().isoformat(),
        version=str(proposed_version),
        bumpversion_part=bumpversion_part,
        release_type=release_type,
    )

    release_files = [
        release_file for release_file in releases_directory.glob('*.md')]
    if release_files:
        release_file = release_files[0]
        release.release_file_path = Path(
            project_settings.releases_directory).joinpath(release_file.name)
        release.description = release_file.read_text()

    return release


def determine_release(latest_version, descriptions, labels):
    if 'BREAKING CHANGE' in descriptions:
        return 'major', ReleaseType.BREAKING_CHANGE, latest_version.next_major()
    elif 'enhancement' in labels:
        return 'minor', ReleaseType.FEATURE, latest_version.next_minor()
    elif 'bug' in labels:
        return 'patch', ReleaseType.FIX, latest_version.next_patch()
    else:
        return None, ReleaseType.NO_CHANGE, latest_version
