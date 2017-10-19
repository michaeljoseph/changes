from datetime import date
from pathlib import Path

import bumpversion
import pkg_resources
from jinja2 import Template

import changes
from changes.config import BumpVersion
from changes.models import Release
from . import info, error, note
from .status import status


def stage(draft, release_name=None, release_description=None):
    repository, bumpversion_part, release_type, proposed_version = status()

    if not repository.changes_since_last_version:
        error("There aren't any changes to release!")
        return

    info('Staging [{}] release for version {}'.format(
        release_type,
        proposed_version
    ))

    bumpversion_arguments = (
        BumpVersion.DRAFT_OPTIONS if draft
        else BumpVersion.STAGE_OPTIONS
    )
    bumpversion_arguments += [bumpversion_part]

    info('Running: bumpversion {}'.format(
        ' '.join(bumpversion_arguments)
    ))

    try:
        bumpversion.main(bumpversion_arguments)
    except bumpversion.WorkingDirectoryIsDirtyException as err:
        error(err)
        raise

    info('Generating Release')
    # prepare context for changelog documentation
    project_labels = changes.project_settings.labels
    for label, properties in project_labels.items():
        pull_requests_with_label = [
            pull_request
            for pull_request in repository.changes_since_last_version
            if label in pull_request.labels
        ]

        project_labels[label]['pull_requests'] = pull_requests_with_label

    release = Release(
        name=release_name,
        release_date=date.today().isoformat(),
        version=proposed_version,
        description=release_description,
        changes=project_labels,
    )

    info('Loading template...')
    # TODO: if project_settings.release_notes_template is None
    release_notes_template = pkg_resources.resource_string(
        changes.__name__,
        'templates/release_notes_template.md'
    ).decode('utf8')

    release_notes = Template(release_notes_template).render(release=release)
    # TODO: jinja2.exceptions.UndefinedError
    
    releases_directory = Path(changes.project_settings.releases_directory)
    if not releases_directory.exists():
        releases_directory.mkdir(parents=True)
    release_notes_path = releases_directory.joinpath(
        '{}.md'.format(release.version)
    )
    if not draft:
        release_notes_path.write_text(release_notes)
    else:
        note(release_notes)
