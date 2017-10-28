"""
For testing:
mkdir /tmp/fake-push-repo
git init /tmp/fake-push-repo
git remote set-url --push origin /tmp/fake-push-repo
"""
import textwrap
from pathlib import Path

import pytest
import responses

from changes.commands import init, stage, publish
from .conftest import github_merge_commit, ISSUE_URL, LABEL_URL, PULL_REQUEST_JSON, BUG_LABEL_JSON


@pytest.fixture
def answer_prompts(mocker):
    prompt = mocker.patch(
        'changes.commands.publish.click.confirm',
        autospec=True,
    )
    prompt.side_effect = [
        'y'
    ]


def test_publish_no_staged_release(
    capsys,
    configured
):
    init.init()
    publish.publish()

    expected_output = textwrap.dedent(
        """\
        No staged release to publish...
        """
    )
    out, _ = capsys.readouterr()
    assert expected_output == out


@responses.activate
def test_publish(
    capsys,
    configured,
    answer_prompts,
):

    github_merge_commit(111)
    responses.add(
        responses.GET,
        ISSUE_URL.format('111'),
        json=PULL_REQUEST_JSON,
        status=200,
        content_type='application/json'
    )
    responses.add(
        responses.GET,
        LABEL_URL,
        json=BUG_LABEL_JSON,
        status=200,
        content_type='application/json'
    )

    init.init()
    stage.stage(
        draft=False,
        release_name='Icarus',
        release_description='The first flight'
    )
    publish.publish()

    expected_output = textwrap.dedent(
        """\
        Staging [fix] release for version 0.0.2...
        Running: bumpversion --verbose --allow-dirty --no-commit --no-tag patch...
        Generating Release...
        Writing release notes to {}...
        Publish release 0.0.2...
        """.format(
            Path('docs').joinpath('releases').joinpath('0.0.2.md')
        )
    )
    out, _ = capsys.readouterr()
    assert expected_output == out
