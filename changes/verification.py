import logging

from plumbum import CommandNotFound, local

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
    if test_runner := get_test_runner():
        result = test_runner()
        log.info('Test execution returned:\n%s' % result)
        return result
    else:
        log.info('No test runner found')

    return None


def run_test_command(context):
    if context.test_command:
        result = shell.dry_run(context.test_command, context.dry_run)
        log.info('Test command "%s", returned %s', context.test_command, result)
    return True
