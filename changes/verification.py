import logging

import sh

from changes import config, shell

log = logging.getLogger(__name__)


def run_tests():
    if config.arguments['--tox']:
        result = sh.tox()
    else:
        result = sh.nosetests()

    if not result:
        raise Exception('Test command failed')
    else:
        return True


def run_test_command():
    if config.arguments['--test-command']:
        test_command = config.arguments['--test-command']
        result = shell.execute(sh, tuple(test_command.split(' ')))
        log.info('Test command "%s", returned %s', test_command, result)
    return True
