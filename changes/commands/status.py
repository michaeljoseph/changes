from changes.commands import info, note, highlight
from changes.commands.init import init


class Release:
    NO_CHANGE = 'nochanges'
    BREAKING_CHANGE = 'breaking'
    FEATURE = 'feature'
    FIX = 'fix'


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
        return Release.FEATURE, current_version.next_minor()
    elif 'bug' in pull_request_labels:
        return Release.FIX, current_version.next_patch()
    else:
        return Release.NO_CHANGE, current_version

    return None


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

    if unreleased_changes:
        release_type, proposed_version = changes_to_release_type(repository)
        info('Computed release type {} from changes issue tags'.format(release_type))
        info('Proposed version bump {} => {}'.format(
            repository.latest_version, proposed_version
        ))
