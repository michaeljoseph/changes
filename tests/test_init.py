import os
import textwrap

import pytest
from plumbum.cmd import git

from changes.commands import init
from .conftest import AUTH_TOKEN_ENVVAR


@pytest.fixture
def init_prompts(mocker):
    _ = mocker.patch(
        'changes.config.click.launch',
        autospec=True,
    )

    prompt = mocker.patch(
        'changes.config.click.prompt',
        autospec=True,
    )
    prompt.side_effect = [
        'foo',
        'docs/releases',
        'test_app/__init__.py',
        '.'
    ]

    prompt = mocker.patch(
        'changes.config.read_user_choices',
        autospec=True
    )
    prompt.return_value = ['enhancement', 'bug']

    saved_token = None
    if os.environ.get(AUTH_TOKEN_ENVVAR):
        saved_token = os.environ[AUTH_TOKEN_ENVVAR]
        del os.environ[AUTH_TOKEN_ENVVAR]

    yield

    if saved_token:
        os.environ[AUTH_TOKEN_ENVVAR] = saved_token


def test_init_prompts_for_auth_token_and_writes_tool_config(
    capsys,
    git_repo,
    patch_user_home_to_tmpdir_path,
    init_prompts,
):

    init.init()

    assert patch_user_home_to_tmpdir_path.exists()
    expected_config = textwrap.dedent(
        """\
        [changes]
        auth_token = "foo"
        """
    )
    assert expected_config == patch_user_home_to_tmpdir_path.read_text()

    expected_output = textwrap.dedent(
        """\
        No auth token found, asking for it...
        You need a Github Auth Token for changes to create a release.
        Indexing repository...
        """
    )
    out, _ = capsys.readouterr()
    assert expected_output == out


def test_init_finds_auth_token_in_environment(
    capsys,
    git_repo,
    with_auth_token_envvar,
    patch_user_home_to_tmpdir_path,
    with_releases_directory_and_bumpversion_file_prompt,
):

    init.init()

    assert patch_user_home_to_tmpdir_path.exists()
    expected_config = textwrap.dedent(
        """\
        [changes]
        auth_token = "foo"
        """
    )
    assert expected_config == patch_user_home_to_tmpdir_path.read_text()

    expected_output = textwrap.dedent(
        """\
        Found Github Auth Token in the environment...
        Indexing repository...
        """
    )
    out, _ = capsys.readouterr()
    assert expected_output == out
