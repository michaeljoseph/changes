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
   changelog   Generates an automatic changelog from your commit messages
   version     Increments the __version__ attribute of your module's __init__
   test        Runs your tests with nosetests
   install     Attempts to install the sdist
   tag         Tags your git repo with the new version number
   upload      Uploads your project with setup.py clean sdist upload
   pypi        Attempts to install your package from pypi
   release     Runs all the previous commands
"""

import ast
import re
import subprocess
import tempfile

from docopt import docopt
from path import path
import logging
import virtualenv

import changes
from changes.util import extract, increment


log = logging.getLogger(__name__)
CHANGELOG = 'CHANGELOG.md'
arguments = None


def strip_long_arguments(argument_names):
    long_arguments = extract(arguments, argument_names)
    return dict([
        (key[2:], value) for key, value in long_arguments.items()
    ])


def extract_version_arguments():
    return strip_long_arguments(['--major', '--minor', '--patch'])


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


def get_new_version(app_name, current_version,
                    major=False, minor=False, patch=True):

    guess_new_version = increment(
        current_version,
        major=major,
        minor=minor,
        patch=patch
    )

    new_version = raw_input(
        'What is the release version for "%s" '
        '[Default: %s]: ' % (
            app_name, guess_new_version
        )
    )
    if not new_version:
        new_version = guess_new_version
    return new_version.strip()


def extract_attribute(app_name, attribute_name):
    """Extract metatdata property from a module"""
    with open('%s/__init__.py' % app_name) as input_file:
        for line in input_file:
            if line.startswith(attribute_name):
                return ast.literal_eval(line.split('=')[1].strip())


def replace_attribute(app_name, attribute_name, new_value, dry_run=True):
    init_file = '%s/__init__.py' % app_name
    _, tmp_file = tempfile.mkstemp()

    with open(init_file) as input_file:
        with open(tmp_file, 'w') as output_file:
            for line in input_file:
                if line.startswith(attribute_name):
                    line = "%s = '%s'\n" % (attribute_name, new_value)

                output_file.write(line)

    if not dry_run:
        path(tmp_file).move(init_file)
    else:
        log.debug(execute(['diff', tmp_file, init_file], dry_run=False))


def current_version(app_name):
    return extract_attribute(app_name, '__version__')


def execute(commands, dry_run=True):
    log.debug('executing %s', commands)
    if not dry_run:
        try:
            return subprocess.check_output(commands).split('\n')
        except subprocess.CalledProcessError, e:
            log.debug('return code: %s, output: %s', e.returncode, e.output)
            return False
    else:
        return True


def write_new_changelog(app_name, filename, content_lines, dry_run=True):
    heading_and_newline = (
        '# [Changelog](%s/releases)\n' %
        extract_attribute(app_name, '__url__')
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
        log.info('New changelog:\n%s', output)


def changelog():
    app_name, dry_run, new_version = common_arguments()

    changelog_content = [
        '\n## [%s](%s/compare/%s...%s)\n\n' % (
            new_version, extract_attribute(app_name, '__url__'),
            current_version(app_name), new_version,
        )
    ]

    git_log_commands = [
        'git', 'log',  '--oneline', '--no-merges',
        '%s..master' % current_version(app_name),
    ]

    git_log_content = execute(git_log_commands, dry_run=False)

    if not git_log_content:
        git_log_commands.pop()
        log.debug('sniffing initial release, drop tags: %s', git_log_commands)
        git_log_content = execute(git_log_commands, dry_run=False)

    for index, line in enumerate(git_log_content):
        # http://stackoverflow.com/a/468378/5549
        sha1_re = re.match(r'^[0-9a-f]{5,40}\b', line)
        if sha1_re:
            sha1 = sha1_re.group()

            new_line = line.replace(
                sha1,
                '[%s](%s/commit/%s)' % (
                    sha1,
                    extract_attribute(app_name, '__url__'),
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


def version():
    app_name, dry_run, new_version = common_arguments()

    replace_attribute(
        app_name,
        '__version__',
        new_version,
        dry_run=dry_run)


def commit_version_change():
    app_name, dry_run, new_version = common_arguments()

    commands = [
        'git', 'ci', '-m', new_version,
        '%s/__init__.py' % app_name, CHANGELOG
    ]

    if not (execute(commands, dry_run=dry_run) and
            execute(['git', 'push'], dry_run=dry_run)):
        raise Exception('Version change commit failed')


def test():
    command = 'nosetests'
    if arguments['--tox']:
        command = 'tox'

    if not execute([command], dry_run=False):
        raise Exception('Test command failed')


def make_virtualenv():
    tmp_dir = tempfile.mkdtemp()
    virtualenv.create_environment(tmp_dir, site_packages=False)
    return tmp_dir


def run_test_command():
    if arguments['--test-command']:
        test_command = arguments['--test-command'].split(' ')
        result = execute(test_command, dry_run=arguments['--dry-run'])
        log.info('Test command "%s", returned %s', test_command, result)
    else:
        log.warning('Test command "%s" failed', test_command)


def install():
    app_name, dry_run, new_version = common_arguments()

    result = execute(
        ['python', 'setup.py', 'clean', 'sdist'],
        dry_run=dry_run
    )
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

    upload = ['python', 'setup.py', 'clean', 'sdist', 'upload']
    if pypi:
        upload.append('-r')
        upload.append(pypi)

    if not execute(upload, dry_run=dry_run):
        raise Exception('Error uploading')
    else:
        log.info('Succesfully uploaded %s %s', app_name, new_version)


def pypi():
    app_name, dry_run, _ = common_arguments()
    pypi = arguments['--pypi']

    package_index = 'pypi'

    tmp_dir = make_virtualenv()
    install = ['%s/bin/pip' % tmp_dir, 'install', app_name]

    if pypi:
        install.append('-i')
        install.append(pypi)
        package_index = pypi

    try:
        result = execute(install, dry_run=dry_run)
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

    execute(
        ['git', 'tag', '-a', new_version, '-m', '"%s"' % new_version],
        dry_run=dry_run
    )
    execute(['git', 'push', '--tags'], dry_run=dry_run)


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
    commands = ['release', 'changelog', 'test', 'version', 'tag', 'upload',
                'install', 'pypi']

    suppress_version_prompt_for = ['test', 'upload']

    app_name = arguments['<app_name>']

    if arguments['--new-version']:
        arguments['new_version'] = arguments['--new-version']

    log.debug('arguments: %s', arguments)

    for command in commands:
        if arguments[command]:
            if command not in suppress_version_prompt_for:
                arguments['new_version'] = get_new_version(
                    app_name,
                    current_version(app_name),
                    **extract_version_arguments()
                )
            globals()[command]()
