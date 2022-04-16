# import get from requests to get the content of the url
from requests import get

# import BeautifulSoup to parse the content of the url
from bs4 import BeautifulSoup

# import color_choices and color_input functions to print colored text
from colorful_terminal import color_choices, color_input

# import no_internet_connection, request_not_200 and check_user_input functions to show the error messages
import errors

def get_requests(url):
    try:
        registrar_request = get(url)
    except:
        return get_elements(errors.no_internet_connection(url))

    if (registrar_request.status_code != 200):
        errors.request_not_200(url)
    else:
        return get_elements(registrar_request.content)

def get_elements(content):
    soup = BeautifulSoup(content, "html.parser")

    user_inputs = []
    for i in ("course_term_code", "course_dept_code"):
        element = soup.find(id=i)
        if (element is None):
            return soup
        options = element.find_all("option")[1::]

        elements_dict = {}
        for option in options:
            elements_dict[option.text] = option["value"]

        color_choices(elements_dict)
        user_input = color_input()
        user_input = errors.check_user_input(user_input, len(elements_dict))
        user_inputs.append(list(elements_dict.values())[user_input - 1])

    return user_inputs