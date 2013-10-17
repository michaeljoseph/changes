"""
changes.

Usage:
  changes [options] <app_name> changelog
  changes [options] <app_name> release
  changes [options] <app_name> version
  changes [options] <app_name> test
  changes [options] <app_name> install
  changes [options] <app_name> upload
  changes [options] <app_name> pypi
  changes [options] <app_name> tag

  changes -h | --help

Options:
  --new-version=<ver>   Specify version.
  -p --patch            Patch-level version increment.
  -m --minor            Minor-level version increment.
  -M --major            Minor-level version increment.

  -h --help             Show this screen.

  --pypi=<pypi>         Use alternative package index
  --dry-run             Prints the commands that would have been executed.
  --skip-changelog      For the release task: should the changelog be generated
                        and committed?
  --tox                 Use tox instead of nosetests
  --test-command=<cmd>  Command to use to test the newly installed package
  --debug               Debug output.

The commands do the following:
   changelog     Generates an automatic changelog from your commit messages
   bump_version  Increments the __version__ attribute of your module's __init__
   test          Runs your tests with nosetests
   install       Attempts to install the sdist
   tag           Tags your git repo with the new version number
   upload        Uploads your project with setup.py clean sdist upload
   pypi          Attempts to install your package from pypi
   release       Runs all the previous commands
"""

import re

import tempfile

from docopt import docopt
from path import path
import logging
import virtualenv

import changes
from changes import attributes, probe, shell, version


log = logging.getLogger(__name__)
CHANGELOG = 'CHANGELOG.md'
arguments = None


def common_arguments():
    """
    Return common arguments

    :return: tuple of <app_name>, --dry-run, new_version
    """
    return (
        arguments['<app_name>'],
        arguments['--dry-run'],
        arguments['new_version'],
    )


def write_new_changelog(app_name, filename, content_lines, dry_run=True):
    heading_and_newline = (
        '# [Changelog](%s/releases)\n' %
        attributes.extract_attribute(app_name, '__url__')
    )

    with open(filename, 'r+') as f:
        existing = f.readlines()

    output = existing[2:]
    output.insert(0, '\n')

    for index, line in enumerate(content_lines):
        output.insert(0, content_lines[len(content_lines) - index - 1])

    output.insert(0, heading_and_newline)

    output = ''.join(output)

    if not dry_run:
        with open(filename, 'w+') as f:
            f.write(output)
    else:
        log.info('New changelog:\n%s', ''.join(content_lines))


def changelog():
    app_name, dry_run, new_version = common_arguments()

    changelog_content = [
        '\n## [%s](%s/compare/%s...%s)\n\n' % (
            new_version, attributes.extract_attribute(app_name, '__url__'),
            version.current_version(app_name), new_version,
        )
    ]
    git_log = 'git log --oneline --no-merges'
    version_difference = '%s..master' % version.current_version(app_name)

    git_log_content = shell.execute(
        '%s %s' % (git_log, version_difference),
        dry_run=False
    )

    if not git_log_content:
        log.debug('sniffing initial release, drop tags: %s', git_log)
        git_log_content = shell.execute(git_log, dry_run=False)

    for index, line in enumerate(git_log_content):
        # http://stackoverflow.com/a/468378/5549
        sha1_re = re.match(r'^[0-9a-f]{5,40}\b', line)
        if sha1_re:
            sha1 = sha1_re.group()

            new_line = line.replace(
                sha1,
                '[%s](%s/commit/%s)' % (
                    sha1,
                    attributes.extract_attribute(app_name, '__url__'),
                    sha1
                )
            )
            log.debug('old line: %s\nnew line: %s', line, new_line)
            git_log_content[index] = new_line

    if git_log_content:
        [
            changelog_content.append('* %s\n' % line)
            if line else line
            for line in git_log_content[:-1]
        ]

    write_new_changelog(
        app_name,
        CHANGELOG,
        changelog_content,
        dry_run=dry_run
    )
    log.info('Added content to CHANGELOG.md')


def bump_version():
    app_name, dry_run, new_version = common_arguments()

    attributes.replace_attribute(
        app_name,
        '__version__',
        new_version,
        dry_run=dry_run)


