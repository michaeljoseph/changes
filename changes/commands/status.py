import changes
from changes.models import changes_to_release_type

from . import info, note, highlight


def status():

    repository = changes.project_settings.repository

    info(
        'Repository: ' +
        highlight(
            '{}/{}'.format(repository.owner, repository.repo),
        )
    )

    info('Latest Version')
    note(repository.latest_version)

    info('Changes')
    unreleased_changes = repository.changes_since_last_version
    note('{} changes found since {}'.format(
        len(unreleased_changes),
        repository.latest_version,
    ))

    for pull_request in unreleased_changes:
        note('#{} {} by @{}{}'.format(
            pull_request.number,
            pull_request.title,
            pull_request.author,
            ' [{}]'.format(
                ','.join(pull_request.labels)
            ) if pull_request.labels else '',
        ))

    bumpversion_part, release_type, proposed_version = changes_to_release_type(repository)
    if unreleased_changes:
        info('Computed release type {} from changes issue tags'.format(release_type))
        info('Proposed version bump {} => {}'.format(
            repository.latest_version, proposed_version
        ))
