from unittest2 import TestCase
from changes.cli import increment, write_new_changelog
import os


class ChangesTestCase(TestCase):

    def setUp(self):
        self.tmp_file = 'test_app/__init__.py'
        if not os.path.exists('test_app'):
            os.mkdir('test_app')

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
        content = [
            'This is the heading\n\n',
            'This is the first line\n',
        ]

        with open(self.tmp_file, 'w') as existing_file:
            existing_file.writelines(content)

        write_new_changelog('test_app', self.tmp_file, 'Now this is')

        self.assertEquals(
            ''.join(content),
            ''.join(
                open(self.tmp_file).readlines()
            )            
        )

        with open(self.tmp_file, 'w') as existing_file:
            existing_file.writelines(content)

        write_new_changelog(
            'test_app',
            self.tmp_file,
            'Now this is',
            dry_run=False
        )
        expected_content = [
            '# (Changelog)[None/releases]\n',
            'Now this is\n',
            'This is the first line\n'
        ]
        self.assertEquals(
            ''.join(expected_content),
            ''.join(
                open(self.tmp_file).readlines()
            )
        )

    def tearDown(self):
        if os.path.exists(self.tmp_file):
            os.remove(self.tmp_file)
            os.rmdir('test_app')
