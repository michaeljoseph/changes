import logging

import semantic_version

from changes import config, attributes

log = logging.getLogger(__name__)


def bump_version():
    module_name, dry_run, new_version = config.common_arguments()

    attributes.replace_attribute(
        module_name,
        '__version__',
        new_version,
        dry_run=dry_run)


def current_version(module_name):
    return attributes.extract_attribute(module_name, '__version__')


def get_new_version(module_name, current_version, no_input,
                    major=False, minor=False, patch=False):

    proposed_new_version = increment(
        current_version,
        major=major,
        minor=minor,
        patch=patch
    )

    if no_input:
        new_version = proposed_new_version
    else:
        new_version = raw_input(
            'What is the release version for "%s" '
            '[Default: %s]: ' % (
                module_name, proposed_new_version
            )
        ) or proposed_new_version

    return new_version.strip()


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
