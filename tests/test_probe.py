from changes import probe
from . import BaseTestCase


class ProbeTestCase(BaseTestCase):

    def test_probe_project(self):
        self.assertTrue(probe.probe_project(self.module_name))
