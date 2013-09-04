import ast
import re
import subprocess
import tempfile

from docopt import docopt
from path import path
import semantic_version
import logging

import changes


log = logging.getLogger(__name__)

CHANGELOG = 'CHANGELOG.md'

def extract(dictionary, keys):
    """
    Extract only the specified keys from a dict

    :param dictionary: source dictionary
    :param keys: list of keys to extract
    :return dict: extracted dictionary
    """
    return dict(
        (k, dictionary[k]) for k in keys if k in dictionary
    )


def increment(version, major=False, minor=False, patch=True):
    """
    Increment a semantic version

    :param version: str of the version to increment
    :param major: bool specifying major level version increment
    :param minor: bool specifying minor level version increment
    :param patch: bool specifying patch level version increment
    :return: str of the incremented version
    """
    version = semantic_version.Version(version)
    if major:
        version.major += 1
        version.minor = 0
        version.patch = 0
    elif minor:
        version.minor += 1
        version.patch = 0
    elif patch:
        version.patch += 1

    return str(version)


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
        log.info('New changelog:\n%s' % output)


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
    if not dry_run:
        try:
            return subprocess.check_output(commands)
        except subprocess.CalledProcessError, e:
            return '\n%s' % e.output
    else:
        log.debug('execute: %s' % commands)


def version(arguments):
    dry_run = arguments['--dry-run']
    app_name = arguments['<app_name>']
    new_version = arguments['new_version']

    replace_attribute(app_name, '__version__', new_version, dry_run=dry_run)

    commands = [
        'git', 'ci', '-m', new_version,
        '%s/__init__.py' % app_name, CHANGELOG
    ]

    execute(commands, dry_run=dry_run)

    execute(['git', 'push'], dry_run=dry_run)


def changelog(arguments):
    dry_run = arguments['--dry-run']
    app_name = arguments['<app_name>']
    new_version = arguments['new_version']

    changelog_content = [
        '\n## [%s](%s/compare/%s...%s)\n\n' % (
            new_version, extract_attribute(app_name, '__url__'),
            current_version(app_name), new_version,
        )
    ]

    git_log_content = execute([
        'git', 'log',  '--oneline', '--no-merges',
        '%s..master' % current_version(app_name)],
        dry_run=False
    ).split('\n')

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
            log.debug('old line: %s\nnew line: %s' % (line, new_line))
            git_log_content[index] = new_line

    if git_log_content:
        [changelog_content.append('* %s\n' % line) if line else line for line in git_log_content[:-1]]

    write_new_changelog(
        app_name,
        CHANGELOG,
        changelog_content,
        dry_run=dry_run
    )
    log.info('Added content to CHANGELOG.md')


def tag(arguments):
    dry_run = arguments['--dry-run']
    new_version = arguments['new_version']

    execute(['git', 'tag', '-a', new_version, '-m', '"%s"' % new_version], dry_run=dry_run)
    execute(['git', 'push', '--tags'], dry_run=dry_run)


def upload(arguments):
    dry_run = arguments['--dry-run']
    pypi = arguments['--pypi']

    upload = ['python', 'setup.py', 'clean', 'sdist', 'upload']
    if pypi: 
        upload.append('-r')
        upload.append(pypi)

    execute(upload, dry_run=dry_run)


def release(arguments):
    if not arguments['--skip-changelog']:
        changelog(arguments)
    version(arguments)
    tag(arguments)
    upload(arguments)


cli = """
changes.

Usage:
  changes [options] <app_name> changelog
  changes [options] <app_name> release
  changes [options] <app_name> version
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
"""


def main():
    arguments = docopt(cli, version=changes.__version__)
    debug = arguments['--debug']
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)

    app_name = arguments['<app_name>']
    if arguments['--new-version']:
        new_version = arguments['--new-version']
    else:
        new_version = get_new_version(
            app_name,
            current_version(app_name),
            **dict([
                (key[2:], value) for key, value in extract(arguments, ['--major', '--minor', '--patch']).items()
            ])
        )

    arguments['new_version'] = new_version
    log.debug('arguments: %s', arguments)
    for command in ['release', 'version', 'changelog', 'tag', 'upload']:
        if arguments[command]:
            globals()[command](arguments)
