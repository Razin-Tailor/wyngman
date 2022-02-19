import json
import os
from os.path import expanduser

from PyInquirer import prompt


def is_configured() -> bool:
    if not os.path.isdir(os.path.join(os.path.expanduser('~'), '.aws_helper')):
        return False
    else:
        return True


def configure_aws_helper() -> None:

    questions = [
        {
            'type': 'input',
            'name': 'access_key',
            'message': 'AWS Access Key ID [None]',
        },
        {
            'type': 'input',
            'name': 'secret_key',
            'message': 'AWS Secret Access Key [None]',
        },
        {
            'type': 'input',
            'name': 'region',
            'message': 'Default region name [None]',
        },
        {
            'type': 'input',
            'name': 'output_fmt',
            'message': 'Default output format [None]',
        },
    ]

    home = expanduser('~')
    helper_path = os.path.join(home, '.aws_helper')

    answers = prompt(questions, keyboard_interrupt_msg='Aborted!')
    for key, value in answers.items():
        if len(value) == 0:
            answers[key] = None

    if not os.path.isdir(helper_path):
        os.mkdir(helper_path)
    with open(os.path.join(helper_path, 'credentials.json'), 'w+') as f:
        json.dump(answers, f)
