from changes import attributes

from . import BaseTestCase


class AttributeTestCase(BaseTestCase):


    def test_extract_attribute(self):
        self.assertEquals(
            '0.0.1',
            attributes.extract_attribute('test_app', '__version__')
        )

    def test_replace_attribute(self):
        attributes.replace_attribute(
            'test_app',
            '__version__',
            '1.0.0',
            dry_run=False
        )

        expected_content = list(self.initial_init_content)
        expected_content[2] = "__version__ = '1.0.0'"
        self.assertEquals(
            '\n'.join(expected_content),
            ''.join(
                open(self.tmp_file).readlines()
            )
        )

    def test_has_attribute(self):
        self.assertTrue(
            attributes.has_attribute(
                self.module_name,
                '__version__'
        ))
