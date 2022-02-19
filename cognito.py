import datetime
import json
import os
import warnings

import boto3
import pandas as pd
import pytz
import tabulate

warnings.filterwarnings('ignore')


REGION = 'ap-south-1'
USER_POOL_ID = 'ap-south-1_IGJhSmqDG'
TO_SHOW_USER_POOL_KEYS = [
    'Id',
    'Name',
    'Status',
    'LastModifiedDate',
    'CreationDate',
]
TO_SHOW_USER_COLUMNS = [
    'Email',
    'UserCreateDate',
    'UserLastModifiedDate',
    'UserStatus',
    'Enabled',
]


class Cognito:
    def __init__(
        self,
        user_pool_id: str,
        region: str = '',
        list_users: bool = False,
        before: str = None,
        after: str = None,
        save: bool = False,
        list_user_pools: bool = False,
    ):
        self.region = region
        self.user_pool_id = user_pool_id
        self.list_user_pools = list_user_pools
        self.list_users = list_users
        self.before = self._to_date(before)
        self.after = self._to_date(after)
        self.save = save
        self.LIMIT = 60
        # Create boto3 CognitoIdentityProvider client
        if not os.path.isfile('./.aws_helper/credentials.json'):
            print(
                'Credentials not Set... Please configure the tool before continuing',
            )
            raise SystemExit(-1)
        else:
            self.credentials = json.load(
                open('./.aws_helper/credentials.json'),
            )
            self.region = (
                self.credentials['region'] if region == '' else region
            )
            self.client = boto3.client(
                'cognito-idp',
                self.region,
                aws_access_key_id=self.credentials['access_key'],
                aws_secret_access_key=self.credentials['secret_key'],
            )

            self.pagination_token = ''
            self.next_token = ''

    def get_list_user_pools(self):
        self.user_pool_list = []
        while True:
            user_records = self.get_user_pools()
            self.user_pool_list = (
                self.user_pool_list + user_records['UserPools']
            )
            if 'NextToken' in user_records.keys():
                self.next_token = user_records['NextToken']
            else:
                break
        concise_list = []
        for item in self.user_pool_list:
            temp_dict = {}
            for key, value in item.items():
                if key in TO_SHOW_USER_POOL_KEYS:
                    temp_dict[key] = value
            concise_list.append(temp_dict)

        header = concise_list[0].keys()
        rows = [x.values() for x in concise_list]
        print(tabulate.tabulate(rows, header, tablefmt='grid'))

    def handle_cognito(self):

        if not self.list_users and not self.save:
            raise SystemExit(
                'No action flag provided. Please use `--help` for more information.',
            )
        else:
            print(' Fetching Users '.center(80, '*'))
            self.list_all_users()
            self.modify_df()
            if self.list_users and self.save:
                self.print_users()
                self.save_data()
            elif self.save:
                self.save_data()
            else:
                self.print_users()

    def save_data(self):
        print(' Saving Users '.center(80, '*'))
        self.to_csv()
        print(f' Finish '.center(80, '*'))

    def modify_df(self):
        df = pd.DataFrame(self.user_list)
        df['Email'] = list(map(self._get_email, df.Attributes))
        df['UserCreateDate'] = df['UserCreateDate'].dt.date

        if self.before is not None and self.after is not None:
            self.df = df[
                (df.UserCreateDate < self.before)
                & (df.UserCreateDate > self.after)
            ]
        elif self.after is not None:
            self.df = df[(df.UserCreateDate > self.after)]
        elif self.before is not None:
            self.df = df[(df.UserCreateDate < self.before)]
        else:
            self.df = df

    def _to_date(self, str_date):
        # y, m, d = str_date.split("-")
        # y = int(y)
        # m = int(m)
        # d = int(d)
        return (
            # datetime.datetime(y, m, d, 0, 0, 0, 0, pytz.UTC)
            datetime.datetime.strptime(str_date, '%Y-%m-%d').date()
            if str_date is not None
            else None
        )

    # Define function that utilize ListUsers AWS API call
    def get_user_pools(self):

        return (
            self.client.list_user_pools(
                # AttributesToGet = ['name'],
                MaxResults=self.LIMIT,
                NextToken=self.pagination_token,
            )
            if self.next_token
            else self.client.list_user_pools(
                # AttributesToGet = ['name'],
                MaxResults=self.LIMIT,
            )
        )

    def get_list_cognito_users(self):

        return (
            self.client.list_users(
                UserPoolId=self.user_pool_id,
                # AttributesToGet = ['name'],
                Limit=self.LIMIT,
                PaginationToken=self.pagination_token,
            )
            if self.pagination_token
            else self.client.list_users(
                UserPoolId=self.user_pool_id,
                # AttributesToGet = ['name'],
                Limit=self.LIMIT,
            )
        )

    def list_all_users(self):
        # Pull Batch of Amazon Cognito User Pool records
        self.user_list = []
        while True:
            user_records = self.get_list_cognito_users()
            self.user_list = self.user_list + user_records['Users']
            if 'PaginationToken' in user_records.keys():
                self.pagination_token = user_records['PaginationToken']
            else:
                break

        # return self.user_list

    def _get_email(self, row: list):
        for data in row:
            if data['Name'] == 'email':
                return data['Value']
            else:
                continue

    def print_users(self):
        to_print = self.df[TO_SHOW_USER_COLUMNS]
        to_print.sort_values(
            by=['UserCreateDate'], ascending=False, inplace=True,
        )
        # print(self.df.to_string())
        header = TO_SHOW_USER_COLUMNS
        rows = to_print.values.tolist()
        print(tabulate.tabulate(rows, header, tablefmt='grid'))
        print(f' Total Users: {self.df.shape[0]} '.center(80, '*'))
        print(f' Finish '.center(80, '*'))

    def to_csv(self):
        if self.before is not None or self.after is not None:
            self.df.to_csv(
                './user_subset.csv', index=False, columns=self.df.columns,
            )
        else:
            self.df.to_csv(
                './all_users.csv', index=False, columns=self.df.columns,
            )
