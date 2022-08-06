from json import loads
from sys import exit

from requests import get, session, post
from requests.exceptions import ConnectionError, RequestException

import auto_registrar.config as config
from auto_registrar.tui.questions import Questions
from auto_registrar.tui.colored_text import print_more_color_text, print_one_color_text
from auto_registrar.tui.ansi import AnsiColor, AnsiCursor, AnsiErase, AnsiStyle
from auto_registrar.tui.bar import progress_bar

CLASS_TYPE_COLORS = {
    "COP": "\x1b[48;2;92;148;13m",
    "DIS": "\x1b[48;2;201;42;42m",
    "FLD": "\x1b[48;2;33;37;41m",
    "IND": "\x1b[48;2;33;37;41m",
    "LAB": "\x1b[48;2;95;61;196m",
    "LEC": "\x1b[48;2;24;100;171m",
    "LRC": "\x1b[48;2;24;100;171m",
    "LLB": "\x1b[48;2;33;37;41m",
    "LPJ": "\x1b[48;2;33;37;41m",
    "MR": "\x1b[48;2;33;37;41m",
    "PRJ": "\x1b[48;2;217;72;15m",
    "REC": "\x1b[48;2;166,30,77m",
    "RES": "\x1b[48;2;201;42;42m",
    "SEM": "\x1b[48;2;8;127;91m",
    "SLB": "\x1b[48;2;33;37;41m",
    "ST": "\x1b[48;2;33;37;41m",
    "STD": "\x1b[48;2;33;37;41m",
    "THS": "\x1b[48;2;54;79;199m",
    "EXP": "\x1b[48;2;201;42;42m"
}


