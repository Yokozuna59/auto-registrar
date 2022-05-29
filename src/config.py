from os import path, listdir
from json import loads, dump
from cli import colorful_text, AnsiEscapeCodes, Questions

def check_configurations() -> dict:
    """
    Checks if user has installed and configured his default configuration.\n
    If he did, return it as `dict` type.
    """

    PROJECT_PATH =  __file__.replace("src/config.py", "").replace("src\config.py", "")
    CONFIG_PATH = f"{PROJECT_PATH}.config.json"
    DRIVERS_PATH = f"{PROJECT_PATH}/drivers" if "/" in PROJECT_PATH else f"{PROJECT_PATH}\drivers"

    if (not path.exists(CONFIG_PATH)):
        # print error messege and stop the script
        with open(CONFIG_PATH, 'w') as f:
            f.write('{"configuration": null, "alarm": "alarms/default-alarm.mp3", "banner": 9, "browser": "chrome", "delay": 60, "interface": "cli", "passcode": null, "username": null}')

    # open config file
    with open(CONFIG_PATH, 'r') as f:
        # read and loads config file
        config_file = loads(f.read())
        browser = config_file["browser"]

    if (not path.exists(DRIVERS_PATH)):
        colorful_text(text_string="! Sorry, you haven't ran `install.sh` or `install.ps1` files, or you haven't installed the drivers yet, or haven't created the driver folder!", text_color=AnsiEscapeCodes.RED)
        colorful_text(text_string="! Since you don't have drivers, you won't be able to registrar for courses.", text_color=AnsiEscapeCodes.YELLOW)
        config_file['browser'] = None
    else:
        # FIXME fix the drivers
        DRIVERS = sorted(list(listdir(DRIVERS_PATH)))

    # check if user has configured yet or not
    if (config_file['configuration'] == None):
        # print error messege
        colorful_text(text_string="! Sorry, you haven't configured yet.", text_color=AnsiEscapeCodes.RED)

        # Ask user if he wants to config now or not
        bool_answer = Questions.bool_question(question="Do you want to configurate now")

        # if True ask 5 question and config the file
        if (bool_answer == True):
            config_file = configuring(file_path=CONFIG_PATH, config_file=config_file)
    if (config_file['browser'] != None):
        config_file['browser'] = "{}{}{}".format(DRIVERS_PATH, "/" if "/" in DRIVERS_PATH else "\\", DRIVERS[0] if browser == "chrome" else DRIVERS[1])
    return config_file

def configuring(file_path: str, config_file: str) -> dict:
    """
    Ask user 5 diffrent questinos to do configuration.\n
    If he answered them, return them as `dict` type.
    """

    with open(file_path, 'r') as f:
        config_file = loads(f.read())

    default_banner = Questions.dict_question(question="Select default banner for registration", choices={"Banner 8":8, "Banner 9":9})
    config_file["banner"] = default_banner

    default_browser = Questions.dict_question(question="Select default browser", choices={"Chrome":"chrome", "Firefox":"firefox"})
    config_file["browser"] = default_browser

    default_delay = Questions.dict_question(question="Select default time delay between refreshes", choices={"10 second":10, "20 Second":20, "30 Second":30, "60 Second":60})
    config_file["delay"] = default_delay

    default_interface = Questions.dict_question(question="Select default user interface", choices={"Command-line interface (CLI)":"cli", "Graphical user interface (GUI)":"gui"})
    config_file["interface"] = default_interface

    username = Questions.str_questoin(question="Enter your student ID with `S`")
    config_file["username"] = username

    passcode = Questions.passcode_question(question="Enter your portal passcode")
    config_file["passcode"] = passcode

    config_file["configuration"] = "configured"

    with open(file_path, "w") as f:
        dump(config_file, f)

    return config_file