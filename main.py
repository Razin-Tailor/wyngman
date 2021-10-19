from typing import Optional, Sequence

import datetime
import os
import sys
from parser import Parser

import boto3
import pandas as pd
from pyfiglet import Figlet

from cognito import Cognito
from utils import configure_aws_helper

F = Figlet(font="slant")

# Amazon Cognito User Pool Configs
LIMIT = 60
REGION = "ap-south-1"
USER_POOL_ID = "ap-south-1_IGJhSmqDG"

# Create boto3 CognitoIdentityProvider client
client = boto3.client("cognito-idp", REGION)
pagination_token = ""


# Define function that utilize ListUsers AWS API call
def get_list_cognito_users(
    cognito_idp_client, next_pagination_token="", Limit=LIMIT
):

    return (
        cognito_idp_client.list_users(
            UserPoolId=USER_POOL_ID,
            # AttributesToGet = ['name'],
            Limit=Limit,
            PaginationToken=next_pagination_token,
        )
        if next_pagination_token
        else cognito_idp_client.list_users(
            UserPoolId=USER_POOL_ID,
            # AttributesToGet = ['name'],
            Limit=Limit,
        )
    )


# Pull Batch of Amazon Cognito User Pool records
# user_list = []
# while True:
#     user_records = get_list_cognito_users(
#         cognito_idp_client=client,
#         next_pagination_token=pagination_token,
#         Limit=LIMIT,
#     )
#     user_list = user_list + user_records["Users"]
#     if "PaginationToken" in user_records.keys():
#         pagination_token = user_records["PaginationToken"]
#     else:
#         break


def datetimeconverter(o):
    if isinstance(o, datetime.datetime):
        return str(o)


def get_email(row):
    for data in row:
        if data["Name"] == "email":
            return data["Value"]
        else:
            continue


# df = pd.DataFrame(user_list)
# print(df.head())
# df["Email"] = list(map(get_email, df.Attributes))
# sub_df = df[
#     df.UserCreateDate >= datetime.datetime(2021, 9, 19, 0, 0, 0, 0, pytz.UTC)
# ]
# print(sub_df["Email"])


def main(argv: Optional[Sequence[str]] = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    # Check if configuration is set
    # if yes use it
    # else prompt to set
    # if not os.path.isdir("./.aws_helper"):
    #     print(
    #         "No Configuration File found. Please run aws-helper configure..."
    #     )
    #     raise SystemExit(-1)
    # os.mkdir("./.aws_helper")
    # configure_aws_helper()

    parser = Parser()
    arg_parser = parser.get_parser()
    print(F.renderText("AWS HELPER"))

    print("Argv:: ", argv)
    if len(argv) == 0:
        arg_parser.print_help()
        # argv = ["--help"]
    args = arg_parser.parse_args(argv)
    print("Args:: ", args.command)
    if args.command == "configure":
        if not os.path.isdir("./.aws_helper"):
            os.mkdir("./.aws_helper")
        configure_aws_helper()
    elif args.command == "cognito":
        list_user_pools = args.list_user_pools
        region = args.region
        user_pool_id = args.user_pool_id
        list_users = args.list_users
        before = args.before
        after = args.after
        save = args.save

        cognito = Cognito(
            list_user_pools=list_user_pools,
            region=region,
            user_pool_id=user_pool_id,
            list_users=list_users,
            before=before,
            after=after,
            save=save,
        )
        if list_user_pools:
            cognito.get_list_user_pools()
        cognito.handle_cognito()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
