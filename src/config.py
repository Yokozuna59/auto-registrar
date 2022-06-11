from os import path
from json import loads, dumps
from cli import colorful_text, AnsiEscapeCodes, Questions

def check_configurations() -> dict:
    """
    Checks if user has installed and configured his default configuration.\n
    If he did, return it as `dict` type.
    """

    SLASH_PATH = "/" if "/" in __file__ else "\\"
    PROJECT_PATH =  __file__.replace(f"src{SLASH_PATH}config.py", "")
    CONFIGS_PATH = f"{PROJECT_PATH}.config.json"
    DRIVERS_PATH = f"{PROJECT_PATH}{SLASH_PATH}drivers"

    if (not path.exists(CONFIGS_PATH)):
        defualt_config = {"configuration": None, "alarm": "alarms/default-alarm.mp3", "banner": 9, "browser": "chrome", "delay": 60, "interface": "cli", "passcode": None, "username": None}
        json_object = dumps(defualt_config, indent=4)
        with open(CONFIGS_PATH, 'w') as file:
            file.write(json_object)

    # open config file
    with open(CONFIGS_PATH, 'r') as file:
        config_file = loads(file.read())
        browser = config_file["browser"]

    if (not (path.exists(DRIVERS_PATH))):
        colorful_text(text_string="! Sorry, you haven't ran `install.sh` or `install.ps1` files, or you haven't installed the drivers yet, or haven't created the driver folder!", text_color=AnsiEscapeCodes.RED)
        colorful_text(text_string="! Since you don't have drivers, you won't be able to registrar for courses.", text_color=AnsiEscapeCodes.YELLOW)
        config_file['browser'] = None

    # check if user has configured yet or not
    if (config_file['configuration'] == None):
        # print error messege
        colorful_text(text_string="! Sorry, you haven't configured yet.", text_color=AnsiEscapeCodes.RED)

        # Ask user if he wants to config now or not
        bool_answer = Questions.bool_question(question="Do you want to configurate now")

        # if True ask 5 question and config the file
        if (bool_answer == True):
            config_file = configuring(file_path=CONFIGS_PATH, config_file=config_file)
    if (config_file['browser'] != None):
        config_file['browser'] = "{}{}{}".format(DRIVERS_PATH, SLASH_PATH, "chromedriver" if browser == "chrome" else "geckodriver")
    return config_file

def configuring(file_path: str, config_file: str) -> dict:
    """
    Ask user 5 diffrent questinos to do configuration.\n
    If he answered them, return them as `dict` type.
    """

    with open(file_path, 'r') as file:
        config_file = loads(file.read())

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

    with open(file_path, "w") as file:
        dumps(config_file, file)

    return config_file