import datetime
import sys
import boto3
import pandas as pd
import pytz

import parser

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


def main() -> int:
    arg_parser = parser.get_parser() 
    opt = arg_parser.parse_args()
    if len(sys.argv) < 2:
        parser.print_help()
        return 1
    else:
        pass
    return 0


if __name__ == "__main__":
    exit(main())
