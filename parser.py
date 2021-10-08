import argparse
import textwrap
import constants as C


class Parser:
    COGNITO_HELP = """\
        AWS Cognito Utilities
        use `aws-helper cognito -h` for more information
        """

    def __init__(self):
        pass

    def get_parser(self) -> argparse.ArgumentParser:
        """This function returns a parser object that will serve as entry point to the Plugin
        Return: argumentParser
        """

        description = textwrap.dedent(
            """\
            This is helper function to support AWS Utilities that are not directly supported by AWS
            Make Sure you have aws-cli setup locally so that the cliendID and client-secret can be accessed by the tool
            """
        )
        parser = argparse.ArgumentParser(
            description=description,
            formatter_class=argparse.RawTextHelpFormatter,
        )
        # https://stackoverflow.com/a/8521644/812183
        parser.add_argument(
            "-V",
            "--version",
            action="version",
            version=f"%(prog)s {C.VERSION}",
        )
        subparsers = parser.add_subparsers(dest="command")

        cognito_parser = subparsers.add_parser(
            "cognito",
            help=self.COGNITO_HELP,
            formatter_class=argparse.RawTextHelpFormatter,
        )
        cognito_parser.add_argument(
            "--list-users",
            "-l",
            dest="list_users",
            action="store_true",
            help="list all users in aws cognito",
        )
        cognito_parser.add_argument(
            "--before",
            "-b",
            type=str,
            default=None,
            help="All users before date Date in format yyyy-mm-dd",
        )
        cognito_parser.add_argument(
            "--after",
            "-a",
            type=str,
            default=None,
            help="All users after date Date in format yyyy-mm-dd",
        )

        cognito_parser.add_argument(
            "--save",
            "-s",
            dest="save",
            action="store_true",
            help="Save as a CSV file",
        )
        return parser
