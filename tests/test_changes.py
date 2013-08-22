import tempfile

from unittest2 import TestCase
from changes.cli import increment, prepend_file


class ChangesTestCase(TestCase):

    def test_increment(self):
        self.assertEquals(
            '1.0.0',
            increment('0.0.1', major=True)
        )

        self.assertEquals(
            '0.1.0',
            increment('0.0.1', minor=True)
        )

        self.assertEquals(
            '1.0.1',
            increment('1.0.0', patch=True)
        )

    def test_prepend_file(self):
        _, tmp_file = tempfile.mkstemp()
        with open(tmp_file, 'w') as existing_file:
            existing_file.write('This is the first line')

        prepend_file(tmp_file, 'Now this is')
        self.assertEquals(
            'This is the first line',
            ''.join(
                open(tmp_file).readlines()
            )            
        )

        prepend_file(tmp_file, 'Now this is', dry_run=False)
        self.assertEquals(
            'Now this is\nThis is the first line',
            ''.join(
                open(tmp_file).readlines()
            )
        )

