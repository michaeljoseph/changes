import re

import giturlparse
from plumbum.cmd import git
from invoke import run


class PullRequest:
    title = None
    description = None
    author = None

    def __init__(self, pr_number, committish):
        self.pr_number = pr_number
        self.committish = committish
    #     - keyed
    #     by
    #     version
    #     - status: open, merged
    #     - issue  # => URL
    #     - title, description
    #     - author
    #     - tags
    #     - (approvers)
    #
    #
    # - since(version)
        pass


def merged_pull_requests():
    commit_history = git(
        'log --oneline --no-merges --no-color'.split(' ')
    ).split('\n')

    pull_requests = []

    for index, commit_msg in enumerate(commit_history):
        matches = re.compile(
            r'^([0-9a-f]{5,40}) Merge pull request #(\w+)',
        ).findall(commit_msg)
        if matches:
            committish, pr_number = matches[0]
            pull_requests.append(PullRequest(pr_number, committish))

    return pull_requests


class GitRepository:
    def __init__(self, url=None):
        self.parsed_repo = url or giturlparse.parse(
            git('config --get remote.origin.url'.split(' '))
        )
        self.commit_history = git(
        'log --oneline --no-merges --no-color'.split(' ')
    ).split('\n')

        self.pull_requests = merged_pull_requests()

        self.tags = git('tag --list'.split(' '))

    @property
    def repo(self):
        return self.parsed_repo.repo

    @property
    def owner(self):
        return self.parsed_repo.owner

    @property
    def github(self):
        return self.parsed_repo.github

    @property
    def bitbucket(self):
        return self.parsed_repo.bitbucket

    def __str__(self):
        return ''.format(

        )
