import logging

from plumbum import local, CommandNotFound

from changes.changelog import generate_changelog
from changes.packaging import install_package, upload_package, install_from_pypi
from changes.vcs import tag_and_push, commit_version_change
from changes.verification import run_tests
from changes.version import increment_version

log = logging.getLogger(__name__)


def perform_release(context):
    """Executes the release process."""
    try:
        print(context)
        if not context.skip_changelog:
            generate_changelog(context)
        increment_version(context)
        commit_version_change(context)
        install_package(context)
        upload_package(context)
        install_from_pypi(context)
        tag_and_push(context)
    except:
        log.exception('Error releasing')
