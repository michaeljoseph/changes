CHANGELOG = 'CHANGELOG.md'
arguments = {}


def common_arguments():
    """
    Return common arguments

    :return: tuple of <module_name>, --dry-run, new_version
    """

    module_name = arguments['<module_name>']

    version_prefix = arguments.get('--version-prefix')
    new_version = arguments['new_version']

    common_arguments = (
        module_name,
        arguments['--dry-run'],
        version_prefix + new_version if version_prefix else new_version,
    )
    return common_arguments
