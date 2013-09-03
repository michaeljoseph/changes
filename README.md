# changes

[![Build Status](https://secure.travis-ci.org/michaeljoseph/changes.png)](http://travis-ci.org/michaeljoseph/changes)
[![Stories in Ready](https://badge.waffle.io/michaeljoseph/changes.png?label=ready)](https://waffle.io/michaeljoseph/changes)
[![pypi version](https://badge.fury.io/py/changes.png)](http://badge.fury.io/py/changes)
[![# of downloads](https://pypip.in/d/changes/badge.png)](https://crate.io/packages/changes?version=latest)
[![code coverage](https://coveralls.io/repos/michaeljoseph/changes/badge.png?branch=master)](https://coveralls.io/r/michaeljoseph/changes?branch=master)

:musical_note: [Ch-ch-ch-ch-changes](http://www.youtube.com/watch?v=pl3vxEudif8) :musical_note: 

![changes](https://github.com/michaeljoseph/changes/raw/master/resources/changes.png)

## Overview

Manages the release of a python library.

* cli that follows [semantic versioning][0] principles to increment the current version
* auto generates a changelog entry (using github's compare view)
* tags the github repo
* uploads to pypi

## Usage

An application wanting to use `changes` must meet these requirements: 

* `setup.py`
* `CHANGELOG.md`
* `app_name/__init__.py` with `__version__` and `__url__`

Install `changes`:

    pip install changes

Run the cli:

```
changes.

Usage:
  changes [options] <app_name> release
  changes [options] <app_name> version
  changes [options] <app_name> changelog
  changes [options] <app_name> tag
  changes [options] <app_name> upload
  changes -h | --help

Options:
  --new-version=<ver>   Specify version.
  -p --patch            Patch-level version increment.
  -m --minor            Minor-level version increment.
  -M --major            Minor-level version increment.

  -h --help             Show this screen.

  --pypi=<pypi>         Specify alternative pypi
  --dry-run             Prints the commands that would have been executed.
  --skip-changelog      For the release task: should the changelog be generated
                        and committed?
  --debug               Debug output.
```

The default workflow is to run the `changelog` command to autogenerate
a changelog entry based on your commit messages.

You're probably going to want to edit that a bit, so `changes` won't commit it,
 unless you're running the `release` command.

The remaining tasks can be automated with the `release` command (the 
`--skip-changelog` option prevents `release` from regenerating the automatic changelog)

```python
(changes)➜  changes git:(master) changes -p changes changelog
What is the release version for "changes" [Default: 0.1.1]:
INFO:changes.cli:Added content to CHANGELOG.md
Everything up-to-date
INFO:changes.cli:Committed changelog update

<< changelog pruning >>

(changes)➜  changes git:(master) ✗ changes -p changes release --skip-changelog
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

Or you can do it all in one step, if your commit messages are good enough:
```python
changes -p changes release
```

## Documentation

[API Documentation][1]

## Testing ##

Install development requirements:

    pip install -r requirements.txt

Tests can then be run by doing:

    nosetests

Run the linting (pep8, pyflakes) with:

    flake8 changes tests

## API documentation

To generate the documentation:

    cd docs && PYTHONPATH=.. make singlehtml

To monitor changes to Python files and execute pep8, pyflakes, and nosetests
automatically, execute the following from the root project directory:

    stir


[0]:http://semver.org
[1]:http://changes.rtfd.org
