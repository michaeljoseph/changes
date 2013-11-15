import logging
from os.path import exists

import sh

from changes import attributes, config

log = logging.getLogger(__name__)

REQUIREMENTS = 'requirements.txt'


def has_requirement(dependency, requirements_contents):
    return any(
        [dependency in requirement for requirement in requirements_contents]
    )


def probe_project(module_name):
    """
    Check if the project meets `changes` requirements
    """
    log.info('Checking project for changes requirements.')
    # on [github](https://github.com)
    git_remotes = sh.git.remote('-v')
    on_github = any(['github.com' in remote for remote in git_remotes])
    log.info('On Github? %s', on_github)

    # `setup.py`
    setup = exists('setup.py')
    log.info('setup.py? %s', setup)

    # `requirements.txt`
    requirements = config.arguments.get('--requirements') or REQUIREMENTS
    has_requirements = exists(requirements)
    log.info('%s? %s', requirements, has_requirements)
    if has_requirements:
        requirements_contents = open(requirements).readlines()

        # supports executing tests with `nosetests` or `tox`
        runs_tests = (
            has_requirement('nose', requirements_contents) or
            has_requirement('tox', requirements_contents)
        )
        log.info('Runs tests? %s' % runs_tests)

    # `CHANGELOG.md`
    has_changelog = exists('CHANGELOG.md')
    log.info('CHANGELOG.md? %s', has_changelog)

    # `<module_name>/__init__.py` with `__version__` and `__url__`
    init_path = '%s/__init__.py' % module_name
    has_metadata = (
        exists(init_path) and
        attributes.has_attribute(module_name, '__version__') and
        attributes.has_attribute(module_name, '__url__')
    )
    log.info('Has module metadata? %s', has_metadata)

    return (on_github and setup and has_changelog and has_metadata and
            has_requirements and runs_tests)
