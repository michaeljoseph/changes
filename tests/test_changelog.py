from changes import changelog
from . import BaseTestCase


class ChangeLogTestCase(BaseTestCase):

    def test_write_new_changelog(self):
        content = [
            'This is the heading\n\n',
            'This is the first line\n',
        ]

        with open(self.tmp_file, 'w') as existing_file:
            existing_file.writelines(content)

        changelog.write_new_changelog('test_app', self.tmp_file, 'Now this is')

        self.assertEquals(
            ''.join(content),
            ''.join(
                open(self.tmp_file).readlines()
            )
        )

        with open(self.tmp_file, 'w') as existing_file:
            existing_file.writelines(content)

        changelog.write_new_changelog(
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

    def test_changelog(self):
        pass
