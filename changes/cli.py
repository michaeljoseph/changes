"""
changes.

Usage:
  changes [options] <app_name> changelog
  changes [options] <app_name> release
  changes [options] <app_name> bump_version
  changes [options] <app_name> run_tests
  changes [options] <app_name> install
  changes [options] <app_name> upload
  changes [options] <app_name> pypi
  changes [options] <app_name> tag

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
"""
import logging

from docopt import docopt

import changes
from changes import config, probe, util, version
from changes.changelog import changelog
from changes.config import arguments
from changes.packaging import install, upload, pypi
from changes.vcs import tag, commit_version_change
from changes.verification import run_tests
from changes.version import bump_version


log = logging.getLogger(__name__)


def release():
    try:
        if not arguments['--skip-changelog']:
            changelog()
        bump_version()
        run_tests()
        commit_version_change()
        install()
        upload()
        pypi()
        tag()
    except:
        log.exception('Error releasing')


def initialise():
    arguments = docopt(__doc__, version=changes.__version__)
    debug = arguments['--debug']
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
    log.debug('arguments: %s', arguments)
    config.arguments = arguments
    return arguments


def main():
    arguments = initialise()

    version_arguments = ['--major', '--minor', '--patch']
    commands = ['release', 'changelog', 'run_tests', 'bump_version', 'tag',
                'upload', 'install', 'pypi']
    suppress_version_prompt_for = ['run_tests', 'upload']

    if arguments['--new-version']:
        arguments['new_version'] = arguments['--new-version']

    app_name = config.arguments['<app_name>']

    if not probe.probe_project(app_name):
        raise Exception('Project does not meet `changes` requirements')

    for command in commands:
        if arguments[command]:
            if command not in suppress_version_prompt_for:
                arguments['new_version'] = version.get_new_version(
                    app_name,
                    version.current_version(app_name),
                    arguments.get('--noinput', False),
                    **util.extract_arguments(arguments, version_arguments)
                )
            globals()[command]()
