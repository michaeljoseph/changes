from pytest import raises
import shutil

from changes import probe
from . import context, setup, teardown


def test_probe_project():
    assert probe.probe_project(context)

def test_probe_with_alt_requirements():
    with raises(Exception):
        shutil.rmtree(context.requirements)
        probe.probe_project(context)
