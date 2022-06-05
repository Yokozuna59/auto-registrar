from __future__ import barry_as_FLUFL
from requests import get
from bs4 import BeautifulSoup
from cli import AnsiEscapeCodes, Questions, progress_bar, colorful_text

def get_requests(request_url: str, interface_config :str):
    """
    Do a get request by `url`.\n
    return it value as `dict` or `list` type.
    """

    while True:
        try:
            registrar_request = get(url=request_url)
            if (not "Under Maintenance!" in registrar_request.text):
                break
            if (interface_config == "cli"):
                colorful_text(text_string="! Sorry, the currently is under maintenance! the script will check in 60 seconds.", text_color=AnsiEscapeCodes.RED)
                progress_bar(60)
        except:
            if (interface_config == "cli"):
                colorful_text(text_string="! Sorry, you currently don't have internet connection! the script will check in 10 seconds.", text_color=AnsiEscapeCodes.RED)
                progress_bar(10)

    if (registrar_request.status_code != 200):
        if (interface_config == "cli"):
            colorful_text(text_string="! Sorry, the website isn't working currently! the script will check in 60 seconds", text_color=AnsiEscapeCodes.RED)
            progress_bar(60)
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
    for index, elements in enumerate(["ddlTerm", "ddlDept"]):
        i = soup.find(id=elements)
        if (i is None):
            return soup
        options = i.find_all("option") if elements != "ddlDept" else i.find_all("option")[1::]

        dict_elements = {}
        for option in options:
            dict_elements[option.text] = option["value"]

        if (interface_config == "cli"):
            dict_answer = Questions.dict_question(question=("Select the term has/have the course/courses" if index==0 else "Select the department has/have the course/courses"), choices=dict_elements)
        user_inputs.append(dict_answer)
    return user_inputs