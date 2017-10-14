from os.path import exists, join, curdir
import io

import click
import giturlparse
from path import Path

from plumbum.cmd import git
import toml
from invoke import run

CONFIG_FILE = '.changes.toml'
CONFIG_FILES = [
    '.changes.toml',
    'pyproject.toml',
    'setup.cfg',
]
DOCS = [
    'CHANGELOG.md',
    'README.md',
]
DEFAULTS = {
    'changelog': 'CHANGELOG.md',
    'readme': 'README.md',
    'github_auth_token': None,
}


class Config:
    test_command = None
    pypi = None
    skip_changelog = None
    changelog_content = None
    repo = None

    def __init__(self, module_name, dry_run, debug, no_input, requirements,
                 new_version, current_version, repo_url, version_prefix):
        self.module_name = module_name
        # module_name => project_name => curdir
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


def project_config():
    """Deprecated"""
    project_name = curdir

    config_path = Path(join(project_name, CONFIG_FILE))

    if not exists(config_path):
        store_settings(DEFAULTS.copy())
        return DEFAULTS

    return toml.load(io.open(config_path)) or {}


def load_settings():
    return project_config()


def store_settings(settings):
    config_path = Path(join(curdir, CONFIG_FILE))

    with click.open_file(config_path, 'w') as f:
        f.write(toml.dumps(settings))


# def bumpversion_settings():
#     pass
# def towncrier_settings():
#     fn = join(curdir, "pyproject.toml")
#     if not exists(fn):
#         return None
#     with open(fn, 'r') as conffile:
#         config = toml.load(conffile)
#
#     if 'tool' not in config or 'package' not in config['tool']['towncrier']:
#         raise NotConfigured(
#             'No [tool.towncrier] section or '
#             "the towncrier section has no required 'package' key."
#         )
#     return config['tool']['towncrier']
