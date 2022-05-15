# import get from requests to get the content of the url
from requests import get

# import BeautifulSoup to parse the content of the url
from bs4 import BeautifulSoup

# import cli_colors and Questions classes to print colorful text and ask user for input
from cli import ColorfulText, Questions, time_delay

def get_requests(request_url: str, interface_config :str):
    """
    Do a get request by `url`.\n
    return it value as `dict` or `list` type.
    """

    while True:
        try:
            registrar_request = get(url=request_url)
            break
        except:
            if (interface_config == "cli"):
                ColorfulText.colorful_print(text_string="\n! Sorry, you currently don't have internet connection! the script will check in 10 seconds.", text_color=ColorfulText.BRIGHT_RED)
                time_delay(10)

    if (registrar_request.status_code != 200):
        if (interface_config == "cli"):
            ColorfulText.colorful_print(text_string="! Sorry, the website isn't working currently! the script will check in 60 seconds", text_color=ColorfulText.BRIGHT_RED)
            time_delay(60)
        return get_requests(request_url=request_url)
    else:
        return get_elements(content=registrar_request.content, interface_config=interface_config)

def get_elements(content: str, interface_config: str) -> list:
    """
    Get terms and departments of the request.\n
    return it as a `list` type.
    """

    user_inputs = []
    soup = BeautifulSoup(content, "html.parser")
    for index, elements in enumerate(["course_term_code", "course_dept_code"]):
        i = soup.find(id=elements)
        if (i is None):
            return soup
        options = i.find_all("option")[1::]

        dict_elements = {}
        for option in options:
            dict_elements[option.text] = option["value"]

        if (interface_config == "cli"):
            dict_answer = Questions.dict_question(question=("Select the term has/have the course/courses" if index==0 else "Select the department has/have the course/courses"), choices=dict_elements)
        user_inputs.append(dict_answer)
    return user_inputs