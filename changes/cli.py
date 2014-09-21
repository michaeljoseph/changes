import logging

import click

from changes import attributes, config, probe, version
from changes.changelog import generate_changelog
from changes.flow import perform_release
from changes.packaging import install_package, upload_package, install_from_pypi
from changes.vcs import tag_and_push
from changes.version import increment_version

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
@click.option('--version-prefix', help='Specify a prefix for version number tags.')
@click.pass_context
def main(context, module_name, dry_run, debug, no_input, requirements, patch, minor, major, version_prefix):
    """Ch-ch-changes"""

    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)

    new_version = version.get_new_version(
        module_name,
        version.current_version(module_name),
        no_input, major, minor, patch,
    )

    current_version = version.current_version(module_name)
    repo_url = attributes.extract_attribute(module_name, '__url__')
    context.obj = config.Changes(module_name, dry_run, debug, no_input, requirements, new_version, current_version, repo_url, version_prefix)

    probe.probe_project(context.obj)


@click.command()
@click.pass_context
def changelog(context):
    """Generates an automatic changelog from your commit messages."""
    generate_changelog(context.obj)


@click.command()
@click.pass_context
def bump_version(context):
    """Increments the __version__ attribute of your module's __init__."""
    increment_version(context.obj)


@click.command()
@click.option('--test-command', help='Command to use to test the newly installed package.')
@click.pass_context
def install(context, test_command):
    """Attempts to install the sdist and wheel."""
    context.obj.test_command = test_command
    install_package(context.obj)


@click.command()
@click.option('--pypi', help='Use an alternative package index.')
@click.pass_context
def upload(context, pypi):
    """Uploads your project with setup.py clean sdist bdist_wheel upload."""
    context.obj.pypi = pypi
    upload_package(context.obj)


@click.command()
@click.option('--pypi', help='Use an alternative package index.')
@click.pass_context
def pypi(context, pypi):
    """Attempts to install your package from pypi."""
    context.obj.pypi = pypi
    install_from_pypi(context.obj)


@click.command()
@click.pass_context
def tag(context):
    """Tags your git repo with the new version number"""
    tag_and_push(context.obj)

@click.command()
@click.option('--skip-changelog', is_flag=True, help='For the release task: should the changelog be generated and committed?')
@click.pass_context
def release(context, skip_changelog):
    """Executes the release process."""
    context.obj.skip_changelog = skip_changelog
    perform_release(context.obj)


main.add_command(changelog)
main.add_command(bump_version)
main.add_command(install)
main.add_command(upload)
main.add_command(pypi)
main.add_command(tag)
main.add_command(release)
