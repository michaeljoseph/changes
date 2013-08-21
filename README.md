# changes

Ch ch ch changes <youtube> / <img>
[build status]
[Documentation][0]

## Overview

Manages the release of a python library.

* cli that uses [semver][1] principles to increment the current version
* auto generates a changelog entry (using github's compare view)
* tags the github repo
* uploads to pypi

## Usage

An application wanting to use [`changes`][2] must meet these requirements: 

* setup.py
* CHANGELOG.md
* `app_name/__init__.py` with `__version__`


Install [`changes`]:

    pip install changes

Run the cli:

    changes major

    # output

## [`changes.changes`]

    # docopt
    # skip prompts
    # specify version number
    # [M]ajor, [m]inor, [p]atch (default)
    


