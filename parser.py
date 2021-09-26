import argparse
import textwrap

def get_parser()-> argparse.ArgumentParser:
    description = textwrap.dedent(
        """\
        This is helper function to support AWS Utilities that are not directly supported by AWS
        Make Sure you have aws-cli setup locally so that the cliendID and client-secret can be accessed by the tool
        """
    )
    parser = argparse.ArgumentParser(
        description=description,
        usage="use `aws-helper {service} -h` for more information",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers()
    parser.add_argument(
        "service",
        metavar="service",
        type=str,
        help="AWS Service [currently only supporting Cognito]",
    )

    cognito_parser = subparsers.add_parser("cognito")
    cognito_parser.add_argument(
        "--list-users", "-l", type=bool, default=False, help="List Users Flag"
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
        "--all", "-A", type=str, default=None, help="Fetch All Users Flag"
    )
    cognito_parser.add_argument(
        "--save", "-s", type=str, default=None, help="Save as a CSV file"
    )
    return parser