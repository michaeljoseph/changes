import re

import attr
import semantic_version
import shlex
import giturlparse
from plumbum.cmd import git

from changes import services

GITHUB_MERGED_PULL_REQUEST = re.compile(
    r'^([0-9a-f]{5,40}) Merge pull request #(\w+)'
)

# def gitx(args):
#     if changes.debug:
#         print('git {}'.format(args))
#     return git(shlex.split(args))


@attr.s
class GitRepository(object):
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
    def merges_since_latest_version(self):
        return self.merges_since(self.latest_version)

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

    @staticmethod
    def add(files_to_add):
        return git(['add'] + files_to_add)

    @staticmethod
    def commit(message):
        return git(shlex.split(
            'commit --message="{}" '.format(message)
        ))

    @staticmethod
    def discard(file_paths):
        git(['checkout', '--'] + file_paths)

    @staticmethod
    def tag(version):
        # TODO: signed tags
        return git(
            shlex.split('tag --annotate {version} --message="{version}"'.format(
                version=version
            ))
        )

    @staticmethod
    def push():
        return git(shlex.split('push --tags'))


@attr.s
class GitHubRepository(GitRepository):
    api = attr.ib(default=None)

    def __attrs_post_init__(self):
        self.api = services.GitHub(self)

    # TODO: cached_property
    @property
    def labels(self):
        return self.api.labels()

    # TODO: cached_property
    @property
    def pull_requests_since_latest_version(self):
        return [
            PullRequest.from_github(self.api.pull_request(pull_request_number))
            for pull_request_number in self.pull_request_numbers_since_latest_version
        ]

    @property
    def pull_request_numbers_since_latest_version(self):
        pull_request_numbers = []

        for commit_msg in self.merges_since(self.latest_version):

            matches = GITHUB_MERGED_PULL_REQUEST.findall(commit_msg)

            if matches:
                _, pull_request_number = matches[0]
                pull_request_numbers.append(pull_request_number)

        return pull_request_numbers

    def create_release(self, release):
        return self.api.create_release(release)


@attr.s
class PullRequest(object):
    number = attr.ib()
    title = attr.ib()
    description = attr.ib()
    author = attr.ib()
    body = attr.ib()
    user = attr.ib()
    labels = attr.ib(default=attr.Factory(list))

    @property
    def description(self):
        return self.body

    @property
    def author(self):
        return self.user['login']

    @property
    def label_names(self):
        return [
            label['name']
            for label in self.labels
        ]

    @classmethod
    def from_github(cls, api_response):
        return cls(**{
            k.name: api_response[k.name]
            for k in attr.fields(cls)
        })

    @classmethod
    def from_number(cls, number):
        pass