import io
import logging
from os.path import exists

from plumbum.cmd import git

from changes import attributes, exceptions

log = logging.getLogger(__name__)


def report_and_raise(probe_name, probe_result, failure_msg):
    """Logs the probe result and raises on failure"""
    log.info('%s? %s' % (probe_name, probe_result))
    if not probe_result:
        raise exceptions.ProbeException(failure_msg)
    else:
        return True


def on_github():
    """on [github](https://github.com)"""
    return report_and_raise(
        'On GitHub',
        any(['github.com' in remote for remote in git('remote', '-v').split('\n')]),
        'Your package needs to be a GitHub project'
    )


def has_setup():
    """`setup.py`"""
    return report_and_raise('Has a setup.py', exists('setup.py'), 'Your project needs a setup.py')

# supports executing tests with `py.test`, `nosetests` or `tox`
TEST_RUNNERS = ['pytest', 'nose', 'tox']
def has_requirements():
    """`requirements.txt` and required requirements"""
    has_requirements = report_and_raise('Has a requirements.txt', exists(context.requirements), 'Create a requirements.txt for your project')

    requirements = io.open(context.requirements).read()
    return report_and_raise(
        'Has a test runner (%s)' % TEST_RUNNERS,
        any([runner in requirements for runner in TEST_RUNNERS]),
        'Please use one of the supported test runners (%s)' % TEST_RUNNERS
    )


def has_changelog():
    """CHANGELOG.md"""
    return report_and_raise('CHANGELOG.md', exists('CHANGELOG.md'), 'Create a CHANGELOG.md file')


def has_readme():
    """README.md"""
    return report_and_raise('README.md', exists('README.md'), 'Create a README.md file')


def has_metadata(context):
    """`<module_name>/__init__.py` with `__version__` and `__url__`"""
    init_path = '%s/__init__.py' % context.module_name
    has_metadata = (
        exists(init_path) and
        attributes.has_attribute(context.module_name, '__version__') and
        attributes.has_attribute(context.module_name, '__url__')
    )
    return report_and_raise(
        'Has module metadata',
        has_metadata,
        'Your %s/__init__.py must contain __version__ and __url__ attributes'
    )


def probe_project(context):
    """
    Check if the project meets `changes` requirements.
    Complain and exit otherwise.
    """
    log.info('Checking project for changes requirements.')
    if (on_github() and has_setup() and
        has_readme() and has_changelog() and has_metadata(context) and
        has_requirements):
        return True
    return False
