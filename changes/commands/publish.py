import click
import changes
from changes.commands import error, info


def publish():

    release = changes.release

    if not release:
        error('No staged release found')
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
