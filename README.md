# AWS Helper

A tool to enhance the AWS utilities. It is dependent on _boto3_ which utilizes `.aws/credentials`. Please have it setup.

One way is to setup _aws-cli_

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
usage: main.py cognito [-h] [--list-users] [--before BEFORE] [--after AFTER] [--save]

optional arguments:
  -h, --help            show this help message and exit
  --list-users, -l      list all users in aws cognito
  --before BEFORE, -b BEFORE
                        all users before date Date in format yyyy-mm-dd
  --after AFTER, -a AFTER
                        all users after date Date in format yyyy-mm-dd
  --save, -s            Save as a CSV file
```
