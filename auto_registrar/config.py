from json import dumps, loads
from os import path, system
from pathlib import Path
from sys import platform

from cryptography.fernet import Fernet, InvalidToken

from auto_registrar.tui.ansi import AnsiColor
from auto_registrar.tui.colored_text import print_one_color_text
from auto_registrar.tui.questions import Questions
from auto_registrar.universities.kfupm.kfupm import KFUPM

PROJECT_PATH: Path = Path(__file__).parent.parent
CONFIGS_PATH: Path = PROJECT_PATH.joinpath(".config.json")
DRIVERS_PATH: Path = PROJECT_PATH.joinpath("drivers")
KEY_PATH: Path = PROJECT_PATH.joinpath(".key")
SOUNDS_PATH: Path = PROJECT_PATH.joinpath("sounds")


def get_configs() -> dict:
    """Get configurations if user has configured. Else write the default
    configurations and ask to configure.

    Args:
        None

    Returns:
        Configurations as `dict` type.
    """

    if not path.exists(path=CONFIGS_PATH):
        university: str = Questions.list_question(
            question="What university you're in", choices=["KFUPM"]
        )
        if university == "KFUPM":
            default_configs: dict = {
                "configured": False,
                "banner": "banner9",
                "delay": 60,
                "interface": "cli",
                "passcode": None,
                "university": "kfupm",
                "username": None,
            }
            write_configs_file(configs_contents=default_configs)

    with open(file=CONFIGS_PATH, encoding="utf-8") as configs_file:
        configs: dict = loads(configs_file.read())

    if not configs["configured"]:
        print_one_color_text(
            text_string="! Sorry, you haven't configured yet!",
            text_color=AnsiColor.LIGHT_RED,
        )
        boolean_answer: bool = Questions.bool_question(
            question="Do you want to configurate now"
        )

        if boolean_answer:
            if configs["university"]:
                configs: dict = KFUPM.ask_for_configs(config_file=configs)

    return configs


def ask_and_write_passcode(configs: dict, ask_for_passcode: bool) -> str:
    """Ask the user to enter his passcode and write the encrypted one.

    Args:
        configs: This is the current configurations.
        ask_for_passcode: To check if it's needed ask user for passcode.

    Returns:
        Passcode as `str` type.
    """

    if ask_for_passcode:
        passcode: str = Questions.passcode_question(
            question="Enter your portal passcode"
        )
    else:
        passcode: str = configs["passcode"]

    key: bytes = Fernet.generate_key()
    with open(file=KEY_PATH, mode="w", encoding="utf-8") as key_file:
        key_file.write(
            "-----BEGIN PRIVATE KEY-----\n"
            + key.decode()
            + "\n-----END PRIVATE KEY-----\n"
        )
    if platform in ("win32", "cygwin"):
        system("attrib +h " + key_file.name)

    fernet: Fernet = Fernet(key=key)
    passcode_encrypted: str = fernet.encrypt(data=passcode.encode()).decode()
    configs["passcode"] = passcode_encrypted
    write_configs_file(configs_contents=configs)

    return passcode


def decode_passcode(passcode: str, configs_contents: dict) -> str:
    """Decrypts the passcode with Fernet.

    Args:
        passcode: The user's passcode.
        configs_contents: The current user configuration.

    Returns:
        The decrypted passcode as `str` type.
    """

    if not path.exists(path=KEY_PATH):
        print_one_color_text(
            text_string="! Sorry, you have deleted your key file, "
            + "which means the script can't decrypt your passcode!",
            text_color=AnsiColor.LIGHT_RED,
        )
        print_one_color_text(
            text_string="Please reenter your passcode again.",
            text_color=AnsiColor.LIGHT_YELLOW,
        )

        passcode: str = ask_and_write_passcode(
            configs=configs_contents, ask_for_passcode=True
        )
        configs_contents["passcode"] = passcode

    with open(file=KEY_PATH, encoding="utf-8") as key_file:
        key: str = key_file.readlines()[1]

    fernet: Fernet = Fernet(key=key)
    try:
        passcode_decrypted: str = fernet.decrypt(
            token=passcode.encode()
        ).decode()
    except InvalidToken:
        print_one_color_text(
            text_string="! Sorry, you have edited your key file, "
            + "which means the script can't decrypt your passcode!",
            text_color=AnsiColor.LIGHT_RED,
        )
        print_one_color_text(
            text_string="Please re-enter your passcode again.",
            text_color=AnsiColor.LIGHT_YELLOW,
        )
        passcode_decrypted: str = ask_and_write_passcode(
            configs=configs_contents, ask_for_passcode=True
        )

    return passcode_decrypted


def write_configs_file(configs_contents: dict) -> None:
    """Write configurations file with `.json` extension.

    Args:
        configs_contents: The contents of the file will be written.

    Returns:
        None
    """

    json_string: str = dumps(obj=configs_contents, sort_keys=True, indent=4)
    with open(file=CONFIGS_PATH, mode="w", encoding="utf-8") as configs_file:
        configs_file.write(json_string)

    if platform in ("win32", "cygwin"):
        system("attrib +h " + configs_file.name)
