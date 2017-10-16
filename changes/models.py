import re
import shlex

import semantic_version
import uritemplate
import requests
import giturlparse
from plumbum.cmd import git

MERGED_PULL_REQUEST = re.compile(
    r'^([0-9a-f]{5,40}) Merge pull request #(\w+)'
)

PULL_REQUEST_API = 'https://api.github.com/repos{/owner}{/repo}/issues{/number}'


class PullRequest:
    title = None
    description = None
    author = None
    labels = []

    def __init__(self, **kwargs):
        # github
        self.number = kwargs['number']
        self.title = kwargs['title']
        self.description = kwargs['body']
        self.author = kwargs['user']['login']
        self.labels = [
            label['name']
            for label in kwargs['labels']
        ]


class GitRepository:
    auth_token = None

    def __init__(self, url=None):
        self.parsed_repo = (
            url or
            # TODO: handle multiple remotes (cookiecutter [non-owner maintainer])
            # giturlparse.parse(
            #     git(shlex.split('config --get remote.upstream.url'))
            # ) or
            giturlparse.parse(
                git(shlex.split('config --get remote.origin.url'))
            )
        )
        self.commit_history = [
            commit_message
            for commit_message in git(shlex.split(
                'log --oneline --no-color'
            )).split('\n')
            if commit_message
        ]

        self.first_commit_sha = git(
            'rev-list', '--max-parents=0', 'HEAD'
        )
        self.tags = git(shlex.split('tag --list')).split('\n')

    @property
    def versions(self):
        versions = []
        for tag in self.tags:
            try:
                versions.append(semantic_version.Version(tag))
            except ValueError:
                pass
        return versions

    @property
    def latest_version(self) -> semantic_version.Version:
        return max(self.versions) if self.versions else semantic_version.Version('0.0.0')

    def merges_since(self, version=None):
        print('merged since')
        print(version)
        
        if version == semantic_version.Version('0.0.0'):
            print('not a real version')
        #     version = self.first_commit_sha

        revision_range = ' {}..HEAD'.format(version) if version else ''

        merge_commits = git(shlex.split(
            'log --oneline --merges --no-color{}'.format(revision_range)
        )).split('\n')
        return merge_commits

    # TODO: pull_requests_since(version=None)
    @property
    def changes_since_last_version(self):
        pull_requests = []

        for index, commit_msg in enumerate(self.merges_since(self.latest_version)):
            matches = MERGED_PULL_REQUEST.findall(commit_msg)

            if matches:
                _, pull_request_number = matches[0]

                pr = self.get_pull_request(pull_request_number)
                pull_requests.append(
                    PullRequest(
                        **pr
                    )
                )
        return pull_requests

    # github api
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
