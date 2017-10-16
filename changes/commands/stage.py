from . import info, note, error
from .status import changes_to_release_type, status


def stage(version=None):
    repository, release_type, proposed_version = status()

    if not repository.changes_since_last_version:
        error("There aren't any changes to release!")
        return

    # default to changes since last version
    version = version if version else proposed_version

    info('Staging [{}] release for version {}'.format(
        release_type,
        version
    ))
