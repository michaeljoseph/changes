from os.path import exists, join
import io

import click
from giturlparse import parse
from path import path
from plumbum.cmd import git
from plumbum import local
import yaml

CONFIG_FILE = '.changes'
DEFAULTS = {
    'changelog': 'CHANGELOG.md',
    'readme': 'README.md',
    'gh_token': None,
}


class CLI(object):
    test_command = None
    pypi = None
    skip_changelog = None
    changelog_content = None
    parsed_repo = None

    def __init__(self, module_name, dry_run, debug, no_input, requirements,
                 new_version, current_version, repo_url, version_prefix):
        self.module_name = module_name
        self.dry_run = dry_run
        self.debug = debug
        self.no_input = no_input
        self.requirements = requirements
        self.new_version = (
            version_prefix + new_version
            if version_prefix
            else new_version
        )
        self.current_version = current_version
        self.repo_url = repo_url


    @property
    def repo(self):
        return self.parsed_repo.repo

    @property
    def owner(self):
        return self.parsed_repo.owner

    @property
    def github(self):
        return self.parsed_repo.github

    @property
    def bitbucket(self):
        return self.parsed_repo.bitbucket


    @property
    def parsed_repo(self):
        with local.cwd(local.cwd / self.module_name):
            return parse(git('config --get remote.origin.url'.split(' ')))


def project_config(module_name):
    config = {}
    config_path = path(join(module_name, CONFIG_FILE))

    if not exists(config_path):
        store_settings(module_name, DEFAULTS.copy())

    config = yaml.load(io.open(config_path))
    return config or {}


def store_settings(module_name, settings):
    config_path = path(join(module_name, CONFIG_FILE))
    with click.open_file(config_path, 'w') as f:
        f.write(yaml.dump(settings, default_flow_style=False))
