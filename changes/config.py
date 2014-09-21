
class Changes(object):
    test_command = None
    pypi = None
    skip_changelog = None

    def __init__(self, module_name, dry_run, debug, no_input, requirements, new_version, current_version, repo_url, version_prefix):
        self.module_name = module_name
        self.dry_run = dry_run
        self.debug = debug
        self.no_input = no_input
        self.requirements = requirements
        self.new_version = version_prefix + new_version if version_prefix else new_version
        self.current_version = current_version
        self.repo_url = repo_url

