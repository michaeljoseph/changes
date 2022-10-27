import os
import tempfile

from plumbum import local
from plumbum.cmd import virtualenv


def create_venv(tmp_dir=None):
    if not tmp_dir:
        tmp_dir = tempfile.mkdtemp()
    virtualenv(tmp_dir)
    return tmp_dir


def install(package_name, venv_dir):
    if not os.path.exists(venv_dir):
        venv_dir = create_venv()
    pip = f'{venv_dir}/bin/pip'
    local[pip]('install', package_name)
