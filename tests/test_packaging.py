from changes import config, packaging
from . import BaseTestCase


class PackagingTestCase(BaseTestCase):

    def test_install(self):
        packaging.install()

    def test_install_with_module_name(self):
        config.arguments['--package-name'] = 'thing'
        packaging.install()

    def test_make_virtualenv(self):
        packaging.make_virtualenv()

    def test_upload(self):
        packaging.upload()

    def test_pypi(self):
        packaging.pypi()
