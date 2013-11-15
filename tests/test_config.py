from changes import config
from . import BaseTestCase


class ConfigTestCase(BaseTestCase):
    arguments = {
        '--debug': True,
        '--dry-run': False,
        '--help': False,
        '--major': False,
        '--minor': False,
        '--new-version': '0.0.1',
        'new_version': '0.0.1',
        '--noinput': True,
        '--patch': True,
        '--pypi': None,
        '--skip-changelog': False,
        '--test-command': None,
        '--tox': False,
        '--version-prefix': None,
        '<module_name>': 'changes',
        'bump_version': False,
        'changelog': True,
        'install': False,
        'pypi': False,
        'release': False,
        'tag': False,
        'test': False,
        'upload': False
    }

    def setUp(self):
        config.arguments = self.arguments

    def test_common_arguments(self):
        expected_arguments = (
            'changes',
            False,
            '0.0.1',
        )
        self.assertEquals(
            expected_arguments,
            config.common_arguments()
        )
