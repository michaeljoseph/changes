import logging
from os.path import exists

from changes import attributes, shell

log = logging.getLogger(__name__)


def has_requirement(dependency, requirements_contents):
    return any(
        [dependency in requirement for requirement in requirements_contents]
    )


def probe_project(app_name):
    """
    Check if the project meets `changes` requirements
    """
    log.info('Checking project for changes requirements..self.')
    # on [github](https://github.com)
    git_remotes = shell.execute('git remote -v', dry_run=False)
    on_github = any(['github.com' in remote for remote in git_remotes])
    log.info('On Github? %s', on_github)

    # `setup.py`
    setup = exists('setup.py')
    log.info('setup.py? %s', setup)

    # `requirements.txt`
    has_requirements = exists('requirements.txt')
    log.info('requirements.txt? %s', setup)
    requirements_contents = open('requirements.txt').readlines()

    # `CHANGELOG.md`
    has_changelog = exists('CHANGELOG.md')
    log.info('CHANGELOG.md? %s', has_changelog)

    # `<app_name>/__init__.py` with `__version__` and `__url__`
    init_path = '%s/__init__.py' % app_name
    has_metadata = (
        exists(init_path) and
        attributes.has_attribute(app_name, '__version__') and
        attributes.has_attribute(app_name, '__url__')
    )
    log.info('Has module metadata? %s', has_metadata)

    # supports executing tests with `nosetests` or `tox`
    log.debug(requirements_contents)
    runs_tests = (
        has_requirement('nose', requirements_contents) or
        has_requirement('tox', requirements_contents)
    )
    log.info('Runs tests? %s' % runs_tests)

    return (on_github and setup and has_changelog and has_metadata and
            has_requirements and runs_tests)
