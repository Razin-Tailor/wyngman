import os
import stat
import sys

import pytest

from wyngman.utils import configure_wyngman
from wyngman.utils import is_configured


CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.wyngman')
CREDENTIALS_PATH = os.path.join(
    os.path.expanduser(
        '~',
    ), '.wyngman', 'credentials.json',
)


@pytest.fixture
def configure_data():
    if is_configured():
        os.remove(CREDENTIALS_PATH)
    status = os.stat(CONFIG_PATH)
    current_status = int(oct(status.st_mode)[-3:], 8)
    # REVIKE Permission to Write
    os.chmod(CONFIG_PATH, 0o400)
    data = {
        'access_key': 'AKIAJ25KSNP7LLSFWS5A',
        'secret_key': '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',
        'region': 'us-east-1',
        'output_fmt': 'json',
    }
    yield data
    if os.path.isfile(CREDENTIALS_PATH):
        os.remove(CREDENTIALS_PATH)
    os.chmod(CONFIG_PATH, current_status)


@pytest.fixture
def with_permission_configure_data():
    if is_configured():
        os.remove(CREDENTIALS_PATH)
    elif not os.path.isdir(CONFIG_PATH):
        os.makedirs(CONFIG_PATH)
    # Add Permission to Write
    status = os.stat(CONFIG_PATH)
    current_status = int(oct(status.st_mode)[-3:], 8)

    os.chmod(CONFIG_PATH, 0o755)
    data = {
        'access_key': 'AKIAJ25KSNP7LLSFWS5A',
        'secret_key': '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',
        'region': 'us-east-1',
        'output_fmt': 'json',
    }
    yield data
    os.chmod(CONFIG_PATH, current_status)
    if os.path.isfile(CREDENTIALS_PATH):
        os.remove(CREDENTIALS_PATH)


def test_is_configured_no_dir():
    if os.path.isdir(CONFIG_PATH):
        os.rmdir(CONFIG_PATH)
    assert is_configured() == False


def test_is_configured_no_file():
    if not os.path.isdir(CONFIG_PATH):
        os.makedirs(CONFIG_PATH)
    if os.path.isfile(CREDENTIALS_PATH):
        os.remove(CREDENTIALS_PATH)
    assert is_configured() == False


def test_configure_wyngman_no_permission(configure_data):
    with pytest.raises(PermissionError) as exc_info:
        configure_wyngman(configure_data)


def test_configure_wyngman_with_permission(with_permission_configure_data):
    configure_wyngman(with_permission_configure_data)
    assert os.path.isfile(CREDENTIALS_PATH)
