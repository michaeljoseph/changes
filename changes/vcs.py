import io
import logging

import click

import requests
from uritemplate import expand

from changes import shell, probe

log = logging.getLogger(__name__)

COMMIT_TEMPLATE = 'git commit --message="%s" %s/__init__.py CHANGELOG.md'
TAG_TEMPLATE = 'git tag %s %s --message="%s"'

EXT_TO_MIME_TYPE = {
    '.gz': 'application/x-gzip',
    '.whl': 'application/zip',
}


def commit_version_change(context):
    # TODO: signed commits?
    shell.dry_run(COMMIT_TEMPLATE % (context.new_version, context.module_name), context.dry_run)
    shell.dry_run('git push', context.dry_run)


def tag_and_push(context):
    """Tags your git repo with the new version number"""
    tag_option = '--annotate'
    if probe.has_signing_key(context):
        tag_option = '--sign'

    shell.dry_run(TAG_TEMPLATE % (tag_option, context.new_version, context.new_version), context.dry_run)

    shell.dry_run('git push --tags', context.dry_run)


def create_github_release(context, gh_token, description):

    params = {
        'tag_name': context.new_version,
        'name': description,
        'body': ''.join(context.changelog_content),
        'prerelease': True,
    }

    response = requests.post(
        'https://api.github.com/repos/{owner}/{repo}/releases'.format(
            owner=context.owner,
            repo=context.repo,
        ),
        auth=(gh_token, 'x-oauth-basic'),
        json=params,
    ).json()

    click.echo('Created release {response}'.format(response=response))
    return response['upload_url']


def upload_release_distributions(context, gh_token, distributions, upload_url):
    for distribution in distributions:
        click.echo('Uploading {distribution} to {upload_url}'.format(
            distribution=distribution,
            upload_url=upload_url
        ))
        response = requests.post(
            expand(upload_url, dict(name=distribution.name)),
            auth=(gh_token, 'x-oauth-basic'),
            headers={
                'content-type': EXT_TO_MIME_TYPE[distribution.ext]
            },
            data=io.open(distribution, mode='rb'),
            verify=False,
        )
        click.echo('Upload response: {response}'.format(response=response))
