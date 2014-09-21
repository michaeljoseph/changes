import io
import logging
from os.path import exists

from plumbum.cmd import git

from changes import attributes

log = logging.getLogger(__name__)


def probe_project(context):
    """
    Check if the project meets `changes` requirements
    """
    log.info('Checking project for changes requirements.')
    # on [github](https://github.com)
    git_remotes = git('remote', '-v').split('\n')
    on_github = any(['github.com' in remote for remote in git_remotes])
    log.info('On Github? %s', on_github)

    # `setup.py`
    setup = exists('setup.py')
    log.info('setup.py? %s', setup)

    # `requirements.txt`
    has_requirements = exists(context.requirements)
    if has_requirements:
        # supports executing tests with `py.test`, `nosetests` or `tox`
        requirements = io.open(context.requirements).read()
        test_runners = ['pytest', 'nose', 'tox']
        runs_tests = any([runner in requirements for runner in test_runners])
        log.info('Runs tests? %s' % runs_tests)

    # `CHANGELOG.md`
    has_changelog = exists('CHANGELOG.md')
    log.info('CHANGELOG.md? %s', has_changelog)

    # `<module_name>/__init__.py` with `__version__` and `__url__`
    init_path = '%s/__init__.py' % context.module_name
    has_metadata = (
        exists(init_path) and
        attributes.has_attribute(context.module_name, '__version__') and
        attributes.has_attribute(context.module_name, '__url__')
    )
    log.info('Has module metadata? %s', has_metadata)

    if not (on_github and setup and has_changelog and has_metadata and
            has_requirements and runs_tests):
        raise Exception('Project does not meet `changes` requirements')
    else:
        return True
