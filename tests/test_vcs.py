from changes import config, vcs
from . import BaseTestCase


class VcsTestCase(BaseTestCase):

    def setUp(self):
        config.arguments['--dry-run'] = True

    def test_commit_version_change(self):
        vcs.commit_version_change()

    def test_tag(self):
        vcs.tag()
