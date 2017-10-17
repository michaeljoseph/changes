import textwrap
from pathlib import Path

import responses
from plumbum.cmd import git

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
        """
    )
    out, _ = capsys.readouterr()
    assert expected_output == out

    assert Path('.bumpversion.cfg').exists()
    # assert Path('pyproject.toml').exists()


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

    stage.stage(draft=False)

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
        """
    )
    out, _ = capsys.readouterr()
    assert expected_output == out
