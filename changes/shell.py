import subprocess
import logging

log = logging.getLogger(__name__)


def execute(command, dry_run=True):
    log.debug('executing %s', command)
    if not dry_run:
        try:
            return subprocess.check_output(command.split(' ')).split('\n')
        except subprocess.CalledProcessError, e:
            log.debug('return code: %s, output: %s', e.returncode, e.output)
            return False
    else:
        return True
