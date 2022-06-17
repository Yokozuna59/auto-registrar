# import exists to check if file exists
from os.path import exists

# import dumps and loads to dumps and loads the json data
from json import dumps, loads

# import print_colorful_text, Questions, AnsiEscapeCodes to print colorful text and ask user for input
from cli import print_colorful_text, Questions, AnsiEscapeCodes

def check_configs() -> dict:
    """
    Checks if user has installed and configured his default configuration.\n
    If he did, return configs as `dict` type.
    """

    SLASH_PATH = "/" if "/" in __file__ else "\\"
    PROJECT_PATH =  __file__.replace(f"{SLASH_PATH}src{SLASH_PATH}config.py", "")
    CONFIGS_PATH = f"{PROJECT_PATH}{SLASH_PATH}.config.json"
    DRIVERS_PATH = f"{PROJECT_PATH}{SLASH_PATH}drivers"

    if (not (exists(CONFIGS_PATH))):
        defualt_configs = {
            "configuration": None,
            "alarm": "alarms/default-alarm.mp3",
            "banner": 9,
            "browser": "chrome",
            "delay": 60,
            "interface": "cli",
            "passcode": None,
            "username": None
        }
        json_objects = dumps(obj=defualt_configs, indent=4)
        with open(CONFIGS_PATH, 'w') as f:
            f.write(json_objects)

    with open(CONFIGS_PATH, 'r') as f:
        configs = loads(f.read())

    if (configs['configuration'] == None):
        print_colorful_text(text_string="! Sorry, you haven't configured yet!", text_color=AnsiEscapeCodes.LIGHT_RED, end_with="\n")
        bool_answer = Questions.bool_question(question="Do you want to configurate now")

        if (bool_answer):
            configs = do_config(configs_path=CONFIGS_PATH, configs_file=configs)

        if (configs["browser"] != None):
            configs["browser"] = "{}{}{}".format(DRIVERS_PATH, SLASH_PATH, "chromedriver" if configs["browser"] == "chrome" else "geckodriver")

    if (not (exists(DRIVERS_PATH))):
        print_colorful_text(text_string="! Sorry, you don't have drivers folder yet, which means the script can't open any WebDrivers to registrar courses!", text_color=AnsiEscapeCodes.LIGHT_RED, end_with="\n")
        print_colorful_text(text_string="Run `install.sh` or `install.ps1` file, please read the `README.md` file for more information.", text_color=AnsiEscapeCodes.LIGHT_YELLOW, end_with="\n")
        configs["browser"] = None

    return configs

def do_config(configs_path: str, configs_file: str) -> dict:
    """
    Ask user 5 diffrent questinos to configurate.\n
    If he answered the question, return them as `dict` type.
    """

    mcq_choices = {
        "banner": {
            "Banner 8": 8,
            "Banner 9": 9
        },
        "browser": {
            "Chrome": "chrome",
            "Firefox": "firefox"
        },
        "delay": {
            "10 second": 10,
            "20 Second": 20,
            "30 Second": 30,
            "60 Second": 60
        },
        "interface": {
            "Command-line interface (CLI)": "cli",
            "Graphical user interface (GUI)": "gui"
        }
    }
    default_banner = Questions.dict_question(question="Select default banner for registration", choices=mcq_choices["banner"])
    configs_file["banner"] = default_banner

    default_browser = Questions.dict_question(question="Select default browser", choices=mcq_choices["browser"])
    configs_file["browser"] = default_browser

    default_delay = Questions.dict_question(question="Select default time delay between refreshes", choices=mcq_choices["delay"])
    configs_file["delay"] = default_delay

    default_interface = Questions.dict_question(question="Select default user interface", choices=mcq_choices["interface"])
    configs_file["interface"] = default_interface

    username = Questions.str_questoin(question="Enter your student ID with `S`")
    configs_file["username"] = username

    passcode = Questions.passcode_question(question="Enter your portal passcode")
    configs_file["passcode"] = passcode

    configs_file["configuration"] = "configured"

    json_objects = dumps(obj=configs_file, indent=4)
    with open(configs_path, "w") as f:
        f.write(json_objects)

    return configs_file