import tempfile
import logging

from changes import shell

log = logging.getLogger(__name__)


def run_tests():
    command = 'nosetests'
    if arguments['--tox']:
        command = 'tox'

    if not shell.execute(command, dry_run=False):
        raise Exception('Test command failed')


def run_test_command():
    if arguments['--test-command']:
        test_command = arguments['--test-command']
        result = shell.execute(test_command, dry_run=arguments['--dry-run'])
        log.info('Test command "%s", returned %s', test_command, result)
    else:
        log.warning('Test command "%s" failed', test_command)
