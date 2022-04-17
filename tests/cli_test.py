""" Tests for aws-helper cli"""
from importlib.metadata import version
from os import linesep

import pytest
from cli_test_helpers import shell


def test_run_as_module():
    """ Can this package run as a python module ?"""

    result = shell('python -m aws-helper --help')
    assert result.exit_code == 1


def test_entrypoint():
    """ Is entrypoint script installed? (setup.py) """
    result = shell('aws-helper --help')
    assert result.exit_code == 0


def test_version():
    """ Does --version display information as expected? """
    expected_version = version('aws-helper')
    result = shell('aws-helper --version')
