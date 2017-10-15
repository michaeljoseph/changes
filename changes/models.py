import re
import shlex

import uritemplate
import requests
import giturlparse
from plumbum.cmd import git

MERGED_PULL_REQUEST = re.compile(
    r'^([0-9a-f]{5,40}) Merge pull request #(\w+)'
)

PULL_REQUEST_API = 'https://api.github.com/repos{/owner}{/repo}/pulls{/number}'


class PullRequest:
    title = None
    description = None
    author = None
    labels = []

    def __init__(self, pr_number, committish, title, description, author):
        self.number = pr_number
        self.committish = committish
        self.title = title
        self.description = description
        self.author = author


class GitRepository:
    auth_token = None

    def __init__(self, url=None):
        self.parsed_repo = url or giturlparse.parse(
            git(shlex.split('config --get remote.origin.url'))
        )
        self.commit_history = git(shlex.split(
            'log --oneline --merges --no-color'
        )).split('\n')

        self.tags = git(shlex.split('tag --list')).split('\n')
        print(self.tags)
        import semantic_version
        self.versions = sorted([
            semantic_version.Version(tag)
            for tag in self.tags
            if tag
        ])

    def get_pull_request(self, pr_num):
        return requests.get(
            uritemplate.expand(
                PULL_REQUEST_API,
                dict(
                    owner=self.owner,
                    repo=self.repo,
                    number=pr_num
                ),
            ),
            headers={
                'Authorization': 'token {}'.format(self.auth_token)
            },
        ).json()

    @property
    def pull_requests(self):
        pull_requests = []

        for index, commit_msg in enumerate(self.commit_history):
            matches = MERGED_PULL_REQUEST.findall(commit_msg)
            if matches:
                committish, pr_number = matches[0]
                title = description = author = None
                if self.auth_token:
                    pr = self.get_pull_request(pr_number)
                    title = pr['title']
                    description = pr['body']
                    author = pr['user']['login']

                pull_requests.append(
                    PullRequest(
                        pr_number,
                        committish,
                        title,
                        description,
                        author,
                    )
                )

        return pull_requests

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
