# import functions from modules
from requests import get, session, post
from requests.exceptions import ConnectionError, RequestException
from json import loads
from sys import exit

# import functions from local files
from cli import AnsiEscapeCodes, Questions, progress_bar, print_colorful_text

def get_term_and_department(interface_config: str):
    """
    Do a get request by `url` and ask user to select a term and department.\n
    return the user answer as `list` type.
    """

    terms_and_departments_list = []
    urls = [
        "https://banner9-registration.kfupm.edu.sa/StudentRegistrationSsb/ssb/classSearch/getTerms?searchTerm=&offset=1&max=1000",
        "https://banner9-registration.kfupm.edu.sa/StudentRegistrationSsb/ssb/classSearch/get_subject?searchTerm=&term=&offset=1&max=1000"
    ]

    for url_index, url in enumerate(urls):
        request_done = False
        while not request_done:
            try:
                response = get(url=(url if (len(terms_and_departments_list) == 0) else url.replace("term=", f"term={terms_and_departments_list[0]}"))).content
                loaded_response = loads(response)

                terms_or_departments_dict = {}
                index = 0
                term_or_department_numbers = 0
                finished = False

                while (not (finished)) and (index < len(loaded_response)-1):
                    description = loaded_response[index]["description"]
                    term_department = loaded_response[index]["code"]

                    if (not ("(View Only)" in description)):
                        terms_or_departments_dict[description.replace("amp;", "")] = term_department
                        term_or_department_numbers += 1
                    else:
                        finished = True
                    index += 1
                if (term_or_department_numbers == 0):
                    print_colorful_text(text_string="! Sorry, there is no terms or departments available for registration.", color=AnsiEscapeCodes.RED)
                    exit()
                request_done = True
            except ConnectionError:
                if (interface_config == "cli"):
                    print_colorful_text(text_string="! Sorry, you currently don't have internet connection! the script will recheck in 10 seconds.", text_color=AnsiEscapeCodes.RED)
                    progress_bar(10)
            except RequestException:
                if (interface_config == "cli"):
                    print_colorful_text(text_string="! Sorry, the website isn't working currently! the script will recheck in 60 seconds", text_color=AnsiEscapeCodes.RED)
                    progress_bar(60)

        if (interface_config == "cli"):
            term_or_department_choice = Questions.dict_question(question=("Select the term has/have the course/courses" if url_index == 0 else "Select the department has/have the course/courses"), choices=terms_or_departments_dict)
            terms_and_departments_list.append(term_or_department_choice)
    return terms_and_departments_list

def get_banner9_requests(term: str, department: str) -> dict:
    """
    Do a get and post requests to get content.\n
    Return the content as a `dict` type.
    """

    # create a session
    session_client = session()

    # get session id
    request_cookies = session_client.get("https://banner9-registration.kfupm.edu.sa/StudentRegistrationSsb/ssb/term/termSelection?mode=search")
    session_id = dict(request_cookies.cookies)["JSESSIONID"]

    post("https://banner9-registration.kfupm.edu.sa/StudentRegistrationSsb/ssb/term/search?mode=search",
        cookies = {
            "JSESSIONID": session_id
        },
        data = {
            "term": term
        }
    )
    response = get(f"https://banner9-registration.kfupm.edu.sa/StudentRegistrationSsb/ssb/searchResults/searchResults?txt_term={term}&txt_subject={department}&pageMaxSize=1000",
        cookies = {
            "JSESSIONID": session_id
        }
    )

    courses = loads(response.text)["data"]
    return courses

"""{'section': ['312', '012', '12', '01', ' 9'], 'activity': ['DIS', 'FLD', 'IND', 'LAB', 'LLB', 'LEC', 'MR', 'PRJ', 'RES', ...], 'crn': ['32131', '14141', '01424', '12424'], 'course_number': ['ICS104', 'ENGL101'], 'class_days': ['M', 'T', 'W', 'R', 'F', 'S'], 'building': ['31', '1', '41', '51'], 'status': 'Open', 'gender': 'M', 'registrar': False}"""