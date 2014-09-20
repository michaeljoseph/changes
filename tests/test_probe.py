from changes import config, probe
from . import BaseTestCase


class ProbeTestCase(BaseTestCase):

    def test_probe_project(self):
        self.assertTrue(probe.probe_project(self.context))

    def test_probe_with_alt_requirements(self):
        self.context.requirements = 'test-requirements.txt'
        with self.assertRaises(Exception):
            probe.probe_project(self.context)
