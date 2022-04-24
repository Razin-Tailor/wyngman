""" Tests for wyngman cli"""
import sys
from importlib.metadata import version
from os import linesep

import pytest
from cli_test_helpers import shell

from main import main
sys.path.insert(0, './')
sys.path.insert(0, '../')


def test_run_as_module():
    """ Can this package run as a python module ?"""

    result = shell('python -m wyngman --help')
    assert result.exit_code == 1


def test_entrypoint():
    """ Is entrypoint script installed? (setup.py) """
    result = shell('wyngman --help')
    assert result.exit_code == 0


def test_version():
    """ Does --version display information as expected? """
    expected_version = version('wyngman')
    result = shell('wyngman --version')
    assert result.stdout == f'wyngman {expected_version}{linesep}'
    assert result.exit_code == 0


"""
def test_configure():
    Does --configure work as expected
    result = shell('wyngman configure')
    print(result)
    assert result.exit_code == 111
"""


def test_cli():
    """ Does CLI stop execution w/o a command argument? """
    with pytest.raises(SystemExit):
        main()
        pytest.fail("CLI doesn't abort asking for a command argument")
