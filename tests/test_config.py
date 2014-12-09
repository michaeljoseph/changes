from os.path import exists

import click

from changes import config
from . import context, setup, teardown  # noqa


def test_no_config():
    assert not exists('test_app/.changes')
    assert config.project_config('test_app') == config.DEFAULTS
    assert exists('test_app/.changes')


def test_existing_config():
    existing_config = 'foo: bar\nbaz: buzz\n'
    with click.open_file('test_app/.changes', 'w') as f:
        f.write(existing_config)
    assert config.project_config('test_app') == {'foo': 'bar', 'baz': 'buzz'}


def test_malformed_config_returns_dict():
    with click.open_file('test_app/.changes', 'w') as f:
        f.write('something\n\n-another thing\n')
        assert config.project_config('test_app') == {}


def test_store_settings():
    config.store_settings('test_app', dict(foo='bar'))
    assert exists('test_app/.changes')
    assert config.project_config('test_app') == dict(foo='bar')


def test_parsed_repo_url():
    assert context.owner == 'michaeljoseph'
    assert context.repo == 'test_app'
    assert context.github
    assert not context.bitbucket
