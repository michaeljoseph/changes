import logging
import re

from changes import attributes, config, shell, version

log = logging.getLogger(__name__)


def write_new_changelog(app_name, filename, content_lines, dry_run=True):
    heading_and_newline = (
        '# [Changelog](%s/releases)\n' %
        attributes.extract_attribute(app_name, '__url__')
    )

    with open(filename, 'r+') as f:
        existing = f.readlines()

    output = existing[2:]
    output.insert(0, '\n')

    for index, line in enumerate(content_lines):
        output.insert(0, content_lines[len(content_lines) - index - 1])

    output.insert(0, heading_and_newline)

    output = ''.join(output)

    if not dry_run:
        with open(filename, 'w+') as f:
            f.write(output)
    else:
        log.info('New changelog:\n%s', ''.join(content_lines))

def replace_sha_with_commit_link(git_log_content):
    repo_url = attributes.extract_attribute(
                    config.common_arguments()[0],
                    '__url__'
                )

    commit_link = ''
    for index, line in enumerate(git_log_content):
        # http://stackoverflow.com/a/468378/5549
        sha1_re = re.match(r'^[0-9a-f]{5,40}\b', line)
        if sha1_re:
            sha1 = sha1_re.group()

            new_line = line.replace(
                sha1,
                '[%s](%s/commit/%s)' % (
                    sha1,
                    attributes.extract_attribute(
                        config.common_arguments()[0],
                        '__url__'
                    ),
                    sha1
                )
            )
            log.debug('old line: %s\nnew line: %s', line, new_line)
            git_log_content[index] = new_line
    return git_log_content

def changelog():
    app_name, dry_run, new_version = config.common_arguments()

    changelog_content = [
        '\n## [%s](%s/compare/%s...%s)\n\n' % (
            new_version, attributes.extract_attribute(app_name, '__url__'),
            version.current_version(app_name), new_version,
        )
    ]

    ## vcs (todo: config templatise all these commands)
    git_log = 'git log --oneline --no-merges'
    version_difference = '%s..master' % version.current_version(app_name)

    git_log_content = shell.execute(
        '%s %s' % (git_log, version_difference),
        dry_run=False
    )
    log.debug('content: %s' % git_log_content)

    if not git_log_content:
        log.debug('sniffing initial release, drop tags: %s', git_log)
        git_log_content = shell.execute(git_log, dry_run=False)

    ## /vcs

    git_log_content = replace_sha_with_commit_link(git_log_content)

    log.debug('content: %s' % git_log_content)

    # makes change log entries into bullet points
    if git_log_content:
        [
            changelog_content.append('* %s' % line)
            if line else line
            for line in git_log_content[:-1]
            # for all except the last line?
        ]

    write_new_changelog(
        app_name,
        config.CHANGELOG,
        changelog_content,
        dry_run=dry_run
    )
    log.info('Added content to CHANGELOG.md')
