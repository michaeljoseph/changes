import logging

import click

from changes.changelog import generate_changelog
from changes.config import project_config, store_settings
from changes.packaging import build_distributions, install_package, upload_package, install_from_pypi
from changes.vcs import tag_and_push, commit_version_change, create_github_release, upload_release_distributions
from changes.verification import run_tests
from changes.version import increment_version

log = logging.getLogger(__name__)


def publish(context):
    """Publishes the project"""
    commit_version_change(context)

    if context.github:
        # github token
        project_settings = project_config(context.module_name)
        if not project_settings['gh_token']:
            click.echo('You need a GitHub token for changes to create a release.')
            click.pause('Press [enter] to launch the GitHub "New personal access '
                        'token" page, to create a token for changes.')
            click.launch('https://github.com/settings/tokens/new')
            project_settings['gh_token'] = click.prompt('Enter your changes token')

            store_settings(context.module_name, project_settings)
        description = click.prompt('Describe this release')

        upload_url = create_github_release(context, project_settings['gh_token'], description)

        upload_release_distributions(
            context,
            project_settings['gh_token'],
            build_distributions(context),
            upload_url,
        )

        click.pause('Press [enter] to review and update your new release')
        click.launch('{0}/releases/tag/{1}'.format(context.repo_url, context.new_version))
    else:
        tag_and_push(context)


def perform_release(context):
    """Executes the release process."""
    try:
        run_tests()

        if not context.skip_changelog:
            generate_changelog(context)

        increment_version(context)

        build_distributions(context)

        install_package(context)

        upload_package(context)

        install_from_pypi(context)

        publish(context)
    except:
        log.exception('Error releasing')
