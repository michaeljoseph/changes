import json

import responses

from changes import packaging, vcs
from . import context, setup, teardown


def test_commit_version_change():
    vcs.commit_version_change(context)

def test_tag_and_push():
    vcs.tag_and_push(context)

@responses.activate
def test_github_release():
    responses.add(
        responses.POST,
        'https://api.github.com/repos/michaeljoseph/test_app/releases',
        body=json.dumps(dict(
            id='release-id',
            upload_url='http://upload.url.com/'
        )),
        status=201,
        content_type='application/json'
    )
    upload_url = vcs.create_github_release(context, 'gh-token', 'Description')
    assert upload_url == 'http://upload.url.com/'

@responses.activate
def test_upload_release_distributions():
    context.dry_run = False
    distributions = packaging.build_distributions(context)
    context.dry_run = True
    for distribution in distributions:
        responses.add(
            responses.POST,
            'http://upload.url.com/',
            status=201,
            content_type='application/json'
        )
    vcs.upload_release_distributions(
        context,
        'gh-token',
        distributions,
        'http://upload.url.com/',
    )
