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


def main(argv: Optional[Sequence[str]] = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    parser = Parser()
    arg_parser = parser.get_parser()
    print(F.renderText("AWS HELPER"))

    # print("Argv:: ", argv)
    if len(argv) == 0:
        arg_parser.print_help()
    args = arg_parser.parse_args(argv)

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
