"""
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
  --package-name=<package>   If your module and package aren't the same
  --requirements=<req>       Requirements file name (default: requirements.txt)
  --debug                    Debug output.

The commands do the following:
   changelog     Generates an automatic changelog from your commit messages
   bump_version  Increments the __version__ attribute of your module's __init__
   run_tests     Runs your tests with nosetests
   install       Attempts to install the sdist and wheel
   tag           Tags your git repo with the new version number
   upload        Uploads your project with setup.py clean sdist bdist_wheel upload
   pypi          Attempts to install your package from pypi
   release       Runs all the previous commands
"""
import logging

import click

import changes
from changes import attributes, config, probe, version
from changes.changelog import changelog
from changes.flow import release
from changes.packaging import install, upload, pypi
from changes.vcs import tag, commit_version_change
from changes.verification import run_tests
from changes.version import bump_version


log = logging.getLogger(__name__)

@click.group()
@click.argument('module_name')
@click.option('--dry-run', is_flag=True, default=False, help='Prints (instead of executing) the operations to be performed.')
@click.option('--debug', is_flag=True, default=False, help='Enables debug output.')
@click.option('--no-input', is_flag=True, default=False, help='Suppresses version number confirmation prompt.')
@click.option('--requirements', default='requirements.txt', help='Requirements file name')
@click.option('-p', '--patch', is_flag=True, help='Patch-level version increment.')
@click.option('-m', '--minor', is_flag=True, help='Minor-level version increment.')
@click.option('-M', '--major', is_flag=True, help='Minor-level version increment.')
@click.pass_context
def main(context, module_name, dry_run, debug, no_input, requirements, patch, minor, major):
    """Ch-ch-changes"""

    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)

    new_version = version.get_new_version(
        module_name,
        version.current_version(module_name),
        no_input, major, minor, patch,
    )

    current_version = version.current_version(module_name)
    repo_url = attributes.extract_attribute(module_name, '__url__')
    context.obj = config.Changes(module_name, dry_run, debug, no_input, requirements, new_version, current_version, repo_url)

    probe.probe_project(context.obj)

main.add_command(changelog)
main.add_command(bump_version)
main.add_command(install)
main.add_command(upload)
main.add_command(pypi)
