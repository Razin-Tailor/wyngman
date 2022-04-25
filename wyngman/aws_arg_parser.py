import argparse
import textwrap

import wyngman.constants as C


class Parser:
    COGNITO_HELP = """\
        AWS Cognito Utilities
        use `wyngman cognito -h` for more information
        """
    CONFIGURE_HELP = """\
        Provide your AWS Credentials
        """

    def __init__(self):
        pass

    def get_parser(self) -> argparse.ArgumentParser:
        """
        This function returns a parser object \
            that will serve as entry point to the Plugin

        Return: argumentParser
        """

        description = textwrap.dedent(
            """\
            This is helper function to support AWS Utilities

            Make Sure you have aws-cli setup locally
            The tool uses cliendID and client-secret
            """,
        )
        parser = argparse.ArgumentParser(
            prog='wyngman',
            description=description,
            formatter_class=argparse.RawTextHelpFormatter,
        )
        # https://stackoverflow.com/a/8521644/812183
        parser.add_argument(
            '-V',
            '--version',
            action='version',
            version=f'%(prog)s {C.VERSION}',
        )
        parser.add_argument(
            # "configure",
            # metavar="configure",
            action='store_true',
            dest='configure',
            help='Set your AWS Credentials',
        )
        subparsers = parser.add_subparsers(dest='command')

        cognito_parser = subparsers.add_parser(
            'cognito',
            help=self.COGNITO_HELP,
            formatter_class=argparse.RawTextHelpFormatter,
        )
        _ = subparsers.add_parser(
            'configure',
            help=self.CONFIGURE_HELP,
            formatter_class=argparse.RawTextHelpFormatter,
        )
        cognito_parser.add_argument(
            '--user-pool-id',
            '-p',
            type=str,
            default=None,
            help='Provide User Pool ID to Fetch Users',
        )
        cognito_parser.add_argument(
            '--region',
            '-r',
            type=str,
            default=None,
            help='Provide AWS Region [Default: Configuration Region]',
        )
        cognito_parser.add_argument(
            '--list-user-pools',
            '-lu',
            dest='list_user_pools',
            action='store_true',
            help='List All User Pools in a given region',
        )
        mutex = cognito_parser.add_mutually_exclusive_group()
        mutex.add_argument(
            '--list-users',
            '-l',
            dest='list_users',
            action='store_true',
            help='list all users in aws cognito',
        )
        mutex.add_argument(
            '--count',
            '-c',
            dest='count_users',
            action='store_true',
            help='Return Count of users',
        )
        cognito_parser.add_argument(
            '--before',
            '-b',
            type=str,
            default=None,
            help='All users before date Date in format yyyy-mm-dd',
        )
        cognito_parser.add_argument(
            '--after',
            '-a',
            type=str,
            default=None,
            help='All users after date Date in format yyyy-mm-dd',
        )

        cognito_parser.add_argument(
            '--save',
            '-s',
            dest='save',
            action='store_true',
            help='Save as a CSV file',
        )

        return parser
