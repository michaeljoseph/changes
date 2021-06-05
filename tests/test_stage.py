import shlex
import textwrap
from datetime import date
from pathlib import Path

import responses
from plumbum.cmd import git

import changes
from changes.commands import stage

from .conftest import (
    BUG_LABEL_JSON,
    ISSUE_URL,
    LABEL_URL,
    PULL_REQUEST_JSON,
    github_merge_commit,
)


@responses.activate
def test_stage_draft(capsys, configured):

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

    changes.initialise()
    stage.stage(draft=True)

    release_notes_path = Path(
        'docs/releases/0.0.2-{}.md'.format(date.today().isoformat())
    )
    expected_output = textwrap.dedent(
        """\
        Staging [fix] release for version 0.0.2...
        Running: bumpversion --dry-run --verbose --no-commit --no-tag --allow-dirty patch...
        Generating Release...
        Would have created {}:...
        """.format(
            release_notes_path
        )
    )

    expected_release_notes_content = [
        '# 0.0.2 ({})'.format(date.today().isoformat()),
        '',
        '## Bug',
        '* #111 The title of the pull request',
        '...',
    ]

    out, _ = capsys.readouterr()

    assert (
        expected_output.splitlines() + expected_release_notes_content
        == out.splitlines()
    )

    assert not release_notes_path.exists()


@responses.activate
def test_stage(capsys, configured):
    responses.add(
        responses.GET,
        LABEL_URL,
        json=BUG_LABEL_JSON,
        status=200,
        content_type='application/json',
    )

    github_merge_commit(111)
    responses.add(
        responses.GET,
        ISSUE_URL,
        json=PULL_REQUEST_JSON,
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
    expected_output = textwrap.dedent(
        """\
        Staging [fix] release for version 0.0.2...
        Running: bumpversion --verbose --allow-dirty --no-commit --no-tag patch...
        Generating Release...
        Writing release notes to {}...
        """.format(
            release_notes_path
        )
    )
    out, _ = capsys.readouterr()
    assert expected_output == out

    assert release_notes_path.exists()
    expected_release_notes = [
        '# 0.0.2 ({}) Icarus'.format(date.today().isoformat()),
        'The first flight',
        '## Bug',
        '* #111 The title of the pull request',
    ]
    assert expected_release_notes == release_notes_path.read_text().splitlines()

    # changelog_path = Path('CHANGELOG.md')
    # expected_changelog = [
    #     '# Changelog',
    #     '',
    #     '<!-- insert changes release notes here -->',
    #     # FIXME:
    #     '# Changelog# 0.0.2 ({}) Icarus'.format(date.today().isoformat()),
    #     'The first flight',
    #     '## Bug',
    #     '    ',
    #     '* #111 The title of the pull request',
    #     '    ',
    # ]
    # assert expected_changelog == changelog_path.read_text().splitlines()


@responses.activate
def test_stage_discard(capsys, configured):
    responses.add(
        responses.GET,
        LABEL_URL,
        json=BUG_LABEL_JSON,
        status=200,
        content_type='application/json',
    )

    github_merge_commit(111)
    responses.add(
        responses.GET,
        ISSUE_URL,
        json=PULL_REQUEST_JSON,
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

    result = git(shlex.split('-c color.status=false status --short --branch'))

    modified_files = [
        '## master',
        ' M .bumpversion.cfg',
        # ' M CHANGELOG.md',
        ' M version.txt',
        '?? docs/',
        '',
    ]
    assert '\n'.join(modified_files) == result

    stage.discard(release_name='Icarus', release_description='The first flight')

    expected_output = textwrap.dedent(
        """\
        Staging [fix] release for version 0.0.2...
        Running: bumpversion --verbose --allow-dirty --no-commit --no-tag patch...
        Generating Release...
        Writing release notes to {release_notes_path}...
        Discarding currently staged release 0.0.2...
        Running: git checkout -- version.txt .bumpversion.cfg...
        Running: rm {release_notes_path}...
        """.format(
            release_notes_path=release_notes_path
        )
    )
    out, _ = capsys.readouterr()
    assert expected_output == out

    result = git(shlex.split('-c color.status=false status --short --branch'))

    modified_files = ['## master', '']
    assert '\n'.join(modified_files) == result


@responses.activate
def test_stage_discard_nothing_staged(capsys, configured):

    changes.initialise()

    stage.discard(release_name='Icarus', release_description='The first flight')

    expected_output = textwrap.dedent(
        """\
        No staged release to discard...
        """
    )
    out, _ = capsys.readouterr()
    assert expected_output == out
