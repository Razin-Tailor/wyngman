"""
Test no argument passed
0. -- Test total users
1. Test list all users
5. Test before date
6. Test after date
7. Test before and after
8. Test show and save for 4, 5, 6, 7
9. -- catch no user pool id provided for cognito class
10. check user-pool doesnot exist
"""
import os
import sys
from turtle import clear

import boto3
import pytest
from dotenv import load_dotenv

from ..utils import configure_aws_helper
from ..utils import is_configured
from .data.user_data import UserData
from cognito import Cognito
from main import main
# from .fixtures.fixture_user import setup_users

sys.path.insert(0, '../')
sys.path.insert(0, '.')


load_dotenv()

CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.aws_helper')
CREDENTIALS_PATH = os.path.join(
    os.path.expanduser(
        '~',
    ), '.aws_helper', 'credentials.json',
)


@pytest.fixture()
def configure():
    if is_configured():
        os.remove(CREDENTIALS_PATH)
    elif not os.path.isdir(CONFIG_PATH):
        os.makedirs(CONFIG_PATH)

    status = os.stat(CONFIG_PATH)
    current_status = int(oct(status.st_mode)[-3:], 8)

    os.chmod(CONFIG_PATH, 0o755)

    data = {
        'access_key': 'AKIARVMWUW4262CCI4MV',
        'secret_key': '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',
        'region': 'ap-south-1',
        'output_fmt': 'json',
    }
    yield data
    os.chmod(CONFIG_PATH, current_status)
    if os.path.isfile(CREDENTIALS_PATH):
        os.remove(CREDENTIALS_PATH)


@pytest.fixture()
def setup_users(configure):
    print(f"{os.getenv('region')}, {os.getenv('test-access-key')}, {os.getenv('test-secret')}")
    print('Configuring tool ...')

    configure_aws_helper(configure)

    cog = boto3.client(
        'cognito-idp', os.getenv('region'), aws_access_key_id=os.getenv(
            'test-access-key',
        ), aws_secret_access_key=os.getenv('test-secret'),
    )
    test_user_pool = cog.create_user_pool(PoolName='test')
    user_1 = cog.admin_create_user(
        UserPoolId=test_user_pool['UserPool']['Id'], Username='user1', UserAttributes=[{'Name': 'email', 'Value': 'a@b.c'}],
    )
    user_2 = cog.admin_create_user(
        UserPoolId=test_user_pool['UserPool']['Id'], Username='user2', UserAttributes=[{'Name': 'email', 'Value': 'd@e.f'}],
    )
    user_3 = cog.admin_create_user(
        UserPoolId=test_user_pool['UserPool']['Id'], Username='user3', UserAttributes=[{'Name': 'email', 'Value': 'g@h.i'}],
    )
    data = {
        'user_pool': test_user_pool, 'users': [
            user_1, user_2, user_3,
        ], 'region': os.getenv('region'),
    }
    yield data
    cog.delete_user_pool(UserPoolId=test_user_pool['UserPool']['Id'])


def clean_output(output: str) -> str:
    return output.replace('\r', '').replace('\n', '').replace(
        '+---------+------------------+----------------------------------+-----------------------+-----------+', '',
    ).replace(
        '+=========+==================+==================================+=======================+===========+', '',
    ).replace(
        '\n ', '',
    ).replace('\n ', '')


def test_total_users(setup_users, capsys):
    """
    Testing the total users for a user-pool-id
    Should return 3
    """

    user_pool_id = os.getenv('user-pool-id')
    print(f'{user_pool_id=}')
    print(f"{user_pool_id=} {os.getenv('user-pool-id')} {os.getenv('region')}")
    cog = Cognito(
        user_pool_id=os.getenv('user-pool-id'),
        region=os.getenv('region'),
        count_users=True,
    )
    cog.handle_cognito()
    captured = capsys.readouterr()
    print(captured)

    assert 'Total Users: 3' in captured.out


def test_no_user_pool_id_provided():
    """Raise an exception if no user-pool-id is provided"""
    with pytest.raises(TypeError):
        cog = Cognito(
            region=os.getenv('region'),
            count_users=True,
        )
        cog.handle_cognito()


def test_user_pool_doesnot_exist(configure):
    """Raise Value Error oif user pool doesnot exist"""
    with pytest.raises(ValueError):
        configure_aws_helper(configure)
        cog = Cognito(
            user_pool_id='somerandomstring',
            region=os.getenv('region'),
            count_users=True,
        )
        cog.handle_cognito()


def test_list_all_users(setup_users, capsys):

    cog = Cognito(
        user_pool_id=os.getenv('user-pool-id'),
        region=os.getenv('region'),
        list_users=True,
    )
    cog.handle_cognito()
    captured = capsys.readouterr()
    print(captured)
    assert "['a@b.c', 'd@e.f', 'g@h.i']" in captured.out
