import ast
import tempfile
from subprocess import call

from docopt import docopt
import path
import semantic_version
import logging

import changes


log = logging.getLogger(__name__)


def extract(d, keys):
    return dict((k, d[k]) for k in keys if k in d)


def increment(version, major=False, minor=False, patch=True):
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


def write_new_changelog(app_name, filename, content, dry_run=True):
    heading_and_newline = (
        '# (Changelog)[%s/releases]\n\n' % 
        extract_attribute(app_name, '__url__')
    )

    with open(filename, 'r+') as f:
        existing = f.readlines()

    output = existing[2:]
    output.insert(0, content + '\n\n')
    output.insert(0, heading_and_newline)

    if not dry_run:
        with open(filename, 'w+') as f: 
            f.writelines(output)
    else:
        log.info('New changelog:\n%s' % '\n'.join(output))


def get_new_version(app_name, current_version,
                    major=False, minor=False, patch=True):

    guess_new_version = increment(
        current_version,
        major=major,
        minor=minor,
        patch=patch
    )

    new_version = raw_input(
        'What is the release version for "%s"'
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
        path.move(tmp_file, init_file)
    else:
      log.debug(execute(['diff', tmp_file, init_file], dry_run=False))


def current_version(app_name):
    return extract_attribute(app_name, '__version__')

def execute(commands, dry_run=True):
    if not dry_run:
        return call(commands)
    else:
        log.debug('execute: %s' % commands)

def version(arguments):
    dry_run=arguments['--dry-run']
    app_name = arguments['<app_name>']
    new_version = arguments['new_version']

    replace_attribute(app_name, '__version__', new_version, dry_run=dry_run)

    execute(
        ['git', 'ci', '-m',
         '"%s"' % new_version,
         '%s/__init__.py' % app_name],
        dry_run=dry_run
    )

    execute(['git', 'push'], dry_run=dry_run)

def changelog(arguments):
    dry_run=arguments['--dry-run']
    app_name = arguments['<app_name>']
    new_version = arguments['new_version']

    write_new_changelog(
        app_name,
        'CHANGELOG.md', '\n'.join([
            '## [%s](https://github.com/yola/demands/compare/%s...%s)\n',
            '* Fill this in.'
        ]) % (
            new_version,
            current_version(app_name),
            new_version
        ),
        dry_run=dry_run
    )

def tag(arguments):
    dry_run=arguments['--dry-run']
    app_name = arguments['<app_name>']
    new_version = arguments['new_version']

    execute(['git', 'tag', '-a', new_version, '"%s"' % new_version], dry_run=dry_run)
    # fixme: check for call error
    execute(['git push --tags'], dry_run=dry_run)

def upload(arguments):
    dry_run=arguments['--dry-run']
    pypi = arguments['--pypi']

    upload = ['python', 'setup.py', 'clean', 'sdist', 'upload']
    if pypi: 
        upload.append('-r')
        upload.append(pypi)

    execute(upload, dry_run=dry_run)

cli = """
changes.

Usage:
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
    for command in ['version', 'changelog', 'tag', 'upload']:
        if arguments[command]:
            globals()[command](arguments)

