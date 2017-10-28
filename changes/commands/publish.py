import click
from datetime import date

import changes
from changes.commands import error, info
from changes.models import changes_to_release_type, Release


def publish():
    bumpversion_part, release_type, proposed_version = changes_to_release_type(
        changes.project_settings.repository
    )
    release = Release(
        release_date=date.today().isoformat(),
        version=str(proposed_version),
   )

    if release.version == str(changes.project_settings.repository.latest_version):
        info('No staged release to publish')
        return



    info('Publish release {}'.format(release.version))
    if click.confirm('Happy to release {}'.format(release.version)):
        files_to_add = [

        ]
        # git add files
        # ? confirm staged diff?
        commit_message = ''
        # make commit
        # ? confirm commit message?

        # tag => release format string

        # git push --tags

        # github release [artifacts?]

    # Release done

    # Verifying

    # install from release (gh
    #     verify release
