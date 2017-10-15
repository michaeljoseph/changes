from os.path import exists

import click
from click.testing import CliRunner
from plumbum.cmd import git

from changes import config
from changes.config import Config


def test_no_config():
    with CliRunner().isolated_filesystem():
        assert not exists('.changes.toml')
        assert config.load_settings() == config.DEFAULTS
        assert exists('.changes.toml')


def test_existing_config():
    with CliRunner().isolated_filesystem():
        with click.open_file('.changes.toml', 'w') as f:
            f.write(
                '[tool.changes]\n'
                'project_name = "foo"\n'
            )

        expected_config = {'tool': {'changes': {'project_name': 'foo'}}}
        assert expected_config == config.load_settings()


def test_malformed_config_returns_dict():

    with CliRunner().isolated_filesystem():
        with click.open_file('.changes.toml', 'w') as f:
            f.write('something\n\n-another thing\n')
            assert config.project_config() == {}


def test_store_settings():
    with CliRunner().isolated_filesystem():
        config.store_settings({'foo':'bar'})
        assert exists('.changes.toml')
        assert config.load_settings() == {'foo':'bar'}


def test_parsed_repo_url():
    with CliRunner().isolated_filesystem():
        git('init')
        git('remote', 'add', 'origin', 'https://github.com/michaeljoseph/test_app.git')

        context = Config(
            'something', True, True, True,
            'requirements.txt', '0.0.2', '0.0.1',
            'https://github.com/someuser/test_app', None
        )
