import json
import os
from posixpath import expanduser
from typing import Dict


def configure_wyngman_for_test(argv: Dict[str, str]) -> None:
    home = expanduser('~')
    helper_path = os.path.join(home, '.wyngman')
    fpath = os.path.join(helper_path, 'credentials.json')

    # write_perm = os.access(fpath, os.W_OK)  # Check for write access
    write_perm = os.access(helper_path, os.W_OK)  # Check for write access
    if (write_perm):
        if not os.path.isdir(helper_path):
            os.mkdir(helper_path)
        with open(fpath, 'w+') as f:
            json.dump(argv, f)
    else:
        raise PermissionError(
            'Tool doesnot have permission to save credentials. Make sure you have appropriate permissions',
        )
