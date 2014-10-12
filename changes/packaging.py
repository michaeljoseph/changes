import logging

import click
from path import path
from plumbum.cmd import python

from changes import probe, shell, util, venv, verification

log = logging.getLogger(__name__)


def build_package(context):
    """Builds package distributions"""
    build_package_command = 'python setup.py clean sdist bdist_wheel'
    result = shell.dry_run(build_package_command, context.dry_run)
    packages = ', '.join(path('dist').files()) if not context.dry_run else "nothing"

    if not result:
        raise Exception('Error building packages: %s' % result)
    else:
        log.info('Built %s' % packages)


def install_package(context):
    """Attempts to install the sdist and wheel."""
    if not context.dry_run and build_package(context):
        with util.mktmpdir() as tmp_dir:
            venv.create_venv(tmp_dir=tmp_dir)
            for distribution in path('dist').files():
                try:
                    venv.install(distribution, tmp_dir)
                    log.info('Successfully installed %s', distribution)
                    if context.test_command and verification.run_test_command(context.test_command):
                        log.info('Successfully ran test command: %s',
                                 test_command)
                except Exception, e:
                    raise Exception('Error installing distribution %s' % distribution, e)
    else:
        log.info('Dry run, skipping installation')


def upload_package(context):
    """Uploads your project packages to pypi with twine."""
    result = build_package(context)

    upload_args = 'twine upload dist/*'
    if context.pypi:
        upload_args += ' -r %s' % context.pypi

    upload_result = shell.dry_run(upload_args, context.dry_run)
    if not context.dry_run and not upload_result:
        raise Exception('Error uploading: %s' % upload_result)
    else:
        log.info('Successfully uploaded %s:%s', context.module_name, context.new_version)


def install_from_pypi(context):
    """Attempts to install your package from pypi."""

    tmp_dir = venv.create_venv()
    install_cmd = '%s/bin/pip install %s' % (tmp_dir, context.module_name)

    package_index = 'pypi'
    if context.pypi:
        install_cmd += '-i %s' % context.pypi
        package_index = context.pypi

    try:
        result = shell.dry_run(install_cmd, context.dry_run)
        if not context.dry_run and not result:
            log.error('Failed to install %s from %s',
                      context.module_name, package_index)
        else:
            log.info('Successfully installed %s from %s',
                     context.module_name, package_index)

    except Exception, e:
        error_msg = 'Error installing %s from %s' % (context.module_name, package_index)
        log.exception(error_msg)
        raise Exception(error_msg, e)

    path(tmp_dir).rmtree(path(tmp_dir))
