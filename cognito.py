import datetime
import boto3
import pandas as pd
import pytz

REGION = "ap-south-1"
USER_POOL_ID = "ap-south-1_IGJhSmqDG"


class Cognito:
    def __init__(
        self,
        region: str = REGION,
        user_pool_id: str = USER_POOL_ID,
        list_users: bool = False,
        before: str = None,
        after: str = None,
        save: bool = False,
    ):
        self.region = region
        self.user_pool_id = user_pool_id
        self.list_users = list_users
        self.before = self._to_date(before)
        self.after = self._to_date(after)
        self.save = save
        self.LIMIT = 60

        # Create boto3 CognitoIdentityProvider client
        self.client = boto3.client("cognito-idp", self.region)
        self.pagination_token = ""

    def handle_cognito(self):

        if not self.list_users and not self.save:
            raise SystemExit(
                "No action flag provided. Please provide either -l or -s"
            )
        else:
            print(" Fetching Users ".center(80, "*"))
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
        print(" Saving Users ".center(80, "*"))
        self.to_csv()
        print(f" Finish ".center(80, "*"))

    def modify_df(self):
        df = pd.DataFrame(self.user_list)
        df["Email"] = list(map(self._get_email, df.Attributes))
        df["UserCreateDate"] = df["UserCreateDate"].dt.date

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
            datetime.datetime.strptime(str_date, "%Y-%m-%d").date()
            if str_date is not None
            else None
        )

    # Define function that utilize ListUsers AWS API call
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
            self.user_list = self.user_list + user_records["Users"]
            if "PaginationToken" in user_records.keys():
                self.pagination_token = user_records["PaginationToken"]
            else:
                break

        # return self.user_list

    def _get_email(self, row: list):
        for data in row:
            if data["Name"] == "email":
                return data["Value"]
            else:
                continue

    def print_users(self):
        print(self.df.to_string())

        print(f" Total Users: {self.df.shape[0]} ".center(80, "*"))
        print(f" Finish ".center(80, "*"))

    def to_csv(self):
        if self.before is not None or self.after is not None:
            self.df.to_csv(
                "./user_subset.csv", index=False, columns=self.df.columns
            )
        else:
            self.df.to_csv(
                "./all_users.csv", index=False, columns=self.df.columns
            )
