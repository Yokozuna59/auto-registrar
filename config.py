# import path to check if user has runed the program before
from os import path

# import loads and dump to load and dump the json data
from json import loads, dump

# import tcolor class and color_input and color_choices functions to print colored text
from colorful_terminal import color_choices, color_input

# import not_configured, number_out_of_range, no_config_file and input_not_digit functions to show the error messages
from errors import check_user_input, not_configured, no_config_file

def check_config():
    # check if the config file exists
    if (path.exists("config.json")):
        with open('config.json', 'r') as f:
            configurations = loads(f.read())

            # check if user has configured yet or not
            if (configurations['configuration'] == None):
                not_configured()
                color_choices(["Configurate Now (just 5 questions).", "Configurate Later (use defult configuration)."])

                user_input = color_input()
                user_input = check_user_input(user_input, 2)
                if (user_input == 1):
                    configurations = do_config(configurations)
            return configurations
    else:
        no_config_file()

def do_config(configurations):
    username = color_input("Enter your portal email: ")
    configurations["username"] = username

    passcode = color_input("Enter your portal passcode: ")
    configurations["passcode"] = passcode

    color_choices(["Chrome", "Firefox"])
    user_input = color_input()
    user_input = check_user_input(user_input, 2)
    if (user_input == 1):
        configurations["browser"] = "chrome"
    else:
        configurations["browser"] = "firefox"

    color_choices(["10s","20s", "30s", "60s"])
    user_input = color_input()
    user_input = check_user_input(user_input, 4)
    if (user_input != 4):
        user_input *= 10
    else:
        user_input *= 15
    configurations["delay"] = user_input

    # banner: 8 or 9

    configurations["configuration"] = "configed"

    with open("config.json", "w") as f:
        dump(configurations, f)

    return configurations