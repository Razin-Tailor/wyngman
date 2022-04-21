[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit) ![coverage](https://img.shields.io/badge/coverage-81%25-green)

# AWS Helper

Use `aws-helper configure` to configure the tool

# Currently Supporting

## AWS Cognito

A Querying support for AWS Cognito

- Support to Query **ALL** users instead of the standard limit of _60_
- Support to Query Users **Before** a certain UserCreationDate
- Support to Query Users **After** a certain UserCreationDate
- Support to **Save as CSV**

# Installation

`pip install aws-helper`

# Usage

```console
foo@bar:~$ aws-helper cognito --help

usage: aws-helper cognito [-h] [--user-pool-id USER_POOL_ID] [--region REGION] [--list-user-pools] [--list-users | --count] [--before BEFORE] [--after AFTER] [--save]

optional arguments:
  -h, --help            show this help message and exit
  --user-pool-id USER_POOL_ID, -p USER_POOL_ID
                        Provide User Pool ID to Fetch Users
  --region REGION, -r REGION
                        Provide AWS Region [Default: Configuration Region]
  --list-user-pools, -lu
                        List All User Pools in a given region
  --list-users, -l      list all users in aws cognito
  --count, -c           Return Count of users
  --before BEFORE, -b BEFORE
                        All users before date Date in format yyyy-mm-dd
  --after AFTER, -a AFTER
                        All users after date Date in format yyyy-mm-dd
  --save, -s            Save as a CSV file
```
