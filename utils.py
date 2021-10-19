import json

from PyInquirer import prompt


def configure_aws_helper() -> None:

    questions = [
        {
            "type": "input",
            "name": "access_key",
            "message": "AWS Access Key ID [None]",
        },
        {
            "type": "input",
            "name": "secret_key",
            "message": "AWS Secret Access Key [None]",
        },
        {
            "type": "input",
            "name": "region",
            "message": "Default region name [None]",
        },
        {
            "type": "input",
            "name": "output_fmt",
            "message": "Default output format [None]",
        },
    ]
    answers = prompt(questions, keyboard_interrupt_msg="Aborted!")
    for key, value in answers.items():
        if len(value) == 0:
            answers[key] = None
    with open("./.aws_helper/credentials.json", "w+") as f:
        json.dump(answers, f)
