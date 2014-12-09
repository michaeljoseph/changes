import logging
import io
import re

from plumbum.cmd import git

log = logging.getLogger(__name__)


def write_new_changelog(repo_url, filename, content_lines, dry_run=True):
    heading_and_newline = '# [Changelog](%s/releases)\n' % repo_url

    with io.open(filename, 'r+') as f:
        existing = f.readlines()

    output = existing[2:]
    output.insert(0, '\n')

    for index, line in enumerate(content_lines):
        output.insert(0, content_lines[len(content_lines) - index - 1])

    output.insert(0, heading_and_newline)

    output = ''.join(output)

    if not dry_run:
        with io.open(filename, 'w+') as f:
            f.write(output)
    else:
        log.info('New changelog:\n%s', ''.join(content_lines))


def replace_sha_with_commit_link(repo_url, git_log_content):
    git_log_content = git_log_content.split('\n')
    for index, line in enumerate(git_log_content):
        # http://stackoverflow.com/a/468378/5549
        sha1_re = re.match(r'^[0-9a-f]{5,40}\b', line)
        if sha1_re:
            sha1 = sha1_re.group()

            new_line = line.replace(
                sha1,
                '[%s](%s/commit/%s)' % (sha1, repo_url, sha1)
            )
            log.debug('old line: %s\nnew line: %s', line, new_line)
            git_log_content[index] = new_line

    return git_log_content


def generate_changelog(context):
    """Generates an automatic changelog from your commit messages."""

    changelog_content = [
        '\n## [%s](%s/compare/%s...%s)\n\n' % (
            context.new_version, context.repo_url,
            context.current_version, context.new_version,
        )
    ]

    git_log_content = None
    git_log = 'log --oneline --no-merges --no-color'.split(' ')
    try:
        git_log_tag = git_log + ['%s..master' % context.current_version]
        git_log_content = git(git_log_tag)
        log.debug('content: %s' % git_log_content)
    except:
        log.warn('Error diffing previous version, initial release')
        git_log_content = git(git_log)

    git_log_content = replace_sha_with_commit_link(context.repo_url, git_log_content)
    # turn change log entries into markdown bullet points
    if git_log_content:
        [
            changelog_content.append('* %s\n' % line)
            if line else line
            for line in git_log_content[:-1]
        ]

    write_new_changelog(
        context.repo_url,
        'CHANGELOG.md',
        changelog_content,
        dry_run=context.dry_run
    )
    log.info('Added content to CHANGELOG.md')
    context.changelog_content = changelog_content
