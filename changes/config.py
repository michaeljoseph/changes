from os.path import exists, join

import click
import yaml

CONFIG_FILE = '.changes'
DEFAULTS = {
    'changelog': 'CHANGELOG.md',
    'readme': 'README.md',
}


class CLI(object):
    test_command = None
    pypi = None
    skip_changelog = None

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


def project_config(context):
    config = {}
    config_path = join(context.module_name, CONFIG_FILE)

    # initialise config with defaults
    if not exists(config_path):
        config = DEFAULTS.copy()

        with click.open_file(config_path, 'w') as f:
            config_yaml = yaml.dump(config, default_flow_style=False)
            f.write(config_yaml)

    config = yaml.safe_load(click.open_file(config_path))
    return config or {}
