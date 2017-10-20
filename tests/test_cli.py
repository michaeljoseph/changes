import textwrap
from pathlib import Path

from click.testing import CliRunner

import changes
from changes.cli import main
from .conftest import AUTH_TOKEN_ENVVAR


def test_version():
    runner = CliRunner()
    result = runner.invoke(main, ['--version'])
    assert result.exit_code == 0
    assert result.output == 'changes %s\n' % changes.__version__


# def test_init_cli(git_repo_with_merge_commit, tmpdir):
#     changes_config_path = Path(str(tmpdir.join('.changes')))
#     changes_config_path.write_text(textwrap.dedent(
#         """\
#         [changes]
#         auth_token = "foo"
#         """
#     ))
#
#     result = CliRunner().invoke(
#         main,
#         ['init'],
#         env={
#             'CHANGES_CONFIG_FILE': str(changes_config_path),
#             # AUTH_TOKEN_ENVVAR: 'foo'
#         },
#     )
#     assert result.exit_code == 0
#
#     expected_output = textwrap.dedent(
#         """\
#         Indexing repository...
#         Looking for Github Auth Token in the environment...
#         Found Github Auth Token in the environment...
#         """
#     )
#     assert expected_output == result.output


# def test_status_cli(git_repo):
#     result = CliRunner().invoke(
#        main,
#        ['status'],
#        env={AUTH_TOKEN_ENVVAR: 'foo'},
#     )
#     assert 0 == result.exit_code
#
#     expected_output = textwrap.dedent(
#         """\
#         Indexing repository...
#         Looking for Github Auth Token in the environment...
#         Found Github Auth Token in the environment...
#         Repository: michaeljoseph/test_app...
#         Latest Version...
#         0.0.0
#         Changes...
#         0 changes found since 0.0.0
#         """
#     )
#     assert expected_output == result.output


# def test_stage_cli(git_repo, tmpdir):
#     result = CliRunner().invoke(
#        main,
#        ['stage'],
#        env={
#            AUTH_TOKEN_ENVVAR: 'foo',
#            'CHANGES_CONFIG_FILE': str(tmpdir.join('.changes')),
#        },
#     )
#     assert 0 == result.exit_code
#
#     expected_output = textwrap.dedent(
#         """\
#         Found Github Auth Token in the environment...
#         Indexing repository...
#         Repository: michaeljoseph/test_app...
#         Latest Version...
#         0.0.0
#         Changes...
#         0 changes found since 0.0.0
#         There aren't any changes to release!
#         """
#     )
#     assert expected_output == result.output
