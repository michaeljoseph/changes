import logging

from plumbum import local, CommandNotFound

from changes import config
from changes.changelog import changelog
from changes.packaging import install, upload, pypi
from changes.vcs import tag, commit_version_change
from changes.verification import run_tests
from changes.version import bump_version


log = logging.getLogger(__name__)

def release():
    try:
        if not config.arguments['--skip-changelog']:
            changelog()
        bump_version()
        run_tests()
        commit_version_change()
        install()
        upload()
        pypi()
        tag()
    except:
        log.exception('Error releasing')
