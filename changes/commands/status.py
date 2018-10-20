import changes

from . import highlight, info, note


def status():
    repository = changes.project_settings.repository

    release = changes.release_from_pull_requests()

    info('Status [{}/{}]'.format(repository.owner, repository.repo))

    info('Repository: ' + highlight('{}/{}'.format(repository.owner, repository.repo)))

    info('Latest Version')
    note(repository.latest_version)

    info('Changes')
    unreleased_changes = repository.pull_requests_since_latest_version
    note(
        '{} changes found since {}'.format(
            len(unreleased_changes), repository.latest_version
        )
    )

    for pull_request in unreleased_changes:
        note(
            '#{} {} by @{}{}'.format(
                pull_request.number,
                pull_request.title,
                pull_request.author,
                ' [{}]'.format(','.join(pull_request.label_names))
                if pull_request.label_names
                else '',
            )
        )

    if unreleased_changes:
        info(
            'Computed release type {} from changes issue tags'.format(
                release.release_type
            )
        )
        info(
            'Proposed version bump {} => {}'.format(
                repository.latest_version, release.version
            )
        )
