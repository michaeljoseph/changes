
import bumpversion

from changes.config import BumpVersion
from . import info, note, error
from .status import status


def stage(draft):
    repository, bumpversion_part, release_type, proposed_version = status()

    if not repository.changes_since_last_version:
        error("There aren't any changes to release!")
        return

    info('Staging [{}] release for version {}'.format(
        release_type,
        proposed_version
    ))

    bumpversion_arguments = (
        BumpVersion.DRAFT_OPTIONS if draft
        else BumpVersion.STAGE_OPTIONS
    )
    bumpversion_arguments += [bumpversion_part]

    info('Running: bumpversion {}'.format(
        ' '.join(bumpversion_arguments)
    ))

    try:
        bumpversion.main(bumpversion_arguments)
    except bumpversion.WorkingDirectoryIsDirtyException as err:
        error(err)
        raise
    staged_files = [

    ]
    staged_release = None
    return staged_release
