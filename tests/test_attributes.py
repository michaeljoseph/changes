from changes import attributes

from . import *

def test_extract_attribute():
    assert '0.0.1' == attributes.extract_attribute('test_app', '__version__')


def test_replace_attribute():
    attributes.replace_attribute(
        'test_app',
        '__version__',
        '1.0.0',
        dry_run=False
    )
    expected_content = list(initial_init_content)
    expected_content[2] = "__version__ = '1.0.0'"
    assert '\n'.join(expected_content) == ''.join(open(tmp_file).readlines())


def test_replace_attribute_dry_run():
    attributes.replace_attribute(
        'test_app',
        '__version__',
        '1.0.0',
        dry_run=True
    )
    expected_content = list(initial_init_content)
    assert '\n'.join(expected_content) == ''.join(open(tmp_file).readlines())


def test_has_attribute():
    assert attributes.has_attribute(module_name, '__version__')
