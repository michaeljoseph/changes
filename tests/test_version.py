import pytest

from changes import version

from .conftest import PYTHON_MODULE


@pytest.mark.skip('bumpversion')
def test_increment():
    assert '1.0.0' == version.increment('0.0.1', major=True)

    assert '0.1.0' == version.increment('0.0.1', minor=True)

    assert '1.0.1' == version.increment('1.0.0', patch=True)


@pytest.mark.skip('bumpversion')
def test_current_version(python_module):
    assert '0.0.1' == version.current_version(PYTHON_MODULE)


@pytest.mark.skip('bumpversion')
def test_get_new_version(mocker):
    with mocker.patch('builtins.input') as mock_raw_input:
        mock_raw_input.return_value = None
        assert '0.1.0' == version.get_new_version(
            PYTHON_MODULE, '0.0.1', True, minor=True
        )
