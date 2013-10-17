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
