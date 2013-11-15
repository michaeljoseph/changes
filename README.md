# changes

[![Build Status](https://secure.travis-ci.org/michaeljoseph/changes.png)](http://travis-ci.org/michaeljoseph/changes)
[![Stories in Ready](https://badge.waffle.io/michaeljoseph/changes.png?label=ready)](https://waffle.io/michaeljoseph/changes)
[![pypi version](https://badge.fury.io/py/changes.png)](http://badge.fury.io/py/changes)
[![# of downloads](https://pypip.in/d/changes/badge.png)](https://crate.io/packages/changes?version=latest)
[![code coverage](https://coveralls.io/repos/michaeljoseph/changes/badge.png?branch=master)](https://coveralls.io/r/michaeljoseph/changes?branch=master)

:musical_note: [Ch-ch-changes](http://www.youtube.com/watch?v=pl3vxEudif8) :musical_note: 

![changes](https://github.com/michaeljoseph/changes/raw/master/resources/changes.png)

## Overview

Manages the release of a python library.

* auto generates a changelog entry (using github's compare view and commit urls)
* cli that follows [semantic versioning][0] principles to auto-increment the library version
* runs the library tests
* test package installation from a tarball and pypi
* uploads to pypi
* tags the github repo

## Usage

An application wanting to use `changes` must meet these requirements: 

* on [github](https://github.com)
* `setup.py`
* `requirements.txt`
* `CHANGELOG.md`
* `<app_name>/__init__.py` with `__version__` and `__url__`
* supports executing tests with [`nosetests`][2] or [`tox`][3]
* we expect `<app_name>` to be the package and module name

Install `changes`:

    pip install changes

Run the cli:

```
changes.

Usage:
  changes [options] <module_name> changelog
  changes [options] <module_name> release
  changes [options] <module_name> bump_version
  changes [options] <module_name> run_tests
  changes [options] <module_name> install
  changes [options] <module_name> upload
  changes [options] <module_name> pypi
  changes [options] <module_name> tag

  changes -h | --help

Options:
  --new-version=<ver>        Specify version.
  -p --patch                 Patch-level version increment.
  -m --minor                 Minor-level version increment.
  -M --major                 Minor-level version increment.

  -h --help                  Show this screen.

  --pypi=<pypi>              Use alternative package index
  --dry-run                  Prints the commands that would have been executed.
  --skip-changelog           For the release task: should the changelog be
                             generated and committed?
  --tox                      Use `tox` instead of the default: `nosetests`
  --test-command=<cmd>       Command to use to test the newly installed package
  --version-prefix=<prefix>  Specify a prefix for version number tags
  --noinput                  To be used in conjuction with one of the version
                             increment options above, this option stops
                             `changes` from confirming the new version number.
  --module-name=<module>     If your module and package aren't the same
  --requirements=<reqfile>   Requirements file name (defaults to requirements.txt)
  --debug                    Debug output.

The commands do the following:
   changelog     Generates an automatic changelog from your commit messages
   bump_version  Increments the __version__ attribute of your module's __init__
   run_tests     Runs your tests with nosetests
   install       Attempts to install the sdist
   tag           Tags your git repo with the new version number
   upload        Uploads your project with setup.py clean sdist upload
   pypi          Attempts to install your package from pypi
   release       Runs all the previous commands
```

The default workflow is to run the `changelog` command to autogenerate
a changelog entry based on your commit messages.

You're probably going to want to edit that a bit, so `changes` won't commit it,
 unless you're running the `release` command.

The remaining tasks can be automated with the `release` command (the 
`--skip-changelog` option prevents `release` from regenerating the automatic changelog)

```python
(changes)$ changes changes -p changes changelog
What is the release version for "changes" [Default: 0.1.1]:
INFO:changes.cli:Added content to CHANGELOG.md
Everything up-to-date
INFO:changes.cli:Committed changelog update

<< changelog pruning >>

(changes)$ changes -p changes release --skip-changelog
What is the release version for "changes" [Default: 0.1.1]:
Counting objects: 7, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (4/4), done.
Writing objects: 100% (4/4), 400 bytes, done.
Total 4 (delta 2), reused 0 (delta 0)
To git@github.com:michaeljoseph/changes.git
   5c6760d..bafce16  master -> master
Counting objects: 1, done.
Writing objects: 100% (1/1), 168 bytes, done.
Total 1 (delta 0), reused 0 (delta 0)
To git@github.com:michaeljoseph/changes.git
 * [new tag]         0.1.1 -> 0.1.1
warning: sdist: standard file not found: should have one of README, README.rst, README.txt
```

Or you can do it all in one step (if your commit messages are good enough):
```python
(changes)$ changes -m changes release
What is the release version for "changes" [Default: 0.2.0]:
INFO:changes.cli:Added content to CHANGELOG.md

Changes test case
- extract
- extract attribute
- increment
- replace attribute
- write new changelog

----------------------------------------------------------------------
Ran 5 tests in 0.119s

OK

Counting objects: 9, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (5/5), done.
Writing objects: 100% (5/5), 1.01 KiB, done.
Total 5 (delta 3), reused 0 (delta 0)
To git@github.com:michaeljoseph/changes.git
   7b8f0a6..6a7379c  master -> master
warning: sdist: standard file not found: should have one of README, README.rst, README.txt

INFO:changes.cli:Successfully installed changes sdist
warning: sdist: standard file not found: should have one of README, README.rst, README.txt

INFO:changes.cli:Successfully installed changes from pypi
Counting objects: 1, done.
Writing objects: 100% (1/1), 168 bytes, done.
Total 1 (delta 0), reused 0 (delta 0)
To git@github.com:michaeljoseph/changes.git
 * [new tag]         0.2.0 -> 0.2.0
```

## Documentation

[API Documentation][1]

## Testing

Install development requirements:

    pip install -r requirements.txt

Tests can then be run with:

    nosetests

Lint the project with:

    flake8 changes tests

## API documentation

Generate the documentation with:

    (cd docs && make singlehtml)

To monitor changes to Python files and execute flake8 and nosetests
automatically, execute the following from the root project directory:

    stir


[0]:http://semver.org
[1]:http://changes.rtfd.org
[2]:http://nose.rtfd.org
[3]:http://tox.rtfd.org

