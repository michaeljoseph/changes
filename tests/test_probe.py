import os
import glob
import pytest

from changes import probe
from changes import exceptions

from . import context, setup, teardown

def test_probe_project():
    assert probe.probe_project(context)


def test_has_binary():
    assert probe.has_binary('git')


def test_has_no_binary():
    assert not probe.has_binary('foo')

def test_has_test_runner():
    assert probe.has_test_runner()

def test_accepts_readme():
	os.chdir(context.module_name)
	for ext in probe.README_EXTENSIONS:
		path = "README%s" % ext
		with open(path, 'w'):
			assert probe.has_readme()
			os.remove(path)
	os.chdir("..")

def test_refuses_readme():
	os.chdir(context.module_name)
	for ext in [".py", ".doc", ".mp3"]:
		path = "README%s" % ext
		with open(path, 'w'):
			with pytest.raises(exceptions.ProbeException):
				probe.has_readme()
			os.remove(path)
	os.chdir("..")

def test_fails_for_missing_readme():
	os.chdir(context.module_name)
	for i in glob.glob("README*"):
		os.remove(i)
	with pytest.raises(exceptions.ProbeException):
		probe.has_readme()
	os.chdir("..")

