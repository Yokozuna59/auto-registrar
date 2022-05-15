# import path and getcwd to check if user has runed the program before
from os import path, getcwd

# import loads and dump to load and dump the json data
from json import loads, dump

# import cli_colors ans Questions classes to print colorful text and ask user for input
from cli import ColorfulText, Questions

def check_configurations() -> dict:
    """
    Checks if user has installed and configured his default configuration.\n
    If he did, return it as `dict` type.
    """

    # get current path
    current_path = getcwd()
    if ("src" not in current_path):
        # print error messege and stop the script
        ColorfulText.colorful_print(text_string="! Sorry, you are in the wrong directory.", text_color=ColorfulText.BRIGHT_RED)
        ColorfulText.colorful_print(text_string="Use `cd` command to change directory.", text_color=ColorfulText.BRIGHT_CYAN)
        exit()

    if (not path.exists(current_path.replace("src", ".config.json"))):
        # print error messege and stop the script
        ColorfulText.colorful_print(text_string="! Sorry, you have run the `install.sh` file to run the script!", text_color=ColorfulText.BRIGHT_RED)
        exit()

    # open config file
    no_src_path = current_path.replace("src", "")
    with open(f"{no_src_path}.config.json", 'r') as f:
        # read and loads config file
        config_file = loads(f.read())
    browser = config_file["browser"]
    # check if user has configured yet or not
    if (config_file['configuration'] == None):
        # print error messege
        ColorfulText.colorful_print(text_string="! Sorry, you haven't configured yet.", text_color=ColorfulText.BRIGHT_RED)

        # Ask user if he wants to config now or not
        bool_answer = Questions.bool_question(question="Do you want to configurate now")

        # if True ask 5 question and config the file
        if (bool_answer == True):
            config_file = configuring(file_path=no_src_path, config_file=config_file)
    config_file["driver"] = "{}{}".format(f"{no_src_path}/driver/", "chromedriver" if browser == "chrome" else "geckodriver")
    return config_file

def configuring(file_path: str, config_file: str) -> dict:
    """
    Ask user 5 diffrent questinos to do configuration.\n
    If he answered them, return them as `dict` type.
    """

    with open(f"{file_path}.config.json", 'r') as f:
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

    with open(f"{file_path}.config.json", "w") as f:
        dump(config_file, f)

    return config_file