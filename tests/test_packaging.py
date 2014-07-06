from changes import config, packaging
from unittest2 import skip
from . import BaseTestCase


class PackagingTestCase(BaseTestCase):

    @skip
    def test_install(self):
        packaging.install()

    @skip
    def test_install_with_module_name(self):
        config.arguments['--package-name'] = 'thing'
        packaging.install()

    def test_upload(self):
        packaging.upload()

    def test_pypi(self):
        packaging.pypi()
