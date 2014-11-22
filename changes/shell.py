import logging

from plumbum import local

log = logging.getLogger(__name__)


def dry_run(command, dry_run):
    """Executes a shell command unless the dry run option is set"""
    if not dry_run:
        cmd_parts = command.split(' ')
        # http://plumbum.readthedocs.org/en/latest/local_commands.html#run-and-popen
        return local[cmd_parts[0]](cmd_parts[1:])
    else:
        log.info('Dry run of %s, skipping' % command)
    return True
