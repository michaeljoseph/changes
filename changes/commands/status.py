import changes

from . import highlight, info, note


def status():
    repository = changes.project_settings.repository

    release = changes.release_from_pull_requests()

    info(f'Status [{repository.owner}/{repository.repo}]')

    info(f"Repository: {highlight(f'{repository.owner}/{repository.repo}')}")

    info('Latest Version')
    note(repository.latest_version)

    info('Changes')
    unreleased_changes = repository.pull_requests_since_latest_version
    note(
        f'{len(unreleased_changes)} changes found since {repository.latest_version}'
    )


    for pull_request in unreleased_changes:
        note(
            '#{} {} by @{}{}'.format(
                pull_request.number,
                pull_request.title,
                pull_request.author,
                f" [{','.join(pull_request.label_names)}]"
                if pull_request.label_names
                else '',
            )
        )


    if unreleased_changes:
        info(f'Computed release type {release.release_type} from changes issue tags')
        info(f'Proposed version bump {repository.latest_version} => {release.version}')
