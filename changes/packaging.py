import virtualenv
from path import path

from changes import config, shell, testing


def make_virtualenv():
    tmp_dir = tempfile.mkdtemp()
    virtualenv.create_environment(tmp_dir, site_packages=False)
    return tmp_dir


def install():
    app_name, dry_run, new_version = config.common_arguments()

    result = shell.execute('python setup.py clean sdist', dry_run=dry_run)
    if result:
        tmp_dir = make_virtualenv()
        try:
            virtualenv.install_sdist(
                arguments['<app_name>'],
                'dist/%s-%s.tar.gz' % (app_name, new_version),
                '%s/bin/python' % tmp_dir
            )
            log.info('Successfully installed %s sdist', app_name)
            if testing.run_test_command():
                log.info('Successfully ran test command: %s',
                         arguments['--test-command'])
        except:
            raise Exception('Error installing %s sdist', app_name)

        path(tmp_dir).rmtree(path(tmp_dir))


def upload():
    app_name, dry_run, new_version = config.common_arguments()
    pypi = arguments['--pypi']

    upload = 'python setup.py clean sdist upload'
    if pypi:
        upload = upload + '-r %s' % pypi

    if not shell.execute(upload, dry_run=dry_run):
        raise Exception('Error uploading')
    else:
        log.info('Succesfully uploaded %s %s', app_name, new_version)


def pypi():
    app_name, dry_run, _ = config.common_arguments()
    pypi = arguments['--pypi']
    package_index = 'pypi'

    tmp_dir = make_virtualenv()
    install = '%s/bin/pip install %s' % (tmp_dir, app_name)

    if pypi:
        install = install + '-i %s' % pypi
        package_index = pypi

    try:
        result = shell.execute(install, dry_run=dry_run)
        if result:
            log.info('Successfully installed %s from %s',
                     app_name, package_index)
        else:
            log.error('Failed to install %s from %s',
                      app_name, package_index)

        testing.run_test_command()
    except:
        raise Exception('Error installing %s from %s', app_name, package_index)

    path(tmp_dir).rmtree(path(tmp_dir))
