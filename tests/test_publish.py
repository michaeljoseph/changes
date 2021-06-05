import shlex
import textwrap
from datetime import date
from pathlib import Path

import pytest
import responses
from plumbum.cmd import git

import changes
from changes.commands import publish, stage

from .conftest import (
    BUG_LABEL_JSON,
    ISSUE_URL,
    LABEL_URL,
    PULL_REQUEST_JSON,
    RELEASES_URL,
    github_merge_commit,
)


@pytest.fixture
def answer_prompts(mocker):
    prompt = mocker.patch('changes.commands.publish.click.confirm', autospec=True)
    prompt.side_effect = ['y']


def test_publish_no_staged_release(capsys, configured):
    changes.initialise()
    publish.publish()

    expected_output = textwrap.dedent(
        """\
        No staged release to publish...
        """
    )
    out, _ = capsys.readouterr()
    assert expected_output == out


@responses.activate
def test_publish(capsys, configured, answer_prompts):

    github_merge_commit(111)
    responses.add(
        responses.GET,
        ISSUE_URL,
        json=PULL_REQUEST_JSON,
        status=200,
        content_type='application/json',
    )
    responses.add(
        responses.GET,
        LABEL_URL,
        json=BUG_LABEL_JSON,
        status=200,
        content_type='application/json',
    )
    responses.add(
        responses.POST,
        RELEASES_URL,
        json={'upload_url': 'foo'},
        status=200,
        content_type='application/json',
    )

    changes.initialise()
    stage.stage(
        draft=False, release_name='Icarus', release_description='The first flight'
    )

    release_notes_path = Path(
        'docs/releases/0.0.2-{}-Icarus.md'.format(date.today().isoformat())
    )
    assert release_notes_path.exists()

    publish.publish()

    pre = textwrap.dedent(
        """\
        Staging [fix] release for version 0.0.2...
        Running: bumpversion --verbose --allow-dirty --no-commit --no-tag patch...
        Generating Release...
        Writing release notes to {release_notes_path}...
        Publishing release 0.0.2...
        Running: git add version.txt .bumpversion.cfg {release_notes_path}...
        Running: git commit --message="# 0.0.2 ({release_date}) Icarus
        """.format(
            release_notes_path=release_notes_path, release_date=date.today().isoformat()
        )
    ).splitlines()

    expected_release_notes_content = [
        'The first flight',
        '## Bug',
        '* #111 The title of the pull request',
    ]

    post = textwrap.dedent(
        """\
        "...
        Running: git tag 0.0.2...
        Running: git push --tags...
        Creating GitHub Release...
        Published release 0.0.2...
        """
    ).splitlines()

    out, _ = capsys.readouterr()

    assert pre + expected_release_notes_content + post == out.splitlines()

    last_commit = git(shlex.split('show --name-only'))
    expected_files = ['version.txt', '.bumpversion.cfg', release_notes_path]
    assert [
        expected_file
        for expected_file in expected_files
        if str(expected_file) in last_commit
    ]

    assert '0.0.2' in git(shlex.split('tag --list'))

    assert release_notes_path.exists()
    expected_release_notes = [
        '# 0.0.2 ({}) Icarus'.format(date.today().isoformat()),
        'The first flight',
        '## Bug',
        '* #111 The title of the pull request',
    ]
    assert expected_release_notes == release_notes_path.read_text().splitlines()
