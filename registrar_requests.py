# import get from requests to get the content of the url
from requests import get

# import BeautifulSoup to parse the content of the url
from bs4 import BeautifulSoup

# import Color_cli and Questions classes to print colorful text and ask user for input
from cli import Color_cli, Questions

# import time_delay to make the script wait
from delay import time_delay

def get_requests(url:str) -> dict:
    """
    This function do a get request by `url` and return value as dict
    """

    while True:
        try:
            registrar_request = get(url)
            break
        except:
            Color_cli.colorful_print(text="\n! You don't have internet connection, the script will check for sections every 10s..", text_color=Color_cli.BRIGHT_RED)
            time_delay(10)

    if (registrar_request.status_code != 200):
        Color_cli.colorful_print(text="! The website isn't working for the time being, the script will check every 60s..", text_color=Color_cli.BRIGHT_RED)
        time_delay(60)
        return get_requests(url)
    else:
        return get_elements(registrar_request.content)

def get_elements(content) -> list:
    """
    This function get terms and departments of the request
    """

    soup = BeautifulSoup(content, "html.parser")

    user_inputs = []
    for index, elements in enumerate(["course_term_code", "course_dept_code"]):
        i = soup.find(id=elements)
        if (i is None):
            return soup
        options = i.find_all("option")[1::]

        dict_elements = {}
        for option in options:
            dict_elements[option.text] = option["value"]
        dict_answer = Questions.dict_question(question=("Select the term has/have the course/courses" if index==0 else "Select the department has/have the course/courses"), choices=dict_elements)

        user_inputs.append(dict_answer)

    return user_inputs