from enum import Enum

import attr


def changes_to_release_type(repository):
    pull_requests = repository.pull_requests_since_latest_version

    labels = set([
        label_name
        for pull_request in pull_requests
        for label_name in pull_request.label_names
    ])

    descriptions = [
        '\n'.join([
            pull_request.title, pull_request.description
        ])
        for pull_request in pull_requests
    ]

    return determine_release(
        repository.latest_version,
        descriptions,
        labels
    )


def determine_release(latest_version, descriptions, labels):
    if 'BREAKING CHANGE' in descriptions:
        return 'major', ReleaseType.BREAKING_CHANGE, latest_version.next_major()
    elif 'enhancement' in labels:
        return 'minor', ReleaseType.FEATURE, latest_version.next_minor()
    elif 'bug' in labels:
        return 'patch', ReleaseType.FIX, latest_version.next_patch()
    else:
        return None, ReleaseType.NO_CHANGE, latest_version


class ReleaseType(str, Enum):
    NO_CHANGE = 'no-changes'
    BREAKING_CHANGE = 'breaking'
    FEATURE = 'feature'
    FIX = 'fix'


@attr.s
class Release(object):

    release_date = attr.ib()
    version = attr.ib()
    description = attr.ib(default=attr.Factory(str))
    name = attr.ib(default=attr.Factory(str))
    changes = attr.ib(default=attr.Factory(dict))

    @property
    def title(self):
        return '{version} ({release_date})'.format(
            version=self.version,
            release_date=self.release_date
        ) + (' ' + self.name) if self.name else ''


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
        return cls(**api_response)

    @classmethod
    def from_number(cls, number):
        pass

# def gitx(args):
#     if changes.debug:
#         print('git {}'.format(args))
#     return git(shlex.split(args))
