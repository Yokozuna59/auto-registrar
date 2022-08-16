from pathlib import Path
from os import path, system
from json import dumps, loads
from sys import platform

from cryptography.fernet import Fernet, InvalidToken

from auto_registrar.tui.questions import Questions
from auto_registrar.tui.colored_text import print_one_color_text
from auto_registrar.tui.ansi import AnsiColor
from auto_registrar.universities.kfupm import KFUPM

PROJECT_PATH = Path(__file__).parent.parent
CONFIGS_PATH = PROJECT_PATH.joinpath(".config.json")
DRIVERS_PATH = PROJECT_PATH.joinpath("drivers")
KEY_PATH = PROJECT_PATH.joinpath(".key")


def get_configs(ask_for_config: bool) -> dict:
    """
    Checks if user configured his default configuration.\n
    return configs as `dict` type.
    """

    if not path.exists(path=CONFIGS_PATH):
        university = Questions.list_question(
            question="What university you're in", choices=["KFUPM"]
        )
        if university == "KFUPM":
            json_objects = {
                "configured": False,
                "alarm": "alarms/default-alarm.mp3",
                "banner": 9,
                "browser": "chrome",
                "delay": 60,
                "interface": "cli",
                "passcode": None,
                "university": "kfupm",
                "username": None,
            }
        write_config_file(configs_file=json_objects)

    with open(file=CONFIGS_PATH, mode="r") as file:
        configs = loads(s=file.read())

    if not configs["configured"]:
        bool_answer = True
        if ask_for_config:
            print_one_color_text(
                text_string="! Sorry, you haven't configured yet!",
                text_color=AnsiColor.LIGHT_RED,
            )
            bool_answer = Questions.bool_question(
                question="Do you want to configurate now"
            )

        if bool_answer:
            if configs["university"]:
                configs = KFUPM.ask_for_configs(config_file=configs)
    else:
        configs["passcode"] = decode_passcode(
            passcode=configs["passcode"], configs_file=configs
        )

    if path.exists(path=DRIVERS_PATH):
        # TODO: check if drivers are installed
        configs["driver_path"] = DRIVERS_PATH.joinpath(configs['browser'])
    else:
        print_one_color_text(
            text_string="! Sorry, you don't have drivers folder yet, which means the script can't open any WebDrivers to registrar courses!",
            text_color=AnsiColor.LIGHT_RED,
        )
        print_one_color_text(
            text_string="Run `install.sh` or `install.ps1` file, please read the `README.md` file for more information.",
            text_color=AnsiColor.LIGHT_YELLOW,
        )
        configs["driver_path"] = None
    return configs


def ask_for_passcode(configs_file: dict) -> dict:
    """
    Ask user to enter the passcode,\n
    Return the passcode as `str` type.
    """

    passcode = Questions.passcode_question(question="Enter your portal passcode")

    key = Fernet.generate_key()
    with open(file=KEY_PATH, mode="w") as fernet:
        fernet.write(
            "-----BEGIN PRIVATE KEY-----\n"
            + key.decode()
            + "\n-----END PRIVATE KEY-----\n"
        )
    if (platform == "win32") or (platform == "cygwin"):
        system("attrib +h " + fernet.name)
    fernet = Fernet(key=key)
    passcode_encrypted = fernet.encrypt(data=passcode.encode()).decode()
    configs_file["passcode"] = passcode_encrypted
    write_config_file(configs_file=configs_file)

    return passcode


def decode_passcode(passcode: str, configs_file: dict) -> str:
    """
    Decrypts the passcode with Fernet,\n
    Return the decrypted passcode as `str` type.
    """

    if not path.exists(path=KEY_PATH):
        print_one_color_text(
            text_string="! Sorry, you have deleted your key file, which means the script can't decrypt your passcode!",
            text_color=AnsiColor.LIGHT_RED,
        )
        print_one_color_text(
            text_string="Please reenter your passcode again.",
            text_color=AnsiColor.LIGHT_YELLOW,
        )

        passcode = ask_for_passcode(configs_file=configs_file)
        configs_file["passcode"] = passcode

    with open(file=KEY_PATH, mode="r") as fernet:
        key = fernet.readlines()[1]
    fernet = Fernet(key=key)
    try:
        passcode_decrypted = fernet.decrypt(token=passcode.encode()).decode()
    except InvalidToken:
        print_one_color_text(
            text_string="! Sorry, you have edited your key file, which means the script can't decrypt your passcode!",
            text_color=AnsiColor.LIGHT_RED,
        )
        print_one_color_text(
            text_string="Please reenter your passcode again.",
            text_color=AnsiColor.LIGHT_YELLOW,
        )
        passcode_decrypted = ask_for_passcode(configs_file=configs_file)
    return passcode_decrypted


def write_config_file(configs_file: dict) -> None:
    """
    Write config file as `json` type.
    Returns `None` type.
    """

    json_objects = dumps(obj=configs_file, sort_keys=True, indent=4)
    with open(file=CONFIGS_PATH, mode="w") as file:
        file.write(json_objects)
    if (platform == "win32") or (platform == "cygwin"):
        system("attrib +h " + file.name)
    return
