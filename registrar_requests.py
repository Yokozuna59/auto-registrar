# import get from requests to get the content of the url
from requests import get

# import BeautifulSoup to parse the content of the url
from bs4 import BeautifulSoup

# import color_choices function from colorful_terminal.py file to show the choices of the user
from colorful_terminal import color_choices

# import requests_not_200 function from errors.py file to check if the website is working or not
# import and no_internet_connection function from errors.py file to check if there is internet connection or not
import errors

# import get_user_input function from user_inputs.py file to get the user input
from user_inputs import get_user_input

def get_requests(url):
    try:
        registrar_request = get(url)
    except:
        return errors.no_internet_connection(url)

    if (registrar_request.status_code != 200):
        errors.request_not_200(url)
    else:
        return registrar_request.content

def get_elements(content):
    soup = BeautifulSoup(content, "html.parser")

    user_inputs = []
    for i in ("course_term_code", "course_dept_code"):
        element = soup.find(id=i)
        options = element.find_all("option")[1::]

        elements_dict = {}
        for option in options:
            elements_dict[option.text] = option["value"]

        color_choices(elements_dict)
        user_input = int(get_user_input(elements_dict))
        user_inputs.append(list(elements_dict.values())[user_input - 1])

    return user_inputs