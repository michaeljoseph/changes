import logging

from plumbum import local

from changes import config
from changes.compat import check_output, CalledProcessError

log = logging.getLogger(__name__)


def dry_run(command):
    """Executes a shell command unless the dry run option is set"""
    if not config.arguments.get('--dry-run', True):
        cmd_parts = command.split(' ')
        return local[cmd_parts[0]](cmd_parts[1:])
    else:
        log.debug('dry run of %s, skipping' % command)
    return True
