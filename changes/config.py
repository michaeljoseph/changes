CHANGELOG = 'CHANGELOG.md'
arguments = {}


class Changes(object):
    def __init__(self, module_name, dry_run, debug, no_input, requirements, new_version, current_version, repo_url):
        self.module_name = module_name
        self.dry_run = dry_run
        self.debug = debug
        self.no_input = no_input
        self.requirements = requirements
        self.new_version = new_version
        self.current_version = current_version
        self.repo_url = repo_url


def common_arguments():
    """
    Return common arguments

    :return: tuple of <module_name>, --dry-run, new_version
    """

    module_name = arguments['<module_name>']

    version_prefix = arguments.get('--version-prefix')
    new_version = arguments['new_version']

    common_arguments = (
        module_name,
        arguments['--dry-run'],
        version_prefix + new_version if version_prefix else new_version,
    )
    return common_arguments
