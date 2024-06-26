"""
Test no argument passed
1. -- Test total users
2. -- Test list all users
3. -- Test before date
4. -- Test after date
5. Test before and after
6. Test show and save for all users and 3,4,5
9. -- catch no user pool id provided for cognito class
10. -- check user-pool doesnot exist
"""
import os
import sys

import boto3
import pytest
from dotenv import load_dotenv

from tests.utils.configure import configure_wyngman_for_test
from wyngman.cognito import Cognito
from wyngman.main import main

from wyngman.utils import is_configured


load_dotenv()

CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.wyngman')
CREDENTIALS_PATH = os.path.join(
    os.path.expanduser(
        '~',
    ), '.wyngman', 'credentials.json',
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
        'access_key': os.getenv('test-access-key'),
        'secret_key': os.getenv('test-secret'),
        'region': os.getenv('region'),
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

    configure_wyngman_for_test(configure)

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
        configure_wyngman_for_test(configure)
        cog = Cognito(
            user_pool_id='somerandomstring',
            region=os.getenv('region'),
            count_users=True,
        )
        cog.handle_cognito()


def test_list_all_users(setup_users, capsys):
    """Tests the list_users functionality"""

    cog = Cognito(
        user_pool_id=os.getenv('user-pool-id'),
        region=os.getenv('region'),
        list_users=True,
    )
    cog.handle_cognito()
    captured = capsys.readouterr()
    print(captured)
    assert "['a@b.c', 'd@e.f', 'g@h.i']" in captured.out


def test_save_all_users(setup_users):
    """Tests save all users"""
    cog = Cognito(
        user_pool_id=os.getenv('user-pool-id'),
        region=os.getenv('region'),
        save=True,
    )

    cog.handle_cognito()

    assert os.path.isfile('./all_users.csv') == True
    os.remove('./all_users.csv')


def test_list_all_users_and_save(setup_users, capsys):
    """Tests list all users and also save them as a csv"""

    cog = Cognito(
        user_pool_id=os.getenv('user-pool-id'),
        region=os.getenv('region'),
        save=True,
        list_users=True,
    )

    cog.handle_cognito()

    captured = capsys.readouterr()
    assert "['a@b.c', 'd@e.f', 'g@h.i']" in captured.out
    assert os.path.isfile('./all_users.csv') == True
    os.remove('./all_users.csv')


def get_date_to_test_after() -> str:

    from datetime import datetime
    now = datetime.now()

    day = int(now.strftime('%d'))
    month = now.strftime('%m')
    year = now.strftime('%Y')
    day_to_test = day - 1

    # Date is in the format yyyy-mm-dd

    date_string = year + '-' + month + '-' + str(day_to_test)
    return date_string


def get_date_to_test_before() -> str:

    from datetime import datetime
    now = datetime.now()

    day = int(now.strftime('%d'))
    month = now.strftime('%m')
    year = now.strftime('%Y')
    day_to_test = day + 1

    # Date is in the format yyyy-mm-dd

    date_string = year + '-' + month + '-' + str(day_to_test)
    return date_string


def test_list_users_after_date(setup_users, capsys):
    """Tests list users before current date so the fixture works"""
    date_string = get_date_to_test_after()

    cog = Cognito(
        user_pool_id=os.getenv('user-pool-id'),
        region=os.getenv('region'),
        list_users=True,
        before=date_string,
    )
    cog.handle_cognito()
    captured = capsys.readouterr()
    print(captured)
    assert "['a@b.c', 'd@e.f', 'g@h.i']" in captured.out


def test_list_users_before_date(setup_users, capsys):
    """Tests list users before current date so the fixture works"""
    date_string = get_date_to_test_before()

    cog = Cognito(
        user_pool_id=os.getenv('user-pool-id'),
        region=os.getenv('region'),
        list_users=True,
        before=date_string,
    )
    cog.handle_cognito()
    captured = capsys.readouterr()
    print(captured)
    assert "['a@b.c', 'd@e.f', 'g@h.i']" in captured.out


def test_cognito_valid_parameter(configure):
    """Test SystemExit on violation of valid params"""

    configure_wyngman_for_test(configure)

    with pytest.raises(SystemExit):
        cog = Cognito(
            user_pool_id=None,
            region=os.getenv('region'),
            list_user_pools=False,
        )
        cog.handle_cognito()


def test_list_user_pools(configure, capsys):
    """Test user pools"""

    configure_wyngman_for_test(configure)

    cog = Cognito(
        user_pool_id=None,
        region=os.getenv('region'),
        list_user_pools=True,
    )

    cog.get_list_user_pools()
    captured = capsys.readouterr()
    print(captured)
    assert 'test' in captured.out


def test_no_action_flag_provided():
    with pytest.raises(SystemExit):

        cog = Cognito(
            user_pool_id=None,
            region=os.getenv('region'),
            list_user_pools=False,
            list_users=False,
            count_users=False,
            save=False,
        )
        cog.handle_cognito()
