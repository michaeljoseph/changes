import logging

import iterpipes

log = logging.getLogger(__name__)


def execute(command, dry_run=True):
    log.debug('executing %s', command)
    if not dry_run:
        try:
            return [result for result in iterpipes.linecmd(command)(None)]
        except iterpipes.CalledProcessError, e:
            log.debug('return code: %s, output: %s', e.returncode, e.output)
            return False
    else:
        return True
