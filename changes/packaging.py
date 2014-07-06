import logging

from path import path
import sh

from changes import config, shell, util, venv, verification

log = logging.getLogger(__name__)


def install():
    module_name, dry_run, new_version = config.common_arguments()
    commands = ['setup.py', 'clean', 'bdist_wheel']

    result = shell.handle_dry_run(sh.python, tuple(commands))

    if result:
        with util.mktmpdir() as tmp_dir:
            venv.create_venv(tmp_dir=tmp_dir)
            package_name = config.arguments.get('--package-name') or module_name
            try:
                print(package_name)
                print(tmp_dir)
                venv.install(package_name, tmp_dir)
                log.info('Successfully installed %s sdist', module_name)
                if verification.run_test_command():
                    log.info('Successfully ran test command: %s',
                             config.arguments['--test-command'])
            except Exception, e:
                raise Exception('Error installing %s sdist', module_name, e)


def upload():
    module_name, dry_run, new_version = config.common_arguments()
    pypi = config.arguments['--pypi']

    upload_args = 'setup.py clean sdist upload'.split(' ')
    if pypi:
        upload_args.extend(['-r',  pypi])

    upload_result = shell.handle_dry_run(sh.python, tuple(upload_args))
    if not upload_result:
        raise Exception('Error uploading')
    else:
        log.info('Succesfully uploaded %s %s', module_name, new_version)


def pypi():
    module_name, dry_run, _ = config.common_arguments()

    tmp_dir = venv.create_venv()
    install_cmd = '%s/bin/pip install %s' % (tmp_dir, module_name)

    package_index = 'pypi'
    pypi = config.arguments['--pypi']
    if pypi:
        install_cmd += '-i %s' % pypi
        package_index = pypi

    try:
        result = shell.execute(install_cmd, dry_run=dry_run)
        if result:
            log.info('Successfully installed %s from %s',
                     module_name, package_index)
        else:
            log.error('Failed to install %s from %s',
                      module_name, package_index)

        verification.run_test_command()
    except Exception, e:
        log.exception(
            'error installing %s from %s', module_name, package_index
        )
        raise Exception(
            'Error installing %s from %s', module_name, package_index, e
        )

    path(tmp_dir).rmtree(path(tmp_dir))
