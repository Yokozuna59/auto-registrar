from asyncio import gather, get_event_loop
from concurrent.futures import ThreadPoolExecutor
from sys import exit

from requests import Session, get
from requests.exceptions import ConnectionError

from auto_registrar.tui.ansi import AnsiColor
from auto_registrar.tui.bar import progress_bar
from auto_registrar.tui.colored_text import print_one_color_text
from auto_registrar.tui.questions import Questions

DAYS = {
    "sunday": "U",
    "monday": "M",
    "tuesday": "T",
    "wednesday": "W",
    "thursday": "R",
    "friday": "F",
    "saturday": "S",
}

BANNER_CHIOCES = {
    "ACCT": "ACFN",
    "ECON": "ACFN",
    "FIN": "ACFN",
    "AS": None,
    "AE": "AE",
    "ARE": "ARE",
    "ARC": "ARC",
    "BIOE": "BIOE",
    "BUS": "MGT",
    "HRM": "MGT",
    "MGT": "MGT",
    "MKT": "MGT",
    "CHE": "CHE",
    "CHEM": "CHEM",
    "CRP": "CRP",
    "CP": "CRP",
    "CE": "CE",
    "CGS": "ELD",
    "ENGL": "ELD",
    "CPG": "CPG",
    "COE": "COE",
    "CEM": "CEM",
    "EM": "CEM",
    "CIE": "CIE",
    "SCE": "CIE",
    "XE": None,
    "EE": "EE",
    "ENVS": "ERTH",
    "GEOL": "ERTH",
    "GEO": "ERTH",
    "GEOP": "ERTH",
    "GS": "GS",
    "ISE": "SE",
    "ICS": "ICS",
    "SEC": "ICS",
    "SWE": "ICS",
    "IAS": "IAS",
    "LS": "LS",
    "MIS": "ISOM",
    "OM": "ISOM",
    "MBA": "MBA",
    "MSE": "MSE",
    "MATH": "MATH",
    "STAT": "MATH",
    "ME": "ME",
    "PETE": "PETE",
    "PE": "PE",
    "PHYS": "PHYS",
    "SE": None,
}

REGISTRER_CHIOCES = {
    "ACFN": "ACCT,ECON,FIN",
    "AE": "AE",
    "ARE": "ARE",
    "ARC": "ARC",
    "BIOE": "BIOE",
    "MGT": "BUS,HRM,MGT,MKT",
    "CHE": "CHE",
    "CHEM": "CHEM",
    "CRP": "CRP,CP",
    "CE": "CE",
    "ELD": "CGS,ENGL",
    "CPG": "CPG",
    "COE": "COE",
    "CEM": "CEM,EM",
    "CIE": "CIE,SCE",
    "EE": "EE",
    "ERTH": "ENVS,GEOL,GEOP",
    "GS": "GS",
    "ISE": "SE",
    "ICS": "ICS,SEC,SWE",
    "IAS": "IAS",
    "LS": "LS",
    "ISOM": "MIS,OM",
    "MBA": "MBA",
    "MSE": "MSE",
    "MATH": "MATH,STAT",
    "ME": "ME",
    "PETE": "PETE",
    "PE": "PE",
    "PHYS": "PHYS",
}


