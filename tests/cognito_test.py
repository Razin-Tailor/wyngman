"""
Test no argument passed
1. Test credential file existence
2. Test correctness of credential file
3. Test Correct initialization of Cognito Class
4. Test list all users
5. Test before date
6. Test after date
7. Test before and after
8. Test show and save for 4, 5, 6, 7
9. catch no user id provided for cognito class
10. check user-pool doesnot exist
"""
import os
import sys
from turtle import clear

import boto3
import pytest
from dotenv import load_dotenv

from ..utils import configure_aws_helper
from .data.user_data import UserData
from cognito import Cognito
from main import main
# from .fixtures.fixture_user import setup_users

sys.path.insert(0, '../')
sys.path.insert(0, '.')


load_dotenv()


@pytest.fixture(scope='module')
def setup_users():
    print(f"{os.getenv('region')}, {os.getenv('test-access-key')}, {os.getenv('test-secret')}")

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


"""
def test_total_users(capsys):
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

    assert captured.out == 'Hello'
"""
