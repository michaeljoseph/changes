import os
import tempfile

import virtualenv


def create_venv(tmp_dir=None):
    if not tmp_dir:
        tmp_dir = tempfile.mkdtemp()
    virtualenv.create_environment(tmp_dir, site_packages=False)
    return tmp_dir


def install(package_name, venv_dir):
    if not os.path.exists(venv_dir):
        venv_dir = create_venv()
    virtualenv.install_wheel(
        [package_name],
        '%s/bin/python' % venv_dir,
    )
