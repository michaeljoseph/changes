import attr
import requests
import uritemplate
from pathlib import Path


EXT_TO_MIME_TYPE = {
    '.gz': 'application/x-gzip',
    '.whl': 'application/zip',
    '.zip': 'application/zip',
}


@attr.s
class GitHub(object):
    ISSUE_ENDPOINT = (
        'https://api.github.com/repos{/owner}{/repo}/issues{/number}'
    )
    LABELS_ENDPOINT = (
        'https://api.github.com/repos{/owner}{/repo}/labels'
    )
    RELEASES_ENDPOINT = (
        'https://api.github.com/repos{/owner}{/repo}/releases'
    )

    repository = attr.ib()
    release = attr.ib()

    @property
    def owner(self):
        return self.repository.owner

    @property
    def repo(self):
        return self.repository.repo

    @property
    def auth_token(self):
        return self.repository.auth_token

    def pull_request(self, pr_num):
        pull_request_api_url = uritemplate.expand(
            self.ISSUE_ENDPOINT,
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

    def labels(self):
        labels_api_url = uritemplate.expand(
            self.LABELS_ENDPOINT,
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

    def create_release(self, uploads=None):
        params = {
            'tag_name': self.release.version,
            'name': self.release.name,
            'body': self.release.description,
            # 'prerelease': True,
        }

        releases_api_url = uritemplate.expand(
            self.RELEASES_ENDPOINT,
            dict(
                owner=self.owner,
                repo=self.repo,
            )
        )

        return requests.post(
            releases_api_url,
            headers={
                'Authorization': 'token {}'.format(self.auth_token)
            },
            # auth=(self.auth_token, 'x-oauth-basic'),
            json=params,
        ).json()

        upload_responses = []
        upload_url = response['upload_url']
        for upload in uploads:
            upload = Path(upload)
            upload_responses.append(requests.post(
                uritemplate.expand(
                    upload_url,
                    dict(name=upload.name)
                ),
                # auth=(gh_token, 'x-oauth-basic'),
                headers={
                    'authorization': 'token {}'.format(self.auth_token),
                    'content-type': EXT_TO_MIME_TYPE[distribution.ext],
                },
                data=upload.read_bytes(),
                verify=False,
            ))

        return response, upload_responses
