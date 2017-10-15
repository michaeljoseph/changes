from changes import attributes

from . import context

import pytest


@pytest.mark.skip('bumpversion')
def test_extract_attribute(python_module):
    assert '0.0.1' == attributes.extract_attribute(
        'test_app',
        '__version__'
    )


@pytest.mark.skip('bumpversion')
def test_replace_attribute(python_module):
    attributes.replace_attribute(
        'test_app',
        '__version__',
        '1.0.0',
        dry_run=False
    )
    expected_content = list(context.initial_init_content)
    expected_content[2] = "__version__ = '1.0.0'"
    assert '\n'.join(expected_content) == ''.join(open(context.tmp_file).readlines())


@pytest.mark.skip('bumpversion')
def test_replace_attribute_dry_run(python_module):
    attributes.replace_attribute(
        'test_app',
        '__version__',
        '1.0.0',
        dry_run=True
    )
    expected_content = list(context.initial_init_content)
    assert '\n'.join(expected_content) == ''.join(open(context.tmp_file).readlines())


@pytest.mark.skip('bumpversion')
def test_has_attribute(python_module):
    assert attributes.has_attribute(context.module_name, '__version__')
