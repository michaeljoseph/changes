import logging

from changes import config

log = logging.getLogger(__name__)


def handle_dry_run(function, *args):
    if not config.arguments.get('--dry-run', True):
        return function(*args)
    else:
        log.debug('dry run of %s %s, skipping' % (function, args))
        return True
