# import color_print function to print colored text
from colorful_terminal import tcolor, color_print

# import delay function to make the script wait
from delay import time_delay

# import get_requests function to get the content of the url
from registrar_requests import get_requests

def no_config_file():
    color_print("[!] - You haven't run the install.sh file yet OR you are in the wrong directory.", tcolor.FAIL)
    exit()

def not_configured():
    color_print("[!] - You haven't configured yet. Please configure first.", tcolor.FAIL)

def check_user_input(user_input, last):
    if (user_input.isdigit()):
        user_input = int(user_input)

        if (user_input >= 1 and user_input <= last):
            return user_input
        else:
            color_print("[!] - You can't choose a number out of range!", tcolor.FAIL)
    else:
        color_print(f"[!] - {user_input} is not a digit, please choose a digit.", tcolor.FAIL)
    exit()

def no_internet_connection(url):
    color_print("[!] - You don't have internet connection, the script will check for sections every 10s..", tcolor.FAIL)
    time_delay(10)
    return get_requests(url)

def request_not_200(url):
    color_print("[!] - The website isn't working for the time being, the script will check every 60s..", tcolor.FAIL)
    time_delay(60)
    return get_requests(url)