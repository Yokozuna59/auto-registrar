# import functions from modules
from os import path, system
from json import dumps, loads
from sys import platform
from cryptography.fernet import Fernet, InvalidToken

# import functions from local files
from cli import print_colorful_text, Questions, AnsiEscapeCodes

SLASH_PATH = "/" if "/" in __file__ else "\\"
PROJECT_PATH = SLASH_PATH.join(__file__.split(SLASH_PATH)[:-2])
CONFIGS_PATH = f"{PROJECT_PATH}{SLASH_PATH}.config.json"
DRIVERS_PATH = f"{PROJECT_PATH}{SLASH_PATH}drivers"


def get_configs() -> dict:
    """
    Checks if user has installed and configured his default configuration.\n
    If he did, return configs as `dict` type.
    """

    if not path.exists(path=CONFIGS_PATH):
        json_objects = {
            "configuration": None,
            "alarm": "alarms/default-alarm.mp3",
            "banner": 9,
            "browser": "chrome",
            "delay": 60,
            "interface": "cli",
            "passcode": None,
            "username": None,
            "version": "0.5.0",
        }
        write_configs_file(configs_file=json_objects)

    with open(file=CONFIGS_PATH, mode="r") as f:
        configs = loads(s=f.read())

    if configs["configuration"] == None:
        print_colorful_text(
            text_string="! Sorry, you haven't configured yet!",
            text_color=AnsiEscapeCodes.LIGHT_RED,
        )
        bool_answer = Questions.bool_question(question="Do you want to configurate now")

        if bool_answer:
            configs = do_configs(configs_file=configs)
    else:
        configs["passcode"] = decode_passcode(
            passcode=configs["passcode"], configs_file=configs
        )

    if path.exists(path=DRIVERS_PATH):
        # TODO: check if drivers are installed
        configs["browser"] = f"{DRIVERS_PATH}{SLASH_PATH}{configs['browser']}"
    else:
        print_colorful_text(
            text_string="! Sorry, you don't have drivers folder yet, which means the script can't open any WebDrivers to registrar courses!",
            text_color=AnsiEscapeCodes.LIGHT_RED,
        )
        print_colorful_text(
            text_string="Run `install.sh` or `install.ps1` file, please read the `README.md` file for more information.",
            text_color=AnsiEscapeCodes.LIGHT_YELLOW,
        )
        configs["browser"] = None
    return configs


def do_configs(configs_file: dict) -> dict:
    """
    Ask user 5 diffrent questinos to configurate.\n
    If he answered the question, return them as `dict` type.
    """

    default_banner = Questions.dict_question(
        question="Select default banner for registration",
        choices={"Banner 8": 8, "Banner 9": 9},
    )
    configs_file["banner"] = default_banner

    default_browser = Questions.dict_question(
        question="Select default browser",
        choices={"Chrome": "chromedriver", "Firefox": "geckodriver"},
    )
    configs_file["browser"] = default_browser

    default_delay = Questions.dict_question(
        question="Select default time delay between refreshes",
        choices={"10 second": 10, "20 Second": 20, "30 Second": 30, "60 Second": 60},
    )
    configs_file["delay"] = default_delay

    default_interface = Questions.dict_question(
        question="Select default user interface",
        choices={
            "Command-line interface (CLI)": "cli",
            "Graphical user interface (GUI)": "gui",
        },
    )
    configs_file["interface"] = default_interface

    username = Questions.str_questoin(question="Enter your student ID with `S`")
    configs_file["username"] = username

    passcode = ask_for_passcode(configs_file=configs_file)

    configs_file["configuration"] = "configured"
    write_configs_file(configs_file=configs_file)

    configs_file["passcode"] = passcode

    return configs_file


def ask_for_passcode(configs_file: dict) -> dict:
    """
    Ask user to enter the passcode,\n
    Return the passcode as `str` type.
    """

    passcode = Questions.passcode_question(question="Enter your portal passcode")

    key = Fernet.generate_key()
    with open(file=f"{PROJECT_PATH}{SLASH_PATH}.key", mode="wb") as fernet:
        fernet.write(key)
    if (platform == "win32") or (platform == "cygwin"):
        system("attrib +h " + fernet.name)
    fernet = Fernet(key=key)
    passcode_encrypted = fernet.encrypt(data=passcode.encode()).decode()
    configs_file["passcode"] = passcode_encrypted
    write_configs_file(configs_file=configs_file)

    return passcode


def decode_passcode(passcode: str, configs_file: dict) -> str:
    """
    Decrypts the passcode with Fernet,\n
    Return the decrypted passcode as `str` type.
    """

    if not path.exists(path=f"{PROJECT_PATH}{SLASH_PATH}.key"):
        print_colorful_text(
            text_string="! Sorry, you have deleted your key file, which means the script can't decrypt your passcode!",
            text_color=AnsiEscapeCodes.LIGHT_RED,
        )
        print_colorful_text(
            text_string="Please reenter your passcode again.",
            text_color=AnsiEscapeCodes.LIGHT_YELLOW,
        )

        passcode = ask_for_passcode(configs_file=configs_file)
        configs_file["passcode"] = passcode

    with open(file=f"{PROJECT_PATH}{SLASH_PATH}.key", mode="rb") as fernet:
        key = fernet.read()
    fernet = Fernet(key=key)
    try:
        passcode_decrypted = fernet.decrypt(token=passcode.encode()).decode()
    except InvalidToken:
        print_colorful_text(
            text_string="! Sorry, you have edited your key file, which means the script can't decrypt your passcode!",
            text_color=AnsiEscapeCodes.LIGHT_RED,
        )
        print_colorful_text(
            text_string="Please reenter your passcode again.",
            text_color=AnsiEscapeCodes.LIGHT_YELLOW,
        )
        passcode_decrypted = ask_for_passcode(configs_file=configs_file)
    return passcode_decrypted


def write_configs_file(configs_file: dict) -> None:
    """
    Write the configs file as `json` type.
    Returns `None` type.
    """

    json_objects = dumps(obj=configs_file, sort_keys=True, indent=4)
    with open(file=CONFIGS_PATH, mode="w") as f:
        f.write(json_objects)
    if (platform == "win32") or (platform == "cygwin"):
        system("attrib +h " + f.name)
    return None
