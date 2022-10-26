from asyncio import gather, get_event_loop
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from requests import get
from requests.exceptions import ConnectionError, Timeout
from nest_asyncio import apply
from warnings import filterwarnings

from auto_registrar.tui.ansi import AnsiColor
from auto_registrar.tui.bar import progress_bar
from auto_registrar.tui.colored_text import print_one_color_text
from auto_registrar.tui.questions import Questions
from auto_registrar.universities.kfupm.banner9 import KFUPM_banner9


filterwarnings("ignore", category=DeprecationWarning)


class KFUPM_registrar:
    def get_registrar_terms_and_departments(interface: str) -> tuple:
        finished = False
        banner9 = False
        url = "https://registrar.kfupm.edu.sa/courses-classes/course-offering1/"

        while not finished:
            try:
                response = get(url=url, timeout=10).text
                if "Under Maintenance" in response:
                    banner9 = True
                finished = True
            except ConnectionError:
                if interface == "cli":
                    print_one_color_text(
                        text_string="! Sorry, you currently don't have internet connection! the script will recheck in 10 seconds.",
                        text_color=AnsiColor.RED,
                    )
                    progress_bar(10)
            except Timeout:
                banner9 = True
                finished = True

        if banner9:
            term, departments = KFUPM_banner9.get_banner9_terms_and_departments(
                interface=interface
            )
        else:
            soup = BeautifulSoup(markup=response, features="html.parser")
            term = KFUPM_registrar.get_registrar_terms(soup=soup)
            departments = KFUPM_registrar.get_registrar_departments(soup=soup)

        return term, departments

    def get_registrar_terms(soup: BeautifulSoup) -> str:
        terms_element = soup.find(id="course_term_code")
        options = terms_element.find_all("option")[1:]

        dict_elements = {}
        for option in options:
            dict_elements[option.text] = option["value"]

        term = Questions.dict_question(
            question="Select the term has/have the course/courses",
            choices=dict(
                sorted(dict_elements.items(), key=lambda x: x[1], reverse=True)
            ),
        )
        return term

    def get_registrar_departments(soup: BeautifulSoup) -> list:
        departments_element = soup.find(id="course_dept_code")
        options = departments_element.find_all("option")[1:]

        dict_elements = {}
        for option in options:
            dict_elements[option.text] = option["value"]

        departments = Questions.mcq_dict_question(
            question="Select the department has/have the course/courses",
            choices=dict_elements,
        )
        return departments

    async def get_registrar_coures(
        term: str, departments: list, interface: str
    ) -> list:
        courses = []
        urls = [
            "https://registrar.kfupm.edu.sa/api/course-offering?term_code=%s&department_code=%s"
            % (term, department)
            for department in departments
        ]

        banner9 = False
        request_finished = False
        with ThreadPoolExecutor() as executor:
            loop = get_event_loop()
            while not request_finished:
                try:
                    futures = [
                        loop.run_in_executor(executor, get, url, 10) for url in urls
                    ]
                    for response in await gather(*futures):
                        if (response.status_code == 200) and ("Under Maintenance" not in response.text) and (
                            response.json()["data"] != None
                        ):
                            courses += response.json()["data"]
                        else:
                            banner9 = True
                            request_finished = True
                            apply()
                            break
                    request_finished = True
                except ConnectionError:
                    if interface == "cli":
                        print_one_color_text(
                            text_string="! Sorry, you currently don't have internet connection! the script will recheck in 10 seconds.",
                            text_color=AnsiColor.RED,
                        )
                        progress_bar(10)
                except Timeout:
                    banner9 = True
                    request_finished = True
                    apply()

            if banner9:
                loop = get_event_loop()
                courses_structured = loop.run_until_complete(
                    KFUPM_banner9.get_banner9_courses(
                        term=term, departments=departments, interface=interface
                    )
                )
            else:
                courses_structured = KFUPM_registrar.get_registrar_courses_structured(
                    courses_requested=courses
                )

            return courses_structured

    def get_registrar_courses_structured(courses_requested: list) -> list:
        found_elements = list(
            filter(
                lambda x: x["available_seats"] > 0 or x["waiting_list_count"] > 0,
                courses_requested,
            )
        )

        courses_structured = []
        for element in found_elements:
            course_dict = {}
            course_dict["crn"] = element["crn"]
            if "course_number" in element:
                course_dict["course_name"] = element["course_number"].replace(" ", "")
            else:
                course_dict["course_name"] = element["course_name"].replace(" ", "")
            if "section_number" in element:
                course_dict["section"] = element["section_number"]
            else:
                course_dict["section"] = element["section"]
            course_dict["available_seats"] = element["available_seats"]
            course_dict["waiting_list_count"] = element["waiting_list_count"]
            course_dict["class_type"] = element["class_type"]
            course_dict["class_days"] = ["class_days"]
            course_dict["start_time"] = element["start_time"]
            course_dict["end_time"] = element["end_time"]
            course_dict["building"] = element["building"]
            course_dict["room"] = element["room"]
            course_dict["instructor_name"] = element["instructor_name"]

            courses_structured.append(course_dict)
        return courses_structured
