import contextlib
import tempfile

from path import path


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


def extract_arguments(arguments, long_keys, key_prefix='--'):
    """
    :param arguments: dict of command line arguments

    """
    long_arguments = extract(
        arguments,
        long_keys,
    )
    return dict([
        (key.replace(key_prefix, ''), value)
        for key, value in long_arguments.items()
    ])


@contextlib.contextmanager
def mktmpdir():
    tmp_dir = tempfile.mkdtemp()
    try:
        yield tmp_dir
    finally:
        path(tmp_dir).rmtree(path(tmp_dir))
