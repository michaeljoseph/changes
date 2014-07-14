import logging

from fabric.api import local

from changes import config
from changes.compat import check_output, CalledProcessError

log = logging.getLogger(__name__)


def dry_run(command):
    if not config.arguments.get('--dry-run', True):
        return local(command, capture=False)
    else:
        log.debug('dry run of %s, skipping' % command)
    return True
