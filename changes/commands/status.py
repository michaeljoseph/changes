from changes.commands import info, note, highlight
from changes.commands.init import init


class Release:
    BREAKING_CHANGE = 1
    FEATURE = 2
    FIX = 3


def changes_to_release_type(repository):
    pull_request_labels = set()
    changes = repository.changes_since_last_version

    for change in changes:
        for label in change.labels:
            pull_request_labels.add(label)

    change_descriptions = [
        '\n'.join([change.title, change.description]) for change in changes
    ]

    current_version = repository.latest_version
    if 'BREAKING CHANGE' in change_descriptions:
        return Release.BREAKING_CHANGE, current_version.next_major()
    elif 'enhancement' in pull_request_labels:
        return Release.BREAKING_CHANGE, current_version.next_minor()
    elif 'bug' in pull_request_labels:
        return Release.BREAKING_CHANGE, current_version.next_patch()


def status():
    repository = init()

    info(
        'Repository: ' +
        highlight(
            '{}/{}'.format(repository.owner, repository.repo),
        )
    )

    info('Latest Version')
    note(repository.latest_version)

    info('Changes')
    note('{} changes found since {}'.format(
        len(repository.changes_since_last_version),
        repository.latest_version,
    ))

    for pull_request in repository.changes_since_last_version:
        note('#{} {} by @{}{}'.format(
            pull_request.number,
            pull_request.title,
            pull_request.author,
            ' [{}] '.format(
                ','.join(pull_request.labels)
            ) if pull_request.labels else '',
        ))

    release_type, proposed_version = changes_to_release_type(repository)
    info('Computed release type {} from changes issue tags'.format(release_type))
    info('Proposed version bump {} => {}'.format(
        repository.latest_version, proposed_version
    ))
