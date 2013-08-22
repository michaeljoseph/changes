import ast
import tempfile
from subprocess import call

from docopt import docopt
import path
import semantic_version

import changes

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


def prepend_file(filename, content, dry_run=True):
    if not dry_run:
        with open(filename, 'r+') as f:
            existing = f.read()
            f.seek(0)
            f.write(content + '\n' + existing)
    else:
        print('Prepending %s to %s' % (content, filename))


def get_new_version(app_name, current_version,
                    major=False, minor=False, patch=True):

    guess_new_version = increment(
        current_version,
        major=major,
        minor=minor,
        patch=patch
    )
    print('ere')

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
      print(execute('diff %s %s' % (tmp_file, init_file)))


def current_version(app_name):
    return extract_attribute(
        arguments['<app_name>'],
        '__version__'
    )

def execute(command, dry_run=True):
    if not dry_run:
        return call([command])
    else:
        print('execute: %s', command)

def version(arguments):
    dry_run=arguments['--dry-run']
    app_name = arguments['<app_name>']
    new_version = arguments['new_version']
    print('oi')
    replace_attribute(app_name, '__version__', new_version, dry_run=dry_run)

    execute('git ci -m "%s" %s/__init__.py && git push' % (
        new_version, app_name
    ), dry_run=dry_run)

def changelog(arguments):
    prepend_file(
        'CHANGELOG.md', '\n'.join([
            '# (Changelog)[https://github.com/michaeljoseph/changes/releases]',
            '## [%s](https://github.com/yola/demands/compare/%s...%s)',
            '* Fill this in.'
        ]) % (
            arguments['new_version'],
            current_version(app_name),
            arguments['new_version']
        ),
        dry_run=arguments['--dry-run']
    )

def tag(arguments):
    execute('git tag -a %s "%s"; git push --tags' % (
        arguments['new_version'], arguments['new_version']
    ), dry_run=arguments['--dry-run'])

def upload(arguments):
    upload = 'python setup.py clean sdist upload'
    if '--pypi' in arguments:
        upload = upload + ' -r %s' % arguments['--pypi']
    execute(upload, dry_run=arguments['--dry-run'])

cli = """
changes.

Usage:
  changes [options] <app_name> version (major|minor|patch)
  changes [options] <app_name> changelog
  changes [options] <app_name> tag
  changes [options] <app_name> upload
  changes -h | --help

Options:
  -h --help             Show this screen.
  --new-version=<ver>   Specify version.
  --pypi=<pypi>         Specify alternative pypi
  --dry-run             Prints the commands that would have been executed.
"""


def main():
    arguments = docopt(cli, version=changes.__version__)

    app_name = arguments['<app_name>']
    if '--new-version' in arguments:
        new_version = arguments['--new-version']
    else:
        new_version = get_new_version(
            app_name,
            current_version(app_name),
            **extract(
                arguments,
                ['major', 'minor', 'patch']
            )
        )

    arguments['new_version'] = new_version
    print(arguments)
    for command in ['version', 'changelog', 'tag', 'upload']:
        if arguments[command]:
            globals()[command](arguments)

