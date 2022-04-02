# import color_print function to print colored text
from colorful_terminal import color_print

# import delay function to make the script wait
from delay import time_delay

# import main function from real_main.py file to run the script
from old_main import *

# import get_requests function to get the content of the url
from registrar_requests import get_requests

def not_configured():
    color_print("[!] - You haven't configured yet. Please configure first.", tcolor.FAIL)

def number_out_of_range():
    color_print("[!] - You can't choose a number out of range!", tcolor.FAIL)
    exit()

def input_not_int(user_input):
    color_print(f"[!] - {user_input} is not a digit, please choose a digit.", tcolor.FAIL)
    exit()

def no_config_file():
    color_print("[!] - You haven't run the install.sh file yet OR you are in the wrong directory.", tcolor.FAIL)
    exit()

def no_internet_connection(url):
    color_print("[!] - You don't have internet connection, the script will check for sections every 10s..", tcolor.FAIL)
    time_delay(10)
    return get_requests(url)

def request_not_200(url):
    color_print("[!] - The website isn't working for the time being, the script will check every 60s..", tcolor.FAIL)
    time_delay(60)
    return get_requests(url)

def data_is_none(term, department):
    color_print("[!] - The API isn't working for the time being, the script will check for sections every 60s..", tcolor.FAIL)
    time_delay(60)
    return get_api_requests(term, department)