import textwrap

import responses

from changes.commands import status
from .conftest import github_merge_commit, ISSUE_URL, LABEL_URL


@responses.activate
def test_status(
    capsys,
    git_repo,
    configured,
):

    responses.add(
        responses.GET,
        LABEL_URL,
        json={
            'bug': {
                "id": 208045946,
                "url": "https://api.github.com/repos/michaeljoseph/test_app/labels/bug",
                "name": "bug",
                "color": "f29513",
                "default": True
            },
        },
        status=200,
        content_type='application/json'
    )

    status.status()

    expected_output = textwrap.dedent(
        """\
        Repository: michaeljoseph/test_app...
        Latest Version...
        0.0.1
        Changes...
        0 changes found since 0.0.1
        """
    )
    out, _ = capsys.readouterr()
    assert expected_output == out

    # TODO:check project config


@responses.activate
def test_status_with_changes(
    capsys,
    git_repo,
    configured,
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
    responses.add(
        responses.GET,
        LABEL_URL,
        json={
            'bug': {
                "id": 208045946,
                "url": "https://api.github.com/repos/michaeljoseph/test_app/labels/bug",
                "name": "bug",
                "color": "f29513",
                "default": True
            },
        },
        status=200,
        content_type='application/json'
    )

    status.status()

    expected_output = textwrap.dedent(
        """\
        Status [michaeljoseph/test_app]...
        Repository: michaeljoseph/test_app...
        Latest Version...
        0.0.1
        Changes...
        1 changes found since 0.0.1
        #111 The title of the pull request by @someone [bug]
        Computed release type fix from changes issue tags...
        Proposed version bump 0.0.1 => 0.0.2...
        """
    )
    out, _ = capsys.readouterr()
    assert expected_output == out
