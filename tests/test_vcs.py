import json

from mock import call
import responses
from click.testing import CliRunner
from changes import packaging, vcs
from . import context
from plumbum.cmd import git


def test_commit_version_change(mocker):
    with CliRunner().isolated_filesystem():
        dry_run = mocker.patch('changes.shell.dry_run')
        vcs.commit_version_change(context)
        dry_run.assert_has_calls([
            call('git commit --message="0.0.2" test_app/__init__.py CHANGELOG.md', True),
            call('git push', True)
        ])


def test_tag_and_push(mocker):
    with CliRunner().isolated_filesystem():
        dry_run = mocker.patch('changes.shell.dry_run')
        probe = mocker.patch('changes.probe.has_signing_key')
        probe.return_value = False

        vcs.tag_and_push(context)
        dry_run.assert_has_calls([
            call('git tag --annotate 0.0.2 --message="0.0.2"', True),
            call('git push --tags', True)
        ])


import pytest
@pytest.mark.skip('requires changelog')
@responses.activate
def test_github_release():
    with CliRunner().isolated_filesystem():
        git('init')
        git('remote', 'add', 'origin', 'https://github.com/michaeljoseph/test_app.git')

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



@pytest.mark.skip('requires changelog')
@responses.activate
def test_upload_release_distributions():
    context.dry_run = False
    distributions = packaging.build_distributions(context)
    context.dry_run = True
    for _ in distributions:
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


@pytest.mark.skip('requires changelog')
def test_signed_tag(mocker):
    dry_run = mocker.patch('changes.shell.dry_run')
    probe = mocker.patch('changes.probe.has_signing_key')
    probe.return_value = True

    vcs.tag_and_push(context)
    dry_run.assert_has_calls([
        'git tag --sign 0.0.2 --message="0.0.2"',
        # call('git tag --sign 0.0.2 --message="0.0.2"', True),
        'git push --tags',
        # call('git push --tags', True)
    ])
