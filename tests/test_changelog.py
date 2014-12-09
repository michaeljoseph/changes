from click.testing import CliRunner

from changes import changelog, cli
from . import context, setup, teardown


def test_write_new_changelog():
    content = [
        'This is the heading\n\n',
        'This is the first line\n',
    ]

    with open(context.tmp_file, 'w') as existing_file:
        existing_file.writelines(content)

    changelog.write_new_changelog('test_app', context.tmp_file, 'Now this is')

    assert ''.join(content) ==  ''.join(open(context.tmp_file).readlines())

    with open(context.tmp_file, 'w') as existing_file:
        existing_file.writelines(content)

    changelog.write_new_changelog(
        'https://github.com/someuser/test_app',
        context.tmp_file,
        'Now this is',
        dry_run=False
    )
    expected_content = [
        '# [Changelog](https://github.com/someuser/test_app/releases)\n',
        'Now this is\n',
        'This is the first line\n'
    ]

    assert ''.join(expected_content) ==  ''.join(open(context.tmp_file).readlines())

def test_replace_sha_with_commit_link():
    repo_url = 'http://github.com/michaeljoseph/changes'
    log = 'dde9538 Coverage for all python version runs'
    expected_content = [
        '[dde9538](http://github.com/michaeljoseph/changes/commit/dde9538) Coverage for all python version runs'
    ]
    assert expected_content == changelog.replace_sha_with_commit_link(repo_url, log)


def test_generate_changelog():
    changelog.generate_changelog(context)
    assert isinstance(context.changelog_content, list)
