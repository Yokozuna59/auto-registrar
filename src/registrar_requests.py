from requests import get, session, post
from requests.exceptions import ConnectionError, RequestException, Timeout
from bs4 import BeautifulSoup
from cli import AnsiEscapeCodes, Questions, progress_bar, print_colorful_text
from json import loads

def get_term_and_department(request_url: str, interface_config: str):
    """
    Do a get request by `url` and ask user to select a term and department.\n
    return the user answer as `list` type.
    """

    while True:
        try:
            response = get(url=request_url).text
            if ("Under Maintenance" in response):
                if (interface_config == "cli"):
                    print_colorful_text(text_string="! Sorry, the website is under maintenance currently! the script will recheck in 60 seconds.", text_color=AnsiEscapeCodes.RED)
                    progress_bar(60)
            else:
                break
        except ConnectionError:
            if (interface_config == "cli"):
                print_colorful_text(text_string="! Sorry, you currently don't have internet connection! the script will recheck in 10 seconds.", text_color=AnsiEscapeCodes.RED)
                progress_bar(10)
        except RequestException:
            if (interface_config == "cli"):
                print_colorful_text(text_string="! Sorry, the website isn't working currently! the script will recheck in 60 seconds", text_color=AnsiEscapeCodes.RED)
                progress_bar(60)

    user_input = []
    soup = BeautifulSoup(response, "html.parser")
    for index, element_id in enumerate(["ddlTerm", "ddlDept"]):
        element = soup.find(id=element_id)
        options = element.find_all("option") if element_id != "ddlDept" else element.find_all("option")[1::]

        dict_elements = {}
        for option in options:
            dict_elements[option.text] = option["value"]

        if (interface_config == "cli"):
            dict_answer = Questions.dict_question(question=("Select the term has/have the course/courses" if index == 0 else "Select the department has/have the course/courses"), choices=dict_elements)
        user_input.append(dict_answer)
    return user_input

def get_course_offering_data(term: str, department: str, interface_config :str, user_search: dict) -> dict:
    """
    Do a get request by `url` and get content.\n
    return the content as a `dict` type.
    """

    while True:
        try:
            response = get(url="https://registrar.kfupm.edu.sa/api/course-offering?term_code={}&department_code={}".format(term, department), timeout=10).content
            return loads(response)["data"]
        except Timeout:
            return banner9_get_requests(term=term, department=department, user_search=user_search)
        except ConnectionError:
            if (interface_config == "cli"):
                print_colorful_text(text_string="! Sorry, you currently don't have internet connection! the script will recheck in 10 seconds.", text_color=AnsiEscapeCodes.RED)
                progress_bar(10)
        except RequestException:
            if (interface_config == "cli"):
                print_colorful_text(text_string="! Sorry, the website isn't working currently! the script will recheck in 60 seconds", text_color=AnsiEscapeCodes.RED)
                progress_bar(60)

def banner9_get_requests(term: str, department: str, user_search: dict) -> dict:
    """
    Do a get and post requests to get content.\n
    return the content as a `dict` type.
    """

    # create a session
    sessionClient = session()

    # get session id
    request_cookies = sessionClient.get("https://banner9-registration.kfupm.edu.sa/StudentRegistrationSsb/ssb/term/termSelection?mode=search")
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
    courses_list = []
    courses = loads(response.text)["data"]
    for i in courses:
        course_data = {}
        course_data["crn"] = i["courseReferenceNumber"]
        course_data["section_number"] = i["sequenceNumber"]
        course_data["available_seats"] = i["seatsAvailable"]
        course_data["waiting_list_count"] = i["waitAvailable"]
        course_data["course_number"] = i["subjectCourse"]
        course_data["instructor_name"] = i["faculty"][0]["displayName"]
        course_data["class_type"] = i["meetingsFaculty"][0]["meetingTime"]["meetingScheduleType"]
        course_data["building"] = i["meetingsFaculty"][0]["meetingTime"]["building"]
        course_data["gender"] = "F" if i["meetingsFaculty"][0]["meetingTime"]["campus"] == "F" else "M"
        courses_list.append(course_data)

        # course_data["class_days"] = []
            # for j in ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]:
                # course_data["class_days"].append(j)
                # course_data["class_days"] = i["meetingsFaculty"][0]["meetingTime"]
    return courses_list

# {'section': ['312', '012', '12', '01', ' 9'], 'activity': ['DIS', 'FLD', 'IND', 'LAB', 'LLB', 'LEC', 'MR', 'PRJ', 'RES', ...], 'crn': ['32131', '14141', '01424', '12424'], 'course_number': ['ICS104', 'ENGL101'], 'class_days': ['M', 'T', 'W', 'R', 'F', 'S'], 'building': ['31', '1', '41', '51'], 'status': 'Open', 'gender': 'M', 'registrar': False}