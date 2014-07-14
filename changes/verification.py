import logging

from fabric.api import local

from changes import config, shell

log = logging.getLogger(__name__)


def run_tests():
    if config.arguments['--tox']:
        result = local('tox')
    else:
        result = local('nosetests')
    return result.succeeded


def run_test_command():
    if config.arguments['--test-command']:
        result = local(config.arguments['--test-command'])
        log.info('Test command "%s", returned %s', test_command, result)
        return result.succeeded
    return True
