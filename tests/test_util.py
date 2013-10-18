from unittest2 import TestCase
from changes import util


class UtilTestCase(TestCase):

    def test_extract(self):
        self.assertEquals(
            {'a': 1, 'b': 2},
            util.extract(
                {'a': 1, 'b': 2, 'c': 3},
                ['a', 'b']
            )
        )

    def test_extract_arguments(self):
        self.assertEquals(
            {
                'major': True,
                'minor': False,
                'patch': False,
            },
            util.extract_arguments(
                {
                    '--major': True,
                    '--minor': False,
                    '--patch': False,
                },
                ['--major', '--minor', '--patch']
            ),
        )
