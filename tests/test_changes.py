from unittest2 import TestCase
from changes.cli import (extract_attribute, increment, replace_attribute,
                         write_new_changelog)
import os


class ChangesTestCase(TestCase):

    def setUp(self):
        self.tmp_file = 'test_app/__init__.py'
        if not os.path.exists('test_app'):
            os.mkdir('test_app')
        self.initial_init_content = [
            '"""A test app"""',
            '',
            "__version__ = '0.0.1'",
            "__url__ = 'https://github.com/michaeljoseph/testapp'",
            "__author__ = 'Michael Joseph'",
            "__email__ = 'michaeljoseph@gmail.com'"
        ]
        with open(self.tmp_file, 'w') as init_file:
            init_file.write('\n'.join(self.initial_init_content))

    def test_extract_attribute(self):
        self.assertEquals(
            '0.0.1',
            extract_attribute('test_app', '__version__')
        )

    def test_replace_attribute(self):
        replace_attribute('test_app', '__version__', '1.0.0', dry_run=False)

        expected_content = list(self.initial_init_content)
        expected_content[2] = "__version__ = '1.0.0'"
        self.assertEquals(
            '\n'.join(expected_content),
            ''.join(
                open(self.tmp_file).readlines()
            )
        )

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

    def test_write_new_changelog(self):
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
            '# [Changelog](None/releases)\n',
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
