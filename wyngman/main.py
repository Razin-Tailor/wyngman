import os
import sys
from os.path import expanduser
from typing import Optional
from typing import Sequence

from pyfiglet import Figlet

from wyngman.aws_arg_parser import Parser
from wyngman.cognito import Cognito
from wyngman.utils import configure_wyngman
from wyngman.utils import is_configured

F = Figlet(font='slant')


def main(argv: Optional[Sequence[str]] = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    parser = Parser()
    arg_parser = parser.get_parser()

    # print("Argv:: ", argv)
    if len(argv) == 0:
        # raise SystemExit(-1)
        arg_parser.print_help()
    args = arg_parser.parse_args(argv)

    if args.command == 'configure':
        print(F.renderText('WYNGMAN'))
        home = expanduser('~')

        helper_path = os.path.join(home, '.wyngman')
        if not os.path.isdir(helper_path):
            try:
                os.mkdir(helper_path)
            except Exception as e:
                raise (e)
        try:
            configure_wyngman()
        except Exception as e:
            raise SystemExit(e)
    elif args.command == 'cognito':
        print(F.renderText('WYNGMAN'))
        if not is_configured():
            raise SystemExit(
                (
                    'You need to configure the tool.'
                    'Please run `wyngman configure`',
                ),
            )
        else:
            list_user_pools = args.list_user_pools
            region = args.region
            user_pool_id = args.user_pool_id
            list_users = args.list_users
            before = args.before
            after = args.after
            save = args.save
            count_users = args.count_users
            cognito = Cognito(
                list_user_pools=list_user_pools,
                region=region,
                user_pool_id=user_pool_id,
                list_users=list_users,
                before=before,
                after=after,
                save=save,
                count_users=count_users,
            )
            if list_user_pools:
                cognito.get_list_user_pools()
            cognito.handle_cognito()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