def commit_version_change():
    app_name, dry_run, new_version = common_arguments()

    command = 'git commit -m %s %s/__init__.py %s' % (
        new_version, app_name, CHANGELOG
    )

    if not (shell.execute(command, dry_run=dry_run) and
            shell.execute('git push', dry_run=dry_run)):
        raise Exception('Version change commit failed')


def test():
    command = 'nosetests'
    if arguments['--tox']:
        command = 'tox'

    if not shell.execute(command, dry_run=False):
        raise Exception('Test command failed')


def make_virtualenv():
    tmp_dir = tempfile.mkdtemp()
    virtualenv.create_environment(tmp_dir, site_packages=False)
    return tmp_dir


def run_test_command():
    if arguments['--test-command']:
        test_command = arguments['--test-command']
        result = shell.execute(test_command, dry_run=arguments['--dry-run'])
        log.info('Test command "%s", returned %s', test_command, result)
    else:
        log.warning('Test command "%s" failed', test_command)


def install():
    app_name, dry_run, new_version = common_arguments()

    result = shell.execute('python setup.py clean sdist', dry_run=dry_run)
    if result:
        tmp_dir = make_virtualenv()
        try:
            virtualenv.install_sdist(
                arguments['<app_name>'],
                'dist/%s-%s.tar.gz' % (app_name, new_version),
                '%s/bin/python' % tmp_dir
            )
            log.info('Successfully installed %s sdist', app_name)
            if run_test_command():
                log.info('Successfully ran test command: %s',
                         arguments['--test-command'])
        except:
            raise Exception('Error installing %s sdist', app_name)

        path(tmp_dir).rmtree(path(tmp_dir))


def upload():
    app_name, dry_run, new_version = common_arguments()
    pypi = arguments['--pypi']

    upload = 'python setup.py clean sdist upload'
    if pypi:
        upload = upload + '-r %s' % pypi

    if not shell.execute(upload, dry_run=dry_run):
        raise Exception('Error uploading')
    else:
        log.info('Succesfully uploaded %s %s', app_name, new_version)


def pypi():
    app_name, dry_run, _ = common_arguments()
    pypi = arguments['--pypi']
    package_index = 'pypi'

    tmp_dir = make_virtualenv()
    install = '%s/bin/pip install %s' % (tmp_dir, app_name)

    if pypi:
        install = install + '-i %s' % pypi
        package_index = pypi

    try:
        result = shell.execute(install, dry_run=dry_run)
        if result:
            log.info('Successfully installed %s from %s',
                     app_name, package_index)
        else:
            log.error('Failed to install %s from %s',
                      app_name, package_index)

        run_test_command()
    except:
        raise Exception('Error installing %s from %s', app_name, package_index)

    path(tmp_dir).rmtree(path(tmp_dir))


def tag():
    _, dry_run, new_version = common_arguments()

    shell.execute(
        'git tag -a %s -m "%s"' % (new_version, new_version),
        dry_run=dry_run
    )
    shell.execute('git push --tags', dry_run=dry_run)


def release():
    try:
        if not arguments['--skip-changelog']:
            changelog()
        version()
        test()
        commit_version_change()
        install()
        upload()
        pypi()
        tag()
    except:
        log.exception('Error releasing')


def initialise():
    global arguments
    arguments = docopt(__doc__, version=changes.__version__)
    debug = arguments['--debug']
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
    log.debug('arguments: %s', arguments)


def main():
    initialise()

    commands = ['release', 'changelog', 'test', 'bump_version', 'tag',
                'upload', 'install', 'pypi']
    suppress_version_prompt_for = ['test', 'upload']

    if arguments['--new-version']:
        arguments['new_version'] = arguments['--new-version']

    app_name = arguments['<app_name>']

    if not probe.probe_project(app_name):
        raise Exception('Project does not meet `changes` requirements')

    for command in commands:
        if arguments[command]:
            if command not in suppress_version_prompt_for:
                arguments['new_version'] = version.get_new_version(
                    app_name,
                    version.current_version(app_name),
                    **version.extract_version_arguments(arguments)
                )
            globals()[command]()
