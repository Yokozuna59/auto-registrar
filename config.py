# import path to check if user has runed the program before
from os import path

# import loads and dump to load and dump the json data
from json import loads, dump

# import tcolor class and color_input and color_choices functions to print colored text
from colorful_terminal import tcolor, color_choices, color_input

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
                color_choices(["Configurate Now (just 6 questions).", "Configurate Later (use defult configuration)."])

                user_input = color_input("[*] - Please choose: ", tcolor.OKGREEN)
                if (user_input.isdigit()):
                    if (user_input == "1" or user_input == "2"):
                        if user_input == "1":
                            configurations = config(configurations)
                    else:
                        number_out_of_range()
                else:
                    input_not_int(user_input)
            return configurations
    else:
        no_config_file()

def config(configurations):
    configurations["configuration"] = "configed"

    with open("config.json", "w") as f:
        dump(configurations, f)