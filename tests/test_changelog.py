from click.testing import CliRunner

from changes import changelog, cli
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
            'https://github.com/someuser/test_app',
            self.tmp_file,
            'Now this is',
            dry_run=False
        )
        expected_content = [
            '# [Changelog](https://github.com/someuser/test_app/releases)\n',
            'Now this is\n',
            'This is the first line\n'
        ]
        self.assertEquals(
            ''.join(expected_content),
            ''.join(
                open(self.tmp_file).readlines()
            )
        )

    def test_replace_sha_with_commit_link(self):
        repo_url = 'http://github.com/michaeljoseph/changes'
        log = 'dde9538 Coverage for all python version runs'
        self.assertEquals(
            changelog.replace_sha_with_commit_link(repo_url, log),
            ['[dde9538](http://github.com/michaeljoseph/changes/commit/dde9538) Coverage for all python version runs']
        )

    def test_generate_changelog(self):
        changelog.generate_changelog(self.context)
