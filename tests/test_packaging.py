from changes import packaging

from click.testing import CliRunner

from . import context


def test_build_distributions():
    with CliRunner().isolated_filesystem():
        packaging.build_distributions(context)


def test_install_package():
    with CliRunner().isolated_filesystem():
        packaging.install_package(context)


def test_upload_package():
    with CliRunner().isolated_filesystem():
        packaging.upload_package(context)


def test_install_from_pypi():
    with CliRunner().isolated_filesystem():
        packaging.install_from_pypi(context)
