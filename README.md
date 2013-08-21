# changes

:musical_note: [Ch-ch-ch-ch-changes](http://www.youtube.com/watch?v=pl3vxEudif8) :musical_note: 

![changes](https://github.com/michaeljoseph/changes/raw/master/resources/changes.png)

[![Build Status](https://secure.travis-ci.org/michaeljoseph/changes.png)](http://travis-ci.org/michaeljoseph/changes)

## Overview

Manages the release of a python library.

* cli that uses [semver][0] principles to increment the current version
* auto generates a changelog entry (using github's compare view)
* tags the github repo
* uploads to pypi

## Usage

An application wanting to use `changes` must meet these requirements: 

* `setup.py`
* `CHANGELOG.md`
* `app_name/__init__.py` with `__version__`

Install `changes`:

    pip install changes

Run the cli:

>> insert docopt <<

## Documentation

[API Documentation][1]

## Testing ##

Install development requirements:

    pip install -r requirements.txt

Tests can then be run by doing:

    nosetests

Run the linting (pep8, pyflakes) with:

    flake8 yousers tests

## API documentation

To generate the documentation:

    cd docs && PYTHONPATH=.. make singlehtml

To monitor changes to Python files and execute pep8, pyflakes, and nosetests
automatically, execute the following from the root project directory:

    stir


[0]:http://semver.org
[1]:http://changes.rtfd.org
