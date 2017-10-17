from . import info, note, error
from .status import changes_to_release_type, status


    repository, release_type, proposed_version = status()
def stage(draft):

    if not repository.changes_since_last_version:
        error("There aren't any changes to release!")
        return

    info('Staging [{}] release for version {}'.format(
        release_type,
        proposed_version
    ))
    ))
