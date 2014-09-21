from changes import vcs
from . import context, setup, teardown


def test_commit_version_change():
    vcs.commit_version_change(context)

def test_tag_and_push():
    pass

