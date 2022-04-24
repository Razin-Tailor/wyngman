from unittest import mock
import pytest
import sys

sys.path.insert(0, './')
sys.path.insert(0, '../')

from main import main

def test_help_flag():
    with pytest.raises(SystemExit):
        main(['--help'])

def test_help_pos_cmd():
    with pytest.raises(SystemExit):
        main(['help'])

def test_main_cognito_help():
    with pytest.raises(SystemExit):
        main(['cognito', '--help'])

