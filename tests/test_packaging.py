from changes import config, packaging
from . import BaseTestCase


class PackagingTestCase(BaseTestCase):

    def test_install(self):
        config.arguments['--dry-run'] = True
        packaging.install()

    def test_install_with_module_name(self):
        config.arguments['--dry-run'] = True
        config.arguments['--module-name'] = 'thing'
        packaging.install()

    def test_make_virtualenv(self):
        packaging.make_virtualenv()

    def test_upload(self):
        config.arguments['--dry-run'] = True
        packaging.upload()

    def test_pypi(self):
        config.arguments['--dry-run'] = True
        packaging.pypi()
