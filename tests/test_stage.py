import textwrap

import responses
from plumbum.cmd import git

from changes.commands import stage
from .conftest import github_merge_commit, ISSUE_URL


@responses.activate
def test_stage(
    capsys,
    git_repo_with_merge_commit,
    with_auth_token_envvar
):

    git('tag', '0.0.2')
    github_merge_commit(112)

    responses.add(
        responses.GET,
        ISSUE_URL.format('112'),
        json={
            'number': 112,
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

    stage.stage()

    expected_output = textwrap.dedent(
        """\
        Indexing repository...
        Looking for Github Auth Token in the environment...
        Found Github Auth Token in the environment...
        Repository: michaeljoseph/test_app...
        Latest Version...
        0.0.2
        Changes...
        1 changes found since 0.0.2
        #112 The title of the pull request by @someone [bug]
        Computed release type fix from changes issue tags...
        Proposed version bump 0.0.2 => 0.0.3...
        Staging [fix] release for version 0.0.3...
        """
    )
    out, _ = capsys.readouterr()
    assert expected_output == out