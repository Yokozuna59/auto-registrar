# import path to check if user has runed the program before
from os import path

# import loads and dump to load and dump the json data
from json import loads, dump

# import tcolor class and color_input and color_choices functions to print colored text
from colorful_terminal import color_choices, color_input

# import not_configured, number_out_of_range, no_config_file and input_not_digit functions to show the error messages
from errors import not_configured, number_out_of_range, no_config_file, input_not_int

def check_config():
    # check if the config file exists
    if path.exists("config.json"):
        # check if user has configured yet or not
        with open('config.json', 'r') as f:
            configurations = loads(f.read())

            if configurations['configuration'] == None:
                not_configured()
                color_choices(["Configurate Now (just 5 questions).", "Configurate Later (use defult configuration)."])

                user_input = color_input("[*] - Please choose: ")
                if (user_input.isdigit()):
                    if (user_input == "1" or user_input == "2"):
                        if user_input == "1":
                            configurations = do_config(configurations)
                    else:
                        number_out_of_range()
                else:
                    input_not_int(user_input)
            return configurations
    else:
        no_config_file()

def do_config(configurations):
    username = color_input("Enter your portal email: ")
    configurations["username"] = username

    passcode = color_input("Enter your portal passcode: ")
    configurations["passcode"] = passcode

    color_choices(["Chrome", "Firefox"])
    user_input = color_input("[*] - Please choose: ")
    if (user_input.isdigit()):
        if (user_input == "1"):
            configurations["browser"] = "chrome"
        elif (user_input == "2"):
            configurations["browser"] = "firefox"
        else:
            number_out_of_range()
    else:
        input_not_int(user_input)

    color_choices(["10s","20s", "30s", "60s"])
    user_input = color_input("[*] - Please choose: ")
    if (user_input.isdigit()):
        user_input = int(user_input)

        if (user_input >= 1 and user_input <= 4):
            if (user_input == 4):
                user_input *= 15
            else:
                user_input *= 10
        else:
            number_out_of_range()
    else:
        input_not_int(user_input)
    configurations["delay"] = user_input

    # banner: 8 or 9

    configurations["configuration"] = "configed"

    with open("config.json", "w") as f:
        dump(configurations, f)