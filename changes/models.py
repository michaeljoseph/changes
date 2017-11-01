import re
import shlex

import attr
import semantic_version
import uritemplate
import requests
import giturlparse
from plumbum.cmd import git

MERGED_PULL_REQUEST = re.compile(
    r'^([0-9a-f]{5,40}) Merge pull request #(\w+)'
)

GITHUB_PULL_REQUEST_API = (
    'https://api.github.com/repos{/owner}{/repo}/issues{/number}'
)
GITHUB_LABEL_API = (
    'https://api.github.com/repos{/owner}{/repo}/labels'
)


def changes_to_release_type(repository):
    pull_request_labels = set()
    changes = repository.changes_since_last_version

    for change in changes:
        for label in change.labels:
            pull_request_labels.add(label)

    change_descriptions = [
        '\n'.join([change.title, change.description]) for change in changes
    ]

    current_version = repository.latest_version
    if 'BREAKING CHANGE' in change_descriptions:
        return 'major', Release.BREAKING_CHANGE, current_version.next_major()
    elif 'enhancement' in pull_request_labels:
        return 'minor', Release.FEATURE, current_version.next_minor()
    elif 'bug' in pull_request_labels:
        return 'patch', Release.FIX, current_version.next_patch()
    else:
        return None, Release.NO_CHANGE, current_version


@attr.s
class Release:
    NO_CHANGE = 'nochanges'
    BREAKING_CHANGE = 'breaking'
    FEATURE = 'feature'
    FIX = 'fix'

    release_date = attr.ib()
    version = attr.ib()
    description = attr.ib(default=attr.Factory(str))
    name = attr.ib(default=attr.Factory(str))
    changes = attr.ib(default=attr.Factory(dict))


@attr.s
class PullRequest:
    number = attr.ib()
    title = attr.ib()
    description = attr.ib()
    author = attr.ib()
    labels = attr.ib(default=attr.Factory(list))

    @classmethod
    def from_github(cls, api_response):
        return cls(
            number=api_response['number'],
            title=api_response['title'],
            description=api_response['body'],
            author=api_response['user']['login'],
            labels=[
                label['name']
                for label in api_response['labels']
            ],
        )


@attr.s
class GitRepository:
    VERSION_ZERO = semantic_version.Version('0.0.0')
    # TODO: handle multiple remotes (cookiecutter [non-owner maintainer])
    REMOTE_NAME = 'origin'

    auth_token = attr.ib(default=None)

    @property
    def remote_url(self):
        return git(shlex.split('config --get remote.{}.url'.format(
            self.REMOTE_NAME
        )))

    @property
    def parsed_repo(self):
        return giturlparse.parse(self.remote_url)

    @property
    def repo(self):
        return self.parsed_repo.repo

    @property
    def owner(self):
        return self.parsed_repo.owner

    @property
    def platform(self):
        return self.parsed_repo.platform

    @property
    def is_github(self):
        return self.parsed_repo.github

    @property
    def is_bitbucket(self):
        return self.parsed_repo.bitbucket

    @property
    def commit_history(self):
        return [
            commit_message
            for commit_message in git(shlex.split(
                'log --oneline --no-color'
            )).split('\n')
            if commit_message
        ]

    @property
    def first_commit_sha(self):
        return git(
            'rev-list', '--max-parents=0', 'HEAD'
        )

    @property
    def tags(self):
        return git(shlex.split('tag --list')).split('\n')

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
        return max(self.versions) if self.versions else self.VERSION_ZERO

    def merges_since(self, version=None):
        if version == semantic_version.Version('0.0.0'):
            version = self.first_commit_sha

        revision_range = ' {}..HEAD'.format(version) if version else ''

        merge_commits = git(shlex.split(
            'log --oneline --merges --no-color{}'.format(revision_range)
        )).split('\n')
        return merge_commits

    @property
    def files_modified_in_last_commit(self):
        return git(shlex.split('diff --name -only --diff -filter=d'))

    @property
    def dirty_files(self):
        return [
            modified_path
            for modified_path in git(shlex.split('-c color.status=false status --short --branch'))
            if modified_path.startswith(' M')
        ]

    @classmethod
    def add(cls, files_to_add):
        return git(['add'] + files_to_add)

    @classmethod
    def commit(cls, message):
        return git(shlex.split(
            'commit --message="{}" '.format(message)
        ))

    @classmethod
    def tag(cls, version):
        # TODO: signed tags
        return git(
            shlex.split('tag --annotate {version} --message="{version}"'.format(
                version=version
            ))
        )

    @classmethod
    def push(cls, tags=False):
        return git(['push'] + ['--tags'] if tags else [])

    # TODO: pull_requests_since(version=None)
    # TODO: cached_property
    @property
    def changes_since_last_version(self):
        pull_requests = []

        for index, commit_msg in enumerate(self.merges_since(self.latest_version)):
            matches = MERGED_PULL_REQUEST.findall(commit_msg)

            if matches:
                _, pull_request_number = matches[0]

                pull_requests.append(PullRequest.from_github(
                    self.github_pull_request(pull_request_number)
                ))
        return pull_requests

    def github_pull_request(self, pr_num):
        pull_request_api_url = uritemplate.expand(
            GITHUB_PULL_REQUEST_API,
            dict(
                owner=self.owner,
                repo=self.repo,
                number=pr_num
            ),
        )

        return requests.get(
            pull_request_api_url,
            headers={
                'Authorization': 'token {}'.format(self.auth_token)
            },
        ).json()

    # TODO: cached_property
    # TODO: move to test fixture
    def github_labels(self):

        labels_api_url = uritemplate.expand(
            GITHUB_LABEL_API,
            dict(
                owner=self.owner,
                repo=self.repo,
            ),
        )

        return requests.get(
            labels_api_url,
            headers={
                'Authorization': 'token {}'.format(self.auth_token)
            },
        ).json()



