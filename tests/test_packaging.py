from changes import packaging

from . import context, setup, teardown


def test_build_distributions():
    packaging.build_distributions(context)

def test_install_package():
    packaging.install_package(context)

def test_upload_package():
    packaging.upload_package(context)

def test_install_from_pypi():
    packaging.install_from_pypi(context)
