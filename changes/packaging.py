import logging
import tempfile

from path import path
import sh
import virtualenv

from changes import config, shell, verification

log = logging.getLogger(__name__)


def make_virtualenv():
    tmp_dir = tempfile.mkdtemp()
    virtualenv.create_environment(tmp_dir, site_packages=False)
    return tmp_dir


def install():
    app_name, dry_run, new_version = config.common_arguments()

    result = shell.handle_dry_run(sh.python, ('setup.py', 'clean', 'sdist'))
    if result:
        tmp_dir = make_virtualenv()
        package_name = config.arguments.get('--package-name') or module_name
        try:
            virtualenv.install_sdist(
                config.arguments['<app_name>'],
                'dist/%s-%s.tar.gz' % (module_name, new_version),
                '%s/bin/python' % tmp_dir
            )
            log.info('Successfully installed %s sdist', app_name)
            if verification.run_test_command():
                log.info('Successfully ran test command: %s',
                         config.arguments['--test-command'])
        except:
            raise Exception('Error installing %s sdist', app_name)

        path(tmp_dir).rmtree(path(tmp_dir))


def upload():
    app_name, dry_run, new_version = config.common_arguments()
    pypi = config.arguments['--pypi']

    upload_args = 'setup.py clean sdist upload'.split(' ')
    if pypi:
        upload_args.extend(['-r',  pypi])

    upload_result = shell.handle_dry_run(sh.python, tuple(upload_args))
    if not upload_result:
        raise Exception('Error uploading')
    else:
        log.info('Succesfully uploaded %s %s', app_name, new_version)


def pypi():
    app_name, dry_run, _ = config.common_arguments()

    tmp_dir = make_virtualenv()
    install_cmd = '%s/bin/pip install %s' % (tmp_dir, app_name)

    package_index = 'pypi'
    pypi = config.arguments['--pypi']
    if pypi:
        install_cmd += '-i %s' % pypi
        package_index = pypi

    try:
        result = shell.execute(install_cmd, dry_run=dry_run)
        if result:
            log.info('Successfully installed %s from %s',
                     app_name, package_index)
        else:
            log.error('Failed to install %s from %s',
                      app_name, package_index)

        verification.run_test_command()
    except:
        log.exception('error installing %s from %s', app_name, package_index)
        raise Exception('Error installing %s from %s', app_name, package_index)

    path(tmp_dir).rmtree(path(tmp_dir))
