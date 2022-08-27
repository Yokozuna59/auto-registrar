from threading import Thread

from asyncio import get_event_loop
from vlc import MediaPlayer

import auto_registrar.config as config
from auto_registrar.tui.questions import Questions
from auto_registrar.tui.colored_text import print_more_color_text, print_one_color_text
from auto_registrar.tui.ansi import AnsiColor, AnsiCursor, AnsiErase, AnsiStyle
from auto_registrar.universities.kfupm.registrar import KFUPM_registrar
from auto_registrar.universities.kfupm.banner9 import KFUPM_banner9

CLASS_TYPE_COLORS = {
    "COP": "\x1b[48;2;92;148;13m",
    "DIS": "\x1b[48;2;201;42;42m",
    "EXP": "\x1b[48;2;201;42;42m",
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
}


def playsounds(sound_path: str):
    sound_file = MediaPlayer(sound_path)
    sound_file.play()


class KFUPM:
    def ask_for_configs(config_file: dict) -> dict:
        """
        Ask user 5 questinos to configurate.\n
        Return answers as `dict` type.
        """

        default_banner = Questions.dict_question(
            question="Select default banner for registration",
            choices={"Banner 9": 9},  # "Banner 8": 8}
        )
        config_file["banner"] = default_banner

        default_browser = Questions.dict_question(
            question="Select default browser",
            choices={"Chrome": "chromedriver"},  # "Firefox": "geckodriver"},
        )
        config_file["browser"] = default_browser

        default_delay = Questions.dict_question(
            question="Select default time delay between refreshes",
            choices={
                "10 second": 10,
                "20 Second": 20,
                "30 Second": 30,
                "60 Second": 60,
            },
        )
        config_file["delay"] = default_delay

        default_interface = Questions.dict_question(
            question="Select default user interface",
            choices={
                "Command-line interface (CLI)": "cli"
                # "Graphical user interface (GUI)": "gui",
            },
        )
        config_file["interface"] = default_interface

        username = Questions.str_questoin(question="Enter your student ID with `S`")
        config_file["username"] = username

        passcode = config.ask_and_write_passcode(
            configs_file=config_file, ask_for_passcode=True
        )

        config_file["configured"] = True
        config.write_config_file(configs_file=config_file)

        config_file["passcode"] = passcode

        return config_file

    def get_term_and_departments(interface: str) -> tuple:
        """
        Do a get request by `url` and ask user to select a term and department.\n
        return the user answer as `list` type.
        """

        term, departments = KFUPM_registrar.get_registrar_terms_and_departments(
            interface=interface
        )

        return term, departments

    def get_search_filter(interface: str, term: str, registration: bool) -> dict:
        """
        Ask user for what he want to search by each refresh.\n
        return answers as `dict` type.
        """

        min_crn = (int(term[-2])) * 10000
        max_crn = (int(term[-2]) + 1) * 10000 - 1

        filter_dictionary = {}
        if interface == "cli":
            if registration:
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
            else:
                alarm_answer = Questions.bool_question(
                    question="Do you want to get notified if a section/sections is/are open",
                    default=True,
                )
                filter_dictionary["alarm"] = alarm_answer
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
                    for index in search_by:
                        if index == "Section/Sections":
                            finished = False
                            while not finished:
                                sections_list = []
                                sections_str = Questions.str_questoin(
                                    question="Enter Section/Sections you want to check each refresh"
                                )

                                for section in sections_str.strip().split(" "):
                                    if section.isdigit():
                                        sections_list.append("%02d" % int(section))
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
                        elif index == "Activity/Activities":
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
                        elif index == "CRN/CRNs":
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
                        elif index == "Course/Courses Name":
                            correct_answer = False
                            while not correct_answer:
                                course_names_list = []
                                courses_names_str = Questions.str_questoin(
                                    question="Enter Course/Courses Name you want to check each refresh"
                                )
                                for index, element in enumerate(
                                    courses_names_str.strip().split(" ")
                                ):
                                    if ((element.isalpha()) and (index % 2 == 1)) or (
                                        (element.isdigit()) and (index % 2 == 0)
                                    ):
                                        print_more_color_text(
                                            "! Sorry, your reply was invalid:",
                                            AnsiColor.LIGHT_RED,
                                            '"' + element + '"',
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
                            filter_dictionary["course_name"] = course_names_list
                        elif index == "Instructor/Instructors":
                            print_one_color_text(
                                text_string="! Sorry, Currently the instructors filter is not supported!",
                                text_color=AnsiColor.RED,
                            )
                            # TODO: edit instructor chioce
                            #     colorful_text(text_string="e.g. ABDULRAHMAN AL-ARFAJ; MOHAMMAD SIDDIQUI", text_color=AnsiEscapeCodes.BRIGHT_CYAN)
                            #     instructors_list = Questions.str_questoin("Enter Instructor/Instructor you want to check each refresh (type the full name of instructor, each instructor separate with ;)")
                            #     filter_dictionary["instructor_name"] = instructors_list.split(";")
                        elif index == "Day/Days":
                            # TODO: edit day chioce
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
                        elif index == "Time/Times":
                            # TODO: edit time choice
                            print_one_color_text(
                                text_string="! Sorry, Currently the time filter is not supported!",
                                text_color=AnsiColor.RED,
                            )
                            #     colorful_text(text_string="e.g. 0800-1050 1300-1350", text_color=cli_colors.BRIGHT_CYAN)
                            #     times_str = Questions.str_questoin("Enter Time/Times you want to check each refresh")
                            #     filter_dictionary["course_number"] = times_str.split(" ")
                        elif index == "Building/Buildings":
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

                            filter_dictionary["building"] = buildings_list
                        elif index == "Status/Statuses":
                            status_list = Questions.mcq_list_question(
                                question="Select status of course/courses",
                                choices=["Open", "Wait list"],
                            )
                            if status_list != 2:
                                filter_dictionary["status"] = status_list[0]
                        elif index == "Gender":
                            genders_list = Questions.mcq_dict_question(
                                question="Select the gender of course/courses meant to have",
                                choices={"Male": "M", "Female": "F"},
                            )
                            if genders_list != 2:
                                filter_dictionary["gender"] = genders_list[0]

        filter_dictionary["registrar"] = registration
        return filter_dictionary

    def get_courses(term: str, departments: list, interface: str) -> list:
        loop = get_event_loop()
        courses = loop.run_until_complete(
            KFUPM_registrar.get_registrar_coures(
                term=term, departments=departments, interface=interface
            )
        )

        return courses

    def check_for_changes(
        courses_strucured: list, search_filter: dict, interface: str, alarm_path: str
    ) -> bool:
        """
        Checks if there is available seats in courses.\n
        return `bool` type.
        """

        max_lengths = {}
        for element in courses_strucured:
            for key, value in element.items():
                max_lengths[key] = max(max_lengths.get(key, 0), len(str(value)))

        course_name_length = max_lengths["course_name"] + max_lengths["section"] + 1
        course_type_length = max_lengths["class_type"]
        course_available_seats = max_lengths["available_seats"]
        course_waiting_list = max_lengths["waiting_list_count"]

        if search_filter == None:
            if interface == "cli":
                for index, element in enumerate(courses_strucured):
                    crn = element["crn"]
                    course_name = element["course_name"]
                    section = element["section"]
                    available_seats = element["available_seats"]
                    waiting_list_count = element["waiting_list_count"]
                    class_type = element["class_type"]

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
            if interface == "cli":
                # TODO: use search_filter in efficient way
                alarm_filter = search_filter.copy().pop("alarm")
                register = search_filter.copy().pop("registrar")

                for index in search_filter:
                    if index == "section":
                        courses_strucured = list(
                            filter(
                                lambda x: x["section"] in search_filter["section"],
                                courses_strucured,
                            )
                        )
                    elif index == "activity":
                        courses_strucured = list(
                            filter(
                                lambda x: x["class_type"] in search_filter["activity"],
                                courses_strucured,
                            )
                        )
                    elif index == "crn":
                        courses_strucured = list(
                            filter(
                                lambda x: x["crn"] in search_filter["crn"],
                                courses_strucured,
                            )
                        )
                    elif index == "course_name":
                        courses_strucured = list(
                            filter(
                                lambda x: x["course_name"]
                                in search_filter["course_name"],
                                courses_strucured,
                            )
                        )
                    elif index == "instructor_name":
                        print_one_color_text(
                            text_string="! Sorry, Currently the instructors filter is not supported!",
                            text_color=AnsiColor.RED,
                        )
                        # TODO: edit instructor name
                    elif index == "class_days":
                        print_one_color_text(
                            text_string="! Sorry, Currently the day filter is not supported!",
                            text_color=AnsiColor.RED,
                        )
                        # TODO: edit day choice
                    elif index == "time":
                        print_one_color_text(
                            text_string="! Sorry, Currently the time filter is not supported!",
                            text_color=AnsiColor.RED,
                        )
                        # TODO: edit time chioce
                    elif index == "building":
                        courses_strucured = list(
                            filter(
                                lambda x: x["building"] in search_filter["building"],
                                courses_strucured,
                            )
                        )
                    elif index == "status":
                        if search_filter["status"] == "Open":
                            courses_strucured = list(
                                filter(
                                    lambda x: x["available_seats"] > 0,
                                    courses_strucured,
                                )
                            )
                        else:
                            courses_strucured = list(
                                filter(
                                    lambda x: x["waiting_list_count"] > 0
                                    and x["available_seats"] <= 0,
                                    courses_strucured,
                                )
                            )
                    elif index == "gender":
                        courses_strucured = list(
                            filter(
                                lambda x: "F" in x["section"]
                                if search_filter["gender"] == "F"
                                else "F" not in x["section"],
                                courses_strucured,
                            )
                        )

                if register:
                    pass
                else:
                    alarm_condition = False
                    for index, element in enumerate(courses_strucured):
                        alarm_condition = True

                        crn = element["crn"]
                        course_name = element["course_name"]
                        section = element["section"]
                        available_seats = element["available_seats"]
                        waiting_list_count = element["waiting_list_count"]
                        class_type = element["class_type"]

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
                    if alarm_condition and alarm_filter:
                        thread = Thread(target=playsounds, args=(alarm_path,))
                        thread.start()
        return False

    def get_courses_structured(courses_requested: list, source: str) -> list:
        if source == "registrar":
            structured_courses = KFUPM_registrar.get_registrar_courses_structured(
                courses_requested=courses_requested
            )
        else:
            structured_courses = KFUPM_banner9.get_banner9_courses_structured(
                courses_requested=courses_requested
            )

        return structured_courses
