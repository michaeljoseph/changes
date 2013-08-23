import tempfile

from unittest2 import TestCase
from changes.cli import increment, write_new_changelog
import os
import shutil


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
        os.mkdir('test_app')
        tmp_file = 'test_app/__init__.py'

        content = [
            'This is the heading\n\n',
            'This is the first line\n',
        ]

        with open(tmp_file, 'w') as existing_file:
            existing_file.writelines(content)

        write_new_changelog('test_app', tmp_file, 'Now this is')

        self.assertEquals(
            ''.join(content),
            ''.join(
                open(tmp_file).readlines()
            )            
        )

        with open(tmp_file, 'w') as existing_file:
            existing_file.writelines(content)

        write_new_changelog(
            'test_app',
            tmp_file,
            'Now this is',
            dry_run=False
        )
        expected_content = [
            '# (Changelog)[None/releases]\n\n',
            'Now this is\n\n',
            'This is the first line\n'
        ]
        self.assertEquals(
            ''.join(expected_content),
            ''.join(
                open(tmp_file).readlines()
            )
        )

        os.remove(tmp_file)
        os.rmdir('test_app')

