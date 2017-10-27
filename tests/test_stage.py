import textwrap
from datetime import date
from pathlib import Path

import responses

from changes.commands import init, stage
from .conftest import github_merge_commit, ISSUE_URL, LABEL_URL, PULL_REQUEST_JSON, BUG_LABEL_JSON


@responses.activate
def test_stage_draft(
    capsys,
    configured,
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
    stage.stage(draft=True)

    expected_output = textwrap.dedent(
        """\
        Staging [fix] release for version 0.0.2...
        Running: bumpversion --dry-run --verbose --no-commit --no-tag --allow-dirty patch...
        Generating Release...
        Would have created {}.md:...
        """.format(
            Path('docs').joinpath('releases').joinpath('0.0.2.md')
        )
    )

    expected_release_notes_content = [
        '# 0.0.2 ({}) '.format(date.today().isoformat()),
        '',
        '## Bug',
        '    ',
        '* #111 The title of the pull request',
        '    ',
        '...'
    ]

    out, _ = capsys.readouterr()

    assert expected_output.splitlines() + expected_release_notes_content == out.splitlines()

    assert not Path('docs/releases/0.0.2.md').exists()


@responses.activate
def test_stage(
    capsys,
    configured,
):

    responses.add(
        responses.GET,
        LABEL_URL,
        json=BUG_LABEL_JSON,
        status=200,
        content_type='application/json'
    )

    github_merge_commit(111)
    responses.add(
        responses.GET,
        ISSUE_URL.format('111'),
        json=PULL_REQUEST_JSON,
        status=200,
        content_type='application/json'
    )

    init.init()
    stage.stage(
        draft=False,
        release_name='Icarus',
        release_description='The first flight'
    )

    expected_output = textwrap.dedent(
        """\
        Staging [fix] release for version 0.0.2...
        Running: bumpversion --verbose --allow-dirty --no-commit --no-tag patch...
        Generating Release...
        Writing release notes to {}...
        """.format(
            Path('docs').joinpath('releases').joinpath('0.0.2.md')
        )
    )
    out, _ = capsys.readouterr()
    assert expected_output == out

    release_notes_path = Path('docs/releases/0.0.2.md')
    assert release_notes_path.exists()
    expected_release_notes = [
        '# 0.0.2 ({}) Icarus'.format(date.today().isoformat()),
        'The first flight',
        '## Bug',
        '    ',
        '* #111 The title of the pull request',
        '    ',
    ]
    assert expected_release_notes == release_notes_path.read_text().splitlines()

