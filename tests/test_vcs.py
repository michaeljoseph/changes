from changes import vcs
from . import BaseTestCase


class VcsTestCase(BaseTestCase):

    def test_commit_version_change(self):
        vcs.commit_version_change(self.context)

    def test_tag_and_push(self):
        pass

