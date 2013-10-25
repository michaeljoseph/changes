import logging

from changes import config
from changes.compat import check_output, CalledProcessError

log = logging.getLogger(__name__)


def handle_dry_run(function, *args):
    if not config.arguments.get('--dry-run', True):
        return function(*args)
    else:
        log.debug('dry run of %s %s, skipping' % (function, args))
        return True


def execute(command, dry_run=True):
    if not dry_run:
        try:
            return check_output(command.split(' ')).split('\n')
        except CalledProcessError as e:
            log.debug('return code: %s, output: %s', e.returncode, e.output)
            return False
    else:
        log.debug('dry run of %s, skipping' % command)
        return True
