from pathlib import Path

import attr
import requests
import uritemplate

EXT_TO_MIME_TYPE = {
    '.gz': 'application/x-gzip',
    '.whl': 'application/zip',
    '.zip': 'application/zip',
}


@attr.s
class GitHub(object):
    ISSUE_ENDPOINT = 'https://api.github.com/repos{/owner}{/repo}/issues{/number}'
    LABELS_ENDPOINT = 'https://api.github.com/repos{/owner}{/repo}/labels'
    RELEASES_ENDPOINT = 'https://api.github.com/repos{/owner}{/repo}/releases'

    repository = attr.ib()

    @property
    def owner(self):
        return self.repository.owner

    @property
    def repo(self):
        return self.repository.repo

    @property
    def auth_token(self):
        return self.repository.auth_token

    @property
    def headers(self):
        # TODO: requests.Session
        return {'Authorization': f'token {self.auth_token}'}

    def pull_request(self, pr_num):
        pull_request_api_url = uritemplate.expand(
            self.ISSUE_ENDPOINT, dict(owner=self.owner, repo=self.repo, number=pr_num)
        )

        return requests.get(pull_request_api_url, headers=self.headers).json()

    def labels(self):
        labels_api_url = uritemplate.expand(
            self.LABELS_ENDPOINT, dict(owner=self.owner, repo=self.repo)
        )

        return requests.get(labels_api_url, headers=self.headers).json()

    def create_release(self, release, uploads=None):
        params = {
            'tag_name': release.version,
            'name': release.name,
            'body': release.description,
            # 'prerelease': True,
        }

        releases_api_url = uritemplate.expand(
            self.RELEASES_ENDPOINT, dict(owner=self.owner, repo=self.repo)
        )

        response = requests.post(
            releases_api_url, headers=self.headers, json=params
        ).json()

        upload_url = response['upload_url']
        upload_responses = (
            [self.create_upload(upload_url, Path(upload)) for upload in uploads]
            if uploads
            else []
        )

        return response, upload_responses

    def create_upload(self, upload_url, upload_path):
        requests.post(
            uritemplate.expand(upload_url, {'name': upload_path.name}),
            headers=dict(
                **self.headers, **{'content-type': EXT_TO_MIME_TYPE[upload_path.ext]}
            ),
            data=upload_path.read_bytes(),
            verify=False,
        )
