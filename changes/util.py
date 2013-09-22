import semantic_version


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
