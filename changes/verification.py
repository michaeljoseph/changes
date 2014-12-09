import logging

from plumbum import local, CommandNotFound

from changes import shell

log = logging.getLogger(__name__)


def get_test_runner():
    test_runners = ['tox', 'nosetests', 'py.test']
    test_runner = None
    for runner in test_runners:
        try:
            test_runner = local[runner]
        except CommandNotFound:
            continue
    return test_runner


def run_tests():
    """Executes your tests."""
    test_runner = get_test_runner()
    if test_runner:
        result = test_runner()
        log.info('Test execution returned:\n%s' % result)
        return result
    else:
        log.info('No test runner found')

    return None

def run_test_command(test_command):
    if test_command:
        result = shell.dry_run(test_command, context.dry_run)
        log.info('Test command "%s", returned %s', test_command, result)
    return True