class KFUPM:
    def do_configs(configs_file: dict) -> dict:
        """
        Ask user 5 diffrent questinos to configurate.\n
        If he answered the question, return them as `dict` type.
        """

        default_banner = Questions.dict_question(
            question="Select default banner for registration",
            choices={"Banner 9": 9},  # "Banner 8": 8}
        )
        configs_file["banner"] = default_banner

        default_browser = Questions.dict_question(
            question="Select default browser",
            choices={"Chrome": "chromedriver"},  # "Firefox": "geckodriver"},
        )
        configs_file["browser"] = default_browser

        default_delay = Questions.dict_question(
            question="Select default time delay between refreshes",
            choices={
                "10 second": 10,
                "20 Second": 20,
                "30 Second": 30,
                "60 Second": 60,
            },
        )
        configs_file["delay"] = default_delay

        default_interface = Questions.dict_question(
            question="Select default user interface",
            choices={
                "Command-line interface (CLI)": "cli"
                # "Graphical user interface (GUI)": "gui",
            },
        )
        configs_file["interface"] = default_interface

        username = Questions.str_questoin(question="Enter your student ID with `S`")
        configs_file["username"] = username

        passcode = config.ask_for_passcode(configs_file=configs_file)

        configs_file["configured"] = True
        config.write_config_file(configs_file=configs_file)

        configs_file["passcode"] = passcode

        return configs_file

    def get_term_and_department(interface: str) -> tuple:
        """
        Do a get request by `url` and ask user to select a term and department.\n
        return the user answer as `list` type.
        """

        term = KFUPM.get_terms(interface=interface)
        department = KFUPM.get_departments(interface=interface, term=term)

        return (term, department)

    def get_terms(interface: str) -> str:
        url = "https://banner9-registration.kfupm.edu.sa/StudentRegistrationSsb/ssb/classSearch/getTerms?searchTerm=&offset=1&max=1000"

        request_done = False
        while not request_done:
            try:
                response = get(url=url).content
                loaded_response = loads(s=response)

                index = 0
                terms_number = 0
                terms_dict = {}
                finished = False

                while (not finished) and (index < len(loaded_response) - 1):
                    description = loaded_response[index]["description"]
                    term_code = loaded_response[index]["code"]

                    if not ("(View Only)" in description):
                        terms_dict[description.replace("amp;", "")] = term_code
                        terms_number += 1
                    else:
                        finished = True
                    index += 1
                if terms_number == 0:
                    print_one_color_text(
                        text_string="! Sorry, there is no terms available for registration.",
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
            except RequestException:
                if interface == "cli":
                    print_one_color_text(
                        text_string="! Sorry, the website isn't working currently! the script will recheck in 60 seconds",
                        text_color=AnsiColor.RED,
                    )
                    progress_bar(total_time=60)

            if interface == "cli":
                term_choice = Questions.dict_question(
                    question=("Select the term has/have the course/courses"),
                    choices=terms_dict,
                )
        return term_choice

    def get_departments(interface: str, term: str) -> str:
        url = "https://banner9-registration.kfupm.edu.sa/StudentRegistrationSsb/ssb/classSearch/get_subject?searchTerm=&term=&offset=1&max=1000".replace(
            "term=", f"term={term}"
        )

        request_done = False
        while not request_done:
            try:
                response = get(url=url).content
                loaded_response = loads(s=response)

                index = 0
                departments_number = 0
                departments_dict = {}

                while index < len(loaded_response) - 1:
                    description = loaded_response[index]["description"]
                    department_code = loaded_response[index]["code"]
                    departments_dict[description.replace("amp;", "")] = department_code
                    departments_number += 1
                    index += 1

                if departments_number == 0:
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
            except RequestException:
                if interface == "cli":
                    print_one_color_text(
                        text_string="! Sorry, the website isn't working currently! the script will recheck in 60 seconds",
                        text_color=AnsiColor.RED,
                    )
                    progress_bar(total_time=60)

            if interface == "cli":
                department_choices = Questions.mcq_dict_question(
                    question=("Select the department has/have the course/courses"),
                    choices=departments_dict,
                )
        return department_choices

    def get_search_filter(interface: str, term: str, driver_path: str = None) -> dict:
        """
        Ask user for what he want to search by each refresh.\n
        return answer as `dict` type.
        """

        min_crn = (int(term[-2])) * 10000
        max_crn = (int(term[-2]) + 1) * 10000 - 1

        filter_dictionary = {}
        if interface == "cli":
            if driver_path != None:
                registrar_answer = Questions.bool_question(
                    question="Do you want to registrar course/courses", default=False
                )

                if registrar_answer == True:
                    finished = False
                    while not finished:
                        crns_list = []
                        crns_str = Questions.str_questoin(
                            question="Enter CRN/CRNs you want to registrar (separated by spaces)"
                        )
                        for crn in crns_str.strip().split(" "):
                            if crn.isdigit():
                                if min_crn <= int(crn) <= max_crn:
                                    crns_list.append(crn)
                                    finished = True
                                else:
                                    print_more_color_text(
                                        "! Sorry, your reply was invalid:",
                                        AnsiColor.LIGHT_RED,
                                        '"' + crn + '"',
                                        AnsiStyle.BOLD,
                                        "is out of range answer, please try again.",
                                        AnsiColor.LIGHT_RED,
                                    )
                                    finished = False
                                    break
                            else:
                                print_more_color_text(
                                    "! Sorry, your reply was invalid:",
                                    AnsiColor.LIGHT_RED,
                                    '"' + crn + '"',
                                    AnsiStyle.BOLD,
                                    "is not a valid answer, please try again.",
                                    AnsiColor.LIGHT_RED,
                                )
                                finished = False
                                break

                    filter_dictionary["registrar"] = True
                    filter_dictionary["crn"] = crns_list
                    return filter_dictionary

            search_by = Questions.mcq_list_question(
                question="What filters you wany to check each refresh",
                choices=[
                    "Check `ALL` courses of the department",
                    "Section/Sections",
                    "Activity/Activities",
                    "CRN/CRNs",
                    "Course/Courses Name",
                    "Instructor/Instructors",
                    "Day/Days",
                    "Time/Times",
                    "Building/Buildings",
                    "Status/Statuses",
                    "Gender",
                ],
            )
            if "Check `ALL` courses of the department" in search_by:
                return None
            else:
                for i in search_by:
                    if i == "Section/Sections":
                        finished = False
                        while not finished:
                            sections_list = []
                            sections_str = Questions.str_questoin(
                                question="Enter Section/Sections you want to check each refresh"
                            )

                            for section in sections_str.strip().split(" "):
                                if section.isdigit():
                                    sections_list.append("%02s" % section)
                                    finished = True
                                else:
                                    print_more_color_text(
                                        "! Sorry, your reply was invalid:",
                                        AnsiColor.LIGHT_RED,
                                        '"' + section + '"',
                                        AnsiStyle.BOLD,
                                        "is not a valid answer, please try again.",
                                        AnsiColor.LIGHT_RED,
                                    )
                        filter_dictionary["section"] = sections_list
                    elif i == "Activity/Activities":
                        activities_str = Questions.mcq_list_question(
                            question="Select type of activity you want to check each refresh",
                            choices=[
                                "COP",
                                "DIS",
                                "FLD",
                                "IND",
                                "LAB",
                                "LLB",
                                "LEC",
                                "MR",
                                "PRJ",
                                "RES",
                                "SEM",
                                "SLB",
                                "ST",
                                "STD",
                                "THS",
                            ],
                        )
                        if len(activities_str) != 15:
                            filter_dictionary["activity"] = activities_str
                    elif i == "CRN/CRNs":
                        # TODO: repeated function
                        finished = False
                        while not finished:
                            crns_list = []
                            crns_str = Questions.str_questoin(
                                question="Enter CRN/CRNs you want to registrar (separated by spaces)"
                            )
                            for crn in crns_str.strip().split(" "):
                                if crn.isdigit():
                                    if min_crn <= int(crn) <= max_crn:
                                        crns_list.append(crn)
                                        finished = True
                                    else:
                                        print_more_color_text(
                                            "! Sorry, your reply was invalid:",
                                            AnsiColor.LIGHT_RED,
                                            '"' + crn + '"',
                                            AnsiStyle.BOLD,
                                            "is out of range answer, please try again.",
                                            AnsiColor.LIGHT_RED,
                                        )
                                else:
                                    print_more_color_text(
                                        "! Sorry, your reply was invalid:",
                                        AnsiColor.LIGHT_RED,
                                        '"' + crn + '"',
                                        AnsiStyle.BOLD,
                                        "is not a valid answer, please try again.",
                                        AnsiColor.LIGHT_RED,
                                    )

                        filter_dictionary["crn"] = crns_list
                    elif i == "Course/Courses Name":
                        correct_answer = False
                        while not correct_answer:
                            course_names_list = []
                            courses_names_str = Questions.str_questoin(
                                question="Enter Course/Courses Name you want to check each refresh"
                            )
                            for index, element in enumerate(
                                courses_names_str.split(" ")
                            ):
                                if ((element.isalpha()) and (index % 2 == 1)) or (
                                    (element.isdigit()) and (index % 2 == 0)
                                ):
                                    print_more_color_text(
                                        "! Sorry, your reply was invalid:",
                                        AnsiColor.LIGHT_RED,
                                        '"' + crn + '"',
                                        AnsiStyle.BOLD,
                                        "is not a valid answer, please try again.",
                                        AnsiColor.LIGHT_RED,
                                    )
                                    break
                                else:
                                    if (element.isalpha()) and (index % 2 == 0):
                                        course = element
                                        index += 1
                                    elif (element.isdigit()) and (index % 2 == 1):
                                        course += element
                                        course_names_list.append(course.upper())
                                        index += 1
                                    elif element.isalnum():
                                        course_names_list.append(element.upper())
                                        index += 2
                                    correct_answer = True

                            AnsiCursor.restore_position()
                            AnsiErase.erase_line_to_end()
                            print_one_color_text(
                                text_string=" ".join(course_names_list).upper(),
                                text_color=AnsiColor.LIGHT_BLUE,
                            )
                        filter_dictionary["course_number"] = course_names_list
                    elif i == "Instructor/Instructors":
                        print_one_color_text(
                            text_string="Currently the instructors filter is not supported!",
                            text_color=AnsiColor.RED,
                        )
                    # TODO: edit instructor chioce
                    #     colorful_text(text_string="e.g. ABDULRAHMAN AL-ARFAJ; MOHAMMAD SIDDIQUI", text_color=AnsiEscapeCodes.BRIGHT_CYAN)
                    #     instructors_list = Questions.str_questoin("Enter Instructor/Instructor you want to check each refresh (type the full name of instructor, each instructor separate with ;)")
                    #     filter_dictionary["instructor_name"] = instructors_list.split(";")
                    elif i == "Day/Days":
                        days_list = Questions.mcq_dict_question(
                            question="Select the Day/Days Course/Courses occurs",
                            choices={
                                "U, Sunday": "U",
                                "M, Monday": "M",
                                "T, Tuesday": "T",
                                "W, Wednesday": "W",
                                "R, Thursday": "R",
                                "F, Friday": "F",
                                "S, Saturday": "S",
                            },
                        )
                        if len(days_list) != 7:
                            filter_dictionary["class_days"] = days_list
                    elif i == "Time/Times":
                        print_one_color_text(
                            text_string="Currently the time filter is not supported!",
                            text_color=AnsiColor.RED,
                        )
                    # TODO edit time chioce
                    #     colorful_text(text_string="e.g. 0800-1050 1300-1350", text_color=cli_colors.BRIGHT_CYAN)
                    #     times_str = Questions.str_questoin("Enter Time/Times you want to check each refresh")
                    #     filter_dictionary["course_number"] = times_str.split(" ")
                    elif i == "Building/Buildings":
                        correct_answer = False
                        while not correct_answer:
                            buildings_list = []
                            buildings_str = Questions.str_questoin(
                                question="Enter Building/Buildings you want to check each refresh"
                            )
                            for building in buildings_str.strip().split(" "):
                                if building.isdigit():
                                    buildings_list.append(building)
                                    correct_answer = True
                                else:
                                    print_more_color_text(
                                        "! Sorry, your reply was invalid:",
                                        AnsiColor.LIGHT_RED,
                                        '"' + crn + '"',
                                        AnsiStyle.BOLD,
                                        "is not a valid answer, please try again.",
                                        AnsiColor.LIGHT_RED,
                                    )
                                    break

                        filter_dictionary["building"] = buildings_list
                    elif i == "Status/Statuses":
                        status_list = Questions.mcq_list_question(
                            question="Select status of course/courses",
                            choices=["Open", "Wait list"],
                        )
                        if status_list != 2:
                            filter_dictionary["status"] = status_list[0]
                    elif i == "Gender":
                        genders_list = Questions.mcq_dict_question(
                            question="Select the gender of course/courses meant to have",
                            choices={"Male": "M", "Female": "F"},
                        )
                        if genders_list != 2:
                            filter_dictionary["gender"] = genders_list[0]
            filter_dictionary["registrar"] = False
        return filter_dictionary

    def get_banner9_courses(term: str, departments: list) -> list:
        """
        Do a get and post requests to get content.\n
        Return the content as a `dict` type.
        """

        session_client = session()

        request_cookies = session_client.get(
            url="https://banner9-registration.kfupm.edu.sa/StudentRegistrationSsb/ssb/term/termSelection?mode=search"
        )
        session_id = dict(request_cookies.cookies)["JSESSIONID"]
        post(
            url="https://banner9-registration.kfupm.edu.sa/StudentRegistrationSsb/ssb/term/search?mode=search",
            cookies={"JSESSIONID": session_id},
            data={"term": term},
        )
        departments = ",".join(departments)

        courses = []
        page_off_set = 0
        number_of_pages = 0
        while page_off_set <= number_of_pages:
            url = f"https://banner9-registration.kfupm.edu.sa/StudentRegistrationSsb/ssb/searchResults/searchResults?txt_term={term}&txt_subject={departments}&pageOffset={page_off_set*500}&pageMaxSize=500"
            response = get(
                url=url,
                cookies={"JSESSIONID": session_id},
            )
            loaded_response = loads(s=response.text)
            courses += loaded_response["data"]
            page_off_set += 1
            if number_of_pages == 0:
                number_of_pages = int(loaded_response["sectionsFetchedCount"] / 500)
        return courses

    def check_for_changes(content: list, searsh_filter: dict, configs_file: str) -> bool:
        """
        Checks if there is available seats in courses.\n
        after checking, return `bool` type.
        """

        if searsh_filter == None:
            course_name_length = 0
            course_type_length = 0
            course_available_seats = 0
            course_waiting_list = 0

            found_elements = list(
                filter(
                    lambda x: int(x["seatsAvailable"]) > 0
                    or int(x["waitAvailable"]) > 0,
                    content,
                )
            )
            if configs_file["interface"] == "cli":
                for element in found_elements:
                    crn = element["courseReferenceNumber"]
                    course_name = element["subjectCourse"].replace(" ", "")
                    section = element["sequenceNumber"]
                    available_seats = element["seatsAvailable"]
                    waiting_list_count = element["waitAvailable"]
                    class_type = element["meetingsFaculty"][0]["meetingTime"][
                        "meetingScheduleType"
                    ]

                    course_name_length = max(
                        len(f"{course_name}-{section}"), course_name_length
                    )
                    course_type_length = max(len(class_type), course_type_length)
                    course_available_seats = max(
                        len(str(available_seats)), course_available_seats
                    )
                    course_waiting_list = max(
                        len(str(waiting_list_count)), course_waiting_list
                    )

                for index, element in enumerate(found_elements):
                    crn = element["courseReferenceNumber"]
                    course_name = element["subjectCourse"].replace(" ", "")
                    section = element["sequenceNumber"]
                    available_seats = element["seatsAvailable"]
                    waiting_list_count = element["waitAvailable"]
                    class_type = element["meetingsFaculty"][0]["meetingTime"][
                        "meetingScheduleType"
                    ]

                    if available_seats > 0:
                        color = AnsiColor.LIGHT_GREEN
                        sign = "+"
                    elif waiting_list_count > 0:
                        color = AnsiColor.LIGHT_YELLOW
                        sign = "-"

                    full_course_name = (
                        f"%{-course_name_length}s" % f"{course_name}-{section}"
                    )
                    full_course_type = f"%{-course_type_length}s" % class_type
                    full_course_available_seats = (
                        f"%{-course_available_seats}s" % available_seats
                    )
                    full_course_waiting_list = (
                        f"%{-course_waiting_list}s" % waiting_list_count
                    )

                    print_more_color_text(
                        f"[{sign}] - {full_course_name}, Type:",
                        color,
                        full_course_type,
                        CLASS_TYPE_COLORS[class_type],
                        f"Available Seats: {full_course_available_seats}, Waiting List: {full_course_waiting_list}, CRN:",
                        color,
                        crn,
                        AnsiColor.LIGHT_BLUE
                        if index % 2 == 0
                        else AnsiColor.LIGHT_MAGENTA,
                    )
        else:
            found_elements = filter(
                lambda x: int(x["seatsAvailable"]) > 0 or int(x["waitAvailable"]) > 0,
                content,
            )
            if configs_file["interface"] == "cli":
                for i in searsh_filter:
                    if i == "section":
                        found_elements = list(
                            filter(
                                lambda x: x["sequenceNumber"]
                                in searsh_filter["section"],
                                found_elements,
                            )
                        )
                    elif i == "activity":
                        found_elements = list(
                            filter(
                                lambda x: x["meetingsFaculty"][0]["meetingTime"][
                                    "meetingScheduleType"
                                ]
                                in searsh_filter["activity"],
                                found_elements,
                            )
                        )
                    elif i == "crn":
                        found_elements = list(
                            filter(
                                lambda x: x["courseReferenceNumber"]
                                in searsh_filter["crn"],
                                found_elements,
                            )
                        )
                    elif i == "course_number":
                        found_elements = list(
                            filter(
                                lambda x: x["subjectCourse"].replace(" ", "")
                                in searsh_filter["course_number"],
                                found_elements,
                            )
                        )
                    elif i == "instructor_name":
                        found_elements = list(
                            filter(
                                lambda x: x["faculty"][0]["displayName"]
                                in searsh_filter["instructor_name"],
                                found_elements,
                            )
                        )
                    # TODO: edit day choice
                    # elif (i == "class_days"):
                    #     found_elements = list(filter(lambda x: x["class_days"] in search_input["class_days"], found_elements))
                    # TODO: edit time chioce
                    # elif (i == "time"):
                    #     (filter(lambda x: x["building"] in search_user_input["building"], found_elements))
                    elif i == "building":
                        found_elements = list(
                            filter(
                                lambda x: x["meetingsFaculty"][0]["meetingTime"][
                                    "building"
                                ]
                                in searsh_filter["building"],
                                found_elements,
                            )
                        )
                    elif i == "status":
                        if searsh_filter["status"] == "Open":
                            found_elements = list(
                                filter(
                                    lambda x: x["seatsAvailable"] > 0, found_elements
                                )
                            )
                        else:
                            found_elements = list(
                                filter(
                                    lambda x: x["waitAvailable"] > 0
                                    and x["seatsAvailable"] <= 0,
                                    found_elements,
                                )
                            )
                    elif i == "gender":
                        found_elements = list(
                            filter(
                                lambda x: "F" in x["sequenceNumber"]
                                if searsh_filter["gender"] == "F"
                                else "F" not in x["section_number"],
                                found_elements,
                            )
                        )
                for element in found_elements:
                    crn = element["courseReferenceNumber"]
                    course_name = element["subjectCourse"].replace(" ", "")
                    section = element["sequenceNumber"]
                    available_seats = element["seatsAvailable"]
                    waiting_list_count = element["waitAvailable"]
                    class_type = element["meetingsFaculty"][0]["meetingTime"][
                        "meetingScheduleType"
                    ]

                    course_name_length = max(
                        len(f"{course_name}-{section}"), course_name_length
                    )
                    course_type_length = max(len(class_type), course_type_length)
                    course_available_seats = max(
                        len(str(available_seats)), course_available_seats
                    )
                    course_waiting_list = max(
                        len(str(waiting_list_count)), course_waiting_list
                    )

                for index, element in enumerate(found_elements):
                    crn = element["courseReferenceNumber"]
                    course_name = element["subjectCourse"].replace(" ", "")
                    section = element["sequenceNumber"]
                    available_seats = element["seatsAvailable"]
                    waiting_list_count = element["waitAvailable"]
                    class_type = element["meetingsFaculty"][0]["meetingTime"][
                        "meetingScheduleType"
                    ]

                    if available_seats > 0:
                        color = AnsiColor.LIGHT_GREEN
                        sign = "+"
                    elif waiting_list_count > 0:
                        color = AnsiColor.LIGHT_YELLOW
                        sign = "-"

                    full_course_name = (
                        f"%{-course_name_length}s" % f"{course_name}-{section}"
                    )
                    full_course_type = f"%{-course_type_length}s" % class_type
                    full_course_available_seats = (
                        f"%{-course_available_seats}s" % available_seats
                    )
                    full_course_waiting_list = (
                        f"%{-course_waiting_list}s" % waiting_list_count
                    )

                    print_more_color_text(
                        f"[{sign}] - {full_course_name}, Type:",
                        color,
                        full_course_type,
                        CLASS_TYPE_COLORS[class_type],
                        f"Available Seats: {full_course_available_seats}, Waiting List: {full_course_waiting_list}, CRN:",
                        color,
                        crn,
                        AnsiColor.LIGHT_BLUE
                        if index % 2 == 0
                        else AnsiColor.LIGHT_MAGENTA,
                    )
        return False
