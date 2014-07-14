import os
import tempfile

from fabric.api import local


def create_venv(tmp_dir=None):
    if not tmp_dir:
        tmp_dir = tempfile.mkdtemp()
    local('virtualenv --no-site-packages %s' % tmp_dir)
    return tmp_dir


def install(package_name, venv_dir):
    if not os.path.exists(venv_dir):
        venv_dir = create_venv()
    local('%s/bin/pip install %s' % (venv_dir, package_name))
