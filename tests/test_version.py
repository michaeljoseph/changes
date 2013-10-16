from unittest2 import TestCase

from changes import version
from . import BaseTestCase


class VersionTestCase(TestCase):

    def test_increment(self):
        self.assertEquals(
            '1.0.0',
            version.increment('0.0.1', major=True)
        )

        self.assertEquals(
            '0.1.0',
            version.increment('0.0.1', minor=True)
        )

        self.assertEquals(
            '1.0.1',
            version.increment('1.0.0', patch=True)
        )

    def test_strip_long_arguments(self):
        arguments = {
            '--major': True,
            '--minor': False,
            '--patch': False,
        }
        long_keys = ['--major', '--minor', '--patch']
        expected = {
            'major': True,
            'minor': False,
            'patch': False,
        }
        self.assertEquals(
            expected,
            version.strip_long_arguments(arguments, long_keys)
        )


class CurrentVersionTestCase(BaseTestCase):

    def test_current_version(self):
        self.assertEquals(
            '0.0.1',
            version.current_version(self.module_name)
        )
