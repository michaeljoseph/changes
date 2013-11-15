from changes import config, probe
from . import BaseTestCase


class ProbeTestCase(BaseTestCase):

    def test_probe_project(self):
        self.assertTrue(probe.probe_project(self.module_name))

    def test_probe_with_alt_requirements(self):
        config.arguments['--requirements'] = 'test-requirements.txt'
        self.assertFalse(probe.probe_project(self.module_name))

    def test_has_requirements(self):
        self.assertTrue(probe.has_requirement('unittest2'))
