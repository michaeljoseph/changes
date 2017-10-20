import textwrap
from datetime import date
from pathlib import Path

import responses

from changes.commands import stage
from .conftest import github_merge_commit, ISSUE_URL


@responses.activate
def test_stage_draft(
    capsys,
    git_repo,
    with_auth_token_envvar,
    patch_user_home_to_tmpdir_path,
    with_releases_directory_and_bumpversion_file_prompt,
):

    github_merge_commit(111)

    responses.add(
        responses.GET,
        ISSUE_URL.format('111'),
        json={
            'number': 111,
            'title': 'The title of the pull request',
            'body': 'An optional, longer description.',
            'user': {
                'login': 'someone'
            },
            'labels': [
                {'id': 1, 'name': 'bug'}
            ],
        },
        status=200,
        content_type='application/json'
    )

    stage.stage(draft=True)

    assert Path('.bumpversion.cfg').exists()

    expected_output = textwrap.dedent(
        """\
        Found Github Auth Token in the environment...
        Indexing repository...
        Repository: michaeljoseph/test_app...
        Latest Version...
        0.0.1
        Changes...
        1 changes found since 0.0.1
        #111 The title of the pull request by @someone [bug]
        Computed release type fix from changes issue tags...
        Proposed version bump 0.0.1 => 0.0.2...
        Staging [fix] release for version 0.0.2...
        Running: bumpversion --dry-run --verbose --no-commit --no-tag --allow-dirty patch...
        Generating Release...
        Loading template......
        """
    )

    expected_release_notes_content = [
        '# None {} 0.0.2 None'.format(date.today().isoformat()),
        '',
        '## Bug',
        '    ',
        '* #111 The title of the pull request',
        '    ',
        ''
    ]

    out, _ = capsys.readouterr()

    assert expected_output.splitlines() + expected_release_notes_content == out.splitlines()

    assert not Path('docs/releases/0.0.2.md').exists()


@responses.activate
def test_stage(
    capsys,
    git_repo,
    with_auth_token_envvar,
    patch_user_home_to_tmpdir_path,
    with_releases_directory_and_bumpversion_file_prompt,
):

    github_merge_commit(111)

    responses.add(
        responses.GET,
        ISSUE_URL.format('111'),
        json={
            'number': 111,
            'title': 'The title of the pull request',
            'body': 'An optional, longer description.',
            'user': {
                'login': 'someone'
            },
            'labels': [
                {'id': 1, 'name': 'bug'}
            ],
        },
        status=200,
        content_type='application/json'
    )

    stage.stage(draft=False, release_name='Icarus', release_description='The first flight')

    expected_output = textwrap.dedent(
        """\
        Found Github Auth Token in the environment...
        Indexing repository...
        Repository: michaeljoseph/test_app...
        Latest Version...
        0.0.1
        Changes...
        1 changes found since 0.0.1
        #111 The title of the pull request by @someone [bug]
        Computed release type fix from changes issue tags...
        Proposed version bump 0.0.1 => 0.0.2...
        Staging [fix] release for version 0.0.2...
        Running: bumpversion --verbose --no-commit --no-tag patch...
        Generating Release...
        Loading template......
        """
    )
    out, _ = capsys.readouterr()
    assert expected_output == out

    release_notes_path = Path('docs/releases/0.0.2.md')
    assert release_notes_path.exists()
    expected_release_notes = [
        '# Icarus {} 0.0.2 The first flight'.format(date.today().isoformat()),
        '',
        '## Bug',
        '    ',
        '* #111 The title of the pull request',
        '    ',
    ]
    assert expected_release_notes == release_notes_path.read_text().splitlines()

