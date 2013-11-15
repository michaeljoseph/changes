import os
import shutil

from unittest2 import TestCase

from changes import config


class BaseTestCase(TestCase):
    module_name = 'test_app'
    tmp_file = '%s/__init__.py' % module_name

    def setUp(self):
        if not os.path.exists(self.module_name):
            os.mkdir(self.module_name)

        self.initial_init_content = [
            '"""A test app"""',
            '',
            "__version__ = '0.0.1'",
            "__url__ = 'https://github.com/someuser/%s'" % self.module_name,
            "__author__ = 'Some User'",
            "__email__ = 'someuser@gmail.com'"
        ]
        with open(self.tmp_file, 'w') as init_file:
            init_file.write('\n'.join(self.initial_init_content))

        with open('%s/requirements.txt' % self.module_name, 'w') as req_file:
            req_file.write('unittest2')

        config.arguments.update({
            '<module_name>': 'test_app',
            '--dry-run': True,
        })

    def tearDown(self):
        if os.path.exists(self.tmp_file):
            shutil.rmtree(self.module_name)
