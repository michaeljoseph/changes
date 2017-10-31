from datetime import date
import shlex
import textwrap
from pathlib import Path

from plumbum.cmd import git
import pytest
import responses

from changes.commands import init, stage, publish
from .conftest import github_merge_commit, ISSUE_URL, LABEL_URL, PULL_REQUEST_JSON, BUG_LABEL_JSON, RELEASES_URL


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
    responses.add(
        responses.POST,
        RELEASES_URL,
        json={'upload_url': 'foo'},
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

    release_notes_path = Path('docs').joinpath('releases').joinpath('0.0.2.md')

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
            release_notes_path=release_notes_path,
            release_date=date.today().isoformat(),
        )
    ).splitlines()

    expected_release_notes_content = [
        'The first flight',
        '## Bug',
        '    ',
        '* #111 The title of the pull request',
        '    ',
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
    expected_files = [
        'version.txt',
        '.bumpversion.cfg',
        release_notes_path,
    ]
    assert [
        expected_file
        for expected_file in expected_files
        if str(expected_file) in last_commit
    ]

    assert '0.0.2' in git(shlex.split('tag --list'))
