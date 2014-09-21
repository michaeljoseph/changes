from pytest import raises

from changes import probe


def test_probe_project():
    assert probe.probe_project(context)

def test_probe_with_alt_requirements():
    context.requirements = 'test-requirements.txt'
    with raises(Exception):
        probe.probe_project(context)