class KFUPM_banner9:
    def get_banner9_terms_and_departments(interface: str) -> tuple:
        term = KFUPM_banner9.get_banner9_terms(interface=interface)
        departments = KFUPM_banner9.get_banner9_departments(
            term=term, interface=interface
        )

        return term, departments

    def get_banner9_terms(interface: str) -> str:
        request_done = False
        url = "https://banner9-registration.kfupm.edu.sa/StudentRegistrationSsb/ssb/classSearch/getTerms?searchTerm=&offset=1&max=1000"

        while not request_done:
            try:
                response = get(url=url)
                loaded_response = response.json()

                index = 0
                terms_dict = {}
                finished = False

                while (not finished) and (index < len(loaded_response) - 1):
                    term_code = loaded_response[index]["code"]
                    description = loaded_response[index]["description"]

                    if not ("(View Only)" in description):
                        terms_dict[description.replace("amp;", "")] = term_code
                    else:
                        finished = True
                    index += 1

                if len(terms_dict) == 0:
                    print_one_color_text(
                        text_string="! Sorry, there isn't any terms available for registration.",
                        color=AnsiColor.RED,
                    )
                    exit()
                request_done = True
            except ConnectionError:
                if interface == "cli":
                    print_one_color_text(
                        text_string="! Sorry, you currently don't have internet connection! the script will recheck in 10 seconds.",
                        text_color=AnsiColor.RED,
                    )
                    progress_bar(total_time=10)

            sorted_terms_dict = dict(
                sorted(terms_dict.items(), key=lambda x: x[1], reverse=True)
            )
            if interface == "cli":
                term_choice = Questions.dict_question(
                    question=("Select the term has/have the course/courses"),
                    choices=sorted_terms_dict,
                )
        return term_choice

    def get_banner9_departments(term: str, interface: str) -> list:
        url = (
            "https://banner9-registration.kfupm.edu.sa/StudentRegistrationSsb/ssb/classSearch/get_subject?searchTerm=&term=%s&offset=1&max=1000"
            % term
        )

        request_done = False
        while not request_done:
            try:
                response = get(url=url)
                loaded_response = response.json()

                index = 0
                departments_dict = {}

                while index < len(loaded_response) - 1:
                    department_code = loaded_response[index]["code"]
                    description = loaded_response[index]["description"]
                    departments_dict[description.replace("amp;", "")] = department_code
                    index += 1

                if len(departments_dict) == 0:
                    print_one_color_text(
                        text_string="! Sorry, there is no department available for registration.",
                        color=AnsiColor.RED,
                    )
                    exit()
                request_done = True
            except ConnectionError:
                if interface == "cli":
                    print_one_color_text(
                        text_string="! Sorry, you currently don't have internet connection! the script will recheck in 10 seconds.",
                        text_color=AnsiColor.RED,
                    )
                    progress_bar(total_time=10)

            if interface == "cli":
                departments_choices = Questions.mcq_dict_question(
                    question=("Select the department has/have the course/courses"),
                    choices=departments_dict,
                )
                departments_list = []
                for department in departments_choices:
                    if BANNER_CHIOCES[department] != None:
                        departments_list.append(BANNER_CHIOCES[department])

        return departments_list

    async def get_banner9_courses(term: str, departments: list, interface: str) -> list:
        """
        Do a get and post requests to get content.\n
        Return the content as a `dict` type.
        """

        request_finished = False
        courses = []
        departments_list = []
        for department in departments:
            if department in REGISTRER_CHIOCES:
                departments_list.append(REGISTRER_CHIOCES[department])
        departments_list = ",".join(departments_list)

        search_url = "https://banner9-registration.kfupm.edu.sa/StudentRegistrationSsb/ssb/term/search?mode=search"
        while not request_finished:
            try:
                session = Session()
                response = session.get(url=search_url)

                session.post(
                    url=search_url,
                    data={"term": term},
                )

                request_url = (
                    "https://banner9-registration.kfupm.edu.sa/StudentRegistrationSsb/ssb/searchResults/searchResults?txt_term=%s&txt_subject=%s&pageOffset=0&pageMaxSize=500"
                    % (term, departments_list)
                )
                response = session.get(
                    url=request_url,
                )
                if (response.status_code == 200) and (response.json()["data"] != None):
                    courses += response.json()["data"]
                    number_of_pages = int(response.json()["sectionsFetchedCount"] / 500)

                    request_finished = True
            except ConnectionError:
                if interface == "cli":
                    print_one_color_text(
                        text_string="! Sorry, you currently don't have internet connection! the script will recheck in 10 seconds.",
                        text_color=AnsiColor.RED,
                    )
                    progress_bar(10)

        urls = [
            "https://banner9-registration.kfupm.edu.sa/StudentRegistrationSsb/ssb/searchResults/searchResults?txt_term=%s&txt_subject=%s&pageOffset=%d&pageMaxSize=500"
            % (term, departments_list, page_off_set)
            for page_off_set in range(1, number_of_pages)
        ]

        request_finished = False
        with ThreadPoolExecutor() as executor:
            loop = get_event_loop()
            while not request_finished:
                try:
                    futures = [
                        loop.run_in_executor(executor, session.get, url) for url in urls
                    ]
                    for response in await gather(*futures):
                        if (response.status_code == 200) and (
                            response.json()["data"] != None
                        ):
                            courses += response.json()["data"]
                    request_finished = True
                except ConnectionError:
                    if interface == "cli":
                        print_one_color_text(
                            text_string="! Sorry, you currently don't have internet connection! the script will recheck in 10 seconds.",
                            text_color=AnsiColor.RED,
                        )
                        progress_bar(10)

        courses_structured = KFUPM_banner9.get_banner9_courses_structured(
            courses_requested=courses
        )
        return courses_structured

    def get_banner9_courses_structured(courses_requested: list) -> list:
        found_elements = list(
            filter(
                lambda x: int(x["seatsAvailable"]) > 0 or int(x["waitAvailable"]) > 0,
                courses_requested,
            )
        )

        courses_structured = []
        for element in found_elements:
            course_dict = {}
            course_dict["crn"] = element["courseReferenceNumber"]
            course_dict["course_name"] = element["subjectCourse"].replace(" ", "")
            course_dict["section"] = element["sequenceNumber"]
            course_dict["available_seats"] = int(element["seatsAvailable"])
            course_dict["waiting_list_count"] = int(element["waitAvailable"])
            course_dict["class_type"] = element["meetingsFaculty"][0]["meetingTime"][
                "meetingScheduleType"
            ]
            course_dict["class_days"] = "".join(
                [
                    DAYS[day]
                    for day in DAYS
                    if element["meetingsFaculty"][0]["meetingTime"][day]
                ]
            )
            course_dict["start_time"] = element["meetingsFaculty"][0]["meetingTime"][
                "beginTime"
            ]
            course_dict["end_time"] = element["meetingsFaculty"][0]["meetingTime"][
                "endTime"
            ]
            course_dict["building"] = element["meetingsFaculty"][0]["meetingTime"][
                "building"
            ]
            course_dict["room"] = element["meetingsFaculty"][0]["meetingTime"]["room"]
            if len(element["faculty"]) != 0:
                course_dict["instructor_name"] = element["faculty"][0]["displayName"]
            else:
                course_dict["instructor_name"] = ""
            courses_structured.append(course_dict)
        return courses_structured

    def get_user_schedule(
        username: str, passcode: str, term: str, interface: str
    ) -> dict:
        session = Session()
        schedule_url = "https://banner9-registration.kfupm.edu.sa/StudentRegistrationSsb/ssb/registrationHistory/registrationHistory"

        try:
            response = session.get(url=schedule_url)
            session_data_key = response.url.split("&")[6].split("=")[1]
            session.post(
                url="https://login.kfupm.edu.sa/commonauth",
                data={
                    "usernameUserInput": "",
                    "username": "@carbon.super",
                    "password": "",
                    "chkRemember": "on",
                    "sessionDataKey": session_data_key,
                },
            )
            test = session.get(
                url="https://banner9-registration.kfupm.edu.sa/StudentRegistrationSsb/ssb/registrationHistory/reset?term=%s"
                % term
            )
            print(test.text)
        except ConnectionError:
            if interface == "cli":
                print_one_color_text(
                    text_string="! Sorry, you currently don't have internet connection! the script will recheck in 10 seconds.",
                    text_color=AnsiColor.RED,
                )
                progress_bar(total_time=10)
