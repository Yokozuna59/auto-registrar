# import path to check if user has runed the program before
from os.path import exists

# import loads and dump to load and dump the json data
from json import loads, dump

# import cli_colors ans Questions classes to print colorful text and ask user for input
from cli import cli_colors, Questions

def check_configuration() -> dict:
    """
    Checks if user has installed and configured his default configuration.\n
    If he did, return it as `dict` type.
    """

    # check if the `install.sh`` file exists
    if (exists("install.sh")):
        # check if the user_pass.json file exists
        if (exists(".config/user_pass.json")):
            # open config file
            with open('.config/config.json', 'r') as f:
                # read and loads config file
                config_file = loads(f.read())

                # check if user has configured yet or not
                if (config_file['configuration'] == None):
                    # print error messege
                    cli_colors.colorful_print(text_string="! Sorry, you haven't configured yet.", text_color=cli_colors.BRIGHT_RED)

                    # Ask user if he wants to config now or not
                    bool_answer = Questions.bool_question(question="Do you want to configurate now")

                    # if True ask 5 question and config the file
                    if (bool_answer == True):
                        config_file = configuring(config_file=config_file)
                return config_file
        else:
            # print error messege and stop the script
            cli_colors.colorful_print(text_string="! You have run the `install.sh` program yet!", text_color=cli_colors.BRIGHT_RED)
            exit()
    else:
        # print error messege and stop the script
        cli_colors.colorful_print(text_string="! Sorry, you are in the wrong directory.", text_color=cli_colors.BRIGHT_RED)
        cli_colors.colorful_print(text_string="Use `cd` command to change directory.", text_color=cli_colors.BRIGHT_CYAN)
        exit()

def configuring(config_file: str) -> dict:
    """
    Ask user 5 diffrent questinos to do configuration.\n
    If he answered them, return them as `dict` type.
    """

    with open('.config/user_pass.json', 'r') as f:
        user_pass_file = loads(f.read())

        username = Questions.str_questoin(question="Enter your student ID with `S`")
        user_pass_file["username"] = username

        passcode = Questions.passcode_question(question="Enter your portal passcode")
        user_pass_file["passcode"] = passcode

        with open(".config/user_pass.json", "w") as f:
            dump(user_pass_file, f)

    browser = Questions.dict_question(question="Select default browser", choices={"Chrome":"chrome", "Firefox":"firefox"})
    config_file["browser"] = browser

    time_delay = Questions.dict_question(question="Select default time delay between refreshes", choices={"10 second":10, "20 Second":20, "30 Second":30, "60 Second":60})
    config_file["delay"] = time_delay

    banner = Questions.dict_question(question="Select default banner for registration", choices={"Banner 8":8, "Banner 9":9})
    config_file["banner"] = banner

    config_file["configuration"] = "configured"

    with open(".config/config.json", "w") as f:
        dump(config_file, f)

    return config_file