from changes import probe
from . import context, setup, teardown


def test_probe_project():
    assert probe.probe_project(context)


def test_has_binary():
    assert probe.has_binary('git')


def test_has_no_binary():
    assert not probe.has_binary('foo')


def test_has_test_runner():
    assert probe.has_test_runner()
