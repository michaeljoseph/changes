import logging

import sh

from changes import config, shell

log = logging.getLogger(__name__)


def run_tests():
    if config.arguments['--tox']:
        sh.tox()
    else:
        sh.nosetests()

    return True


def run_test_command():
    if config.arguments['--test-command']:
        test_command = config.arguments['--test-command']
        result = shell.execute(sh, tuple(test_command.split(' ')))
        log.info('Test command "%s", returned %s', test_command, result)
    return True
