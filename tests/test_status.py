import textwrap

import responses

import changes
from changes.commands import status
from .conftest import github_merge_commit, ISSUE_URL, LABEL_URL, BUG_LABEL_JSON, PULL_REQUEST_JSON


@responses.activate
def test_status(
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

    status.status()

    expected_output = textwrap.dedent(
        """\
        Status [michaeljoseph/test_app]...
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
        ISSUE_URL,
        json=PULL_REQUEST_JSON,
        status=200,
        content_type='application/json'
    )

    changes.initialise()
    status.status()

    expected_output = textwrap.dedent(
        """\
        Status [michaeljoseph/test_app]...
        Repository: michaeljoseph/test_app...
        Latest Version...
        0.0.1
        Changes...
        1 changes found since 0.0.1
        #111 The title of the pull request by @michaeljoseph [bug]
        Computed release type fix from changes issue tags...
        Proposed version bump 0.0.1 => 0.0.2...
        """
    )
    out, _ = capsys.readouterr()
    assert expected_output == out
