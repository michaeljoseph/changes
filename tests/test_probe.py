import os
import glob
import pytest
from click.testing import CliRunner

from changes import probe, exceptions
from .conftest import PYTHON_MODULE


def test_probe_project(python_module):
    assert probe.probe_project('test_app')


def test_has_binary():
    assert probe.has_binary('git')


def test_has_no_binary():
    assert not probe.has_binary('foo')


def test_has_test_runner():
    assert probe.has_test_runner()


def test_accepts_readme(python_module):
    for ext in probe.README_EXTENSIONS:
        path = 'README{0}'.format(ext)
        open(path, 'w')
        assert probe.has_readme()
        os.remove(path)


def test_refuses_readme():
    with CliRunner().isolated_filesystem():
        for ext in ['.py', '.doc', '.mp3']:
            path = 'README{0}'.format(ext)
            open(path, 'w')
            with pytest.raises(exceptions.ProbeException):
                probe.has_readme()
            os.remove(path)


def test_fails_for_missing_readme(python_module):
    with CliRunner().isolated_filesystem():
    # for i in glob.glob('README*'):
    #     os.remove(i)
        with pytest.raises(exceptions.ProbeException):
            probe.has_readme()
