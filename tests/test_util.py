from changes import util

from . import context, setup, teardown


def test_extract():
    assert {'a': 1, 'b': 2} == util.extract({'a': 1, 'b': 2, 'c': 3}, ['a', 'b'])


def test_extract_arguments():
    assert {
        'major': True,
        'minor': False,
        'patch': False,
    } == util.extract_arguments({
        '--major': True,
        '--minor': False,
        '--patch': False,
        },
        ['--major', '--minor', '--patch']
    )

