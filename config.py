# import path to check if user has runed the program before
from os import path

# import loads to load the json data
from json import loads, dump

# import colorful_terminal.py file to use tcolor Class and color_print, color_input and color_choices Functions
from colorful_terminal import *

# import didnt_config function, number_out_of_range and no_config_file from errors.py file to show the error messages
from errors import didnt_config, number_out_of_range, no_config_file

def check_config():
    # check if the config file exists
    if path.exists("config.json"):
        # check if user has configured yet or not
        with open('config.json', 'r') as f:
            configurations = loads(f.read())

            if configurations['configuration'] == None:
                didnt_config()
                color_choices(["Configurate Now (just 6 questions).", "Configurate Later (use defult configuration)."])

                user_input = int(color_input("[*] - Please choose: ", tcolor.OKGREEN))
                if (user_input == 1 or user_input == 2):
                    if user_input == "1":
                        configurations = config(configurations)
                else:
                    number_out_of_range()
            return configurations
    else:
        no_config_file()

def config(configurations):
    configurations["configuration"] = "configed"

    with open("config.json", "w") as f:
        dump(configurations, f)