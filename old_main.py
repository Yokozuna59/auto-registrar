import requests
from bs4 import BeautifulSoup
from delay import time_delay
import json
from colorful_terminal import *
from search import *
from search import *

def get_registrar_requests():
    registrar_request = requests.get("https://registrar.kfupm.edu.sa/courses-classes/course-offering/")
    status = registrar_request.status_code

    if (status != 200):
        request_not_200()
    else:
        return registrar_request.content


def request_not_200():
    color_print("[!] - The website isn't working for the time being, the script will check every 60s..", tcolor.FAIL)
    time_delay(60)
    get_registrar_requests()
    return True


def get_elements(text, content):
    soup = BeautifulSoup(content, "html.parser")
    if (text == "Term"):
        element_id = "course_term_code"
    else:
        element_id = "course_dept_code"

    element = soup.find(id=element_id)
    options = element.find_all("option")[1::]

    elements_list = []
    for option in options:
        elements_list.append(option.text)

    show_choices(elements_list, text, tcolor.OKBLUE, tcolor.OKCYAN)

    term = get_user_input(text, elements_list)

    return term


def show_choices(elements, text, color1, color2):
    if (text == "Department"):
        departments_short_name = departments_list()

    for index, element in enumerate(elements):
        if index % 2 == 0:
            if (text == "Term" or text == None):
                color_print(f"[{index + 1}] {element}", color1)
            elif (text == "Department"):
                print(f"\033[94m[{index + 1}]\033[0m \033[93m{departments_short_name[index]}\033[0m | \033[94m{element}\033[0m")
        else:
            if (text == "Term" or text == None):
                color_print(f"[{index + 1}] {element}", color2)
            elif (text == "Department"):
                print(f"\033[96m[{index + 1}]\033[0m \033[95m{departments_short_name[index]}\033[0m | \033[96m{element}\033[0m")


def departments_list():
    deps_code = ["ACFN", "AE", "ARE", "ARC", "MBA", "CHE", "CHEM", "CPR", "CE", "COE", "CEM", "CIE", "EE", "ELD", "ELI", "ERTH", "GS", "SE", "ICS", "ISOM", "IAS", "LS", "MGT", "MSE", "MATH", "ME", "CPG", "PETE", "PE", "PHYS", "PSE"]

    return deps_code


def get_user_input(text, lists):
    user_input = color_input("[*] - Enter number: ", tcolor.OKGREEN)

    if (len(lists) > 0 and len(lists) >= int(user_input)):
        if (text == "Term"):
            list_element = lists[int(user_input) - 1].replace("Term ", "")
        elif (text == "Department"):
            list_element = departments_list()[int(user_input) - 1]
        elif (text == None):
            pass
    else:
        print("You can't choose a number out of range!")
        return False

    return list_element


def get_time_input():
    elements_list = ["10s","20s", "30s", "60s"]

    show_choices(elements_list, None, tcolor.OKBLUE, tcolor.OKCYAN)
    user_input = int(color_input("[*] - Check every (enter number): ", tcolor.OKGREEN))

    if (user_input > 0 and user_input <= 4):
        if (user_input == 4):
            user_input *= 15
        else:
            user_input *= 10
    else:
        print("You can't choose a number out of range!")
        return False

    return user_input


def get_api_requests(term, department):
    api_request = requests.get(f"https://registrar.kfupm.edu.sa/api/course-offering?term_code=20{term}0&department_code={department}")
    status = api_request.status_code

    if (api_request.status_code != 200):
        request_not_200()
    else:
        data = json.loads(api_request.text)

        if (data["data"] == None):
            color_print("The API isn't working for the time being, the code will check for sections every 60s..", tcolor.FAIL)
            time_delay(60)
            get_api_requests(term, department)
            return True
        else:
            return data["data"]


def check_courses(data, refreash_time, search_input):
    for course in data:
        # if_statement(course, search_input)
        if (search_input != None):
            if (course["status"] == "Open"):
                color_print(f"[+] - {course['course_code']} is open!", tcolor.OKGREEN)
            else:
                color_print(f"[-] - {course['course_code']} is closed!", tcolor.FAIL)
        else:
            course_name = course["course_number"]
            section = course["section_number"]
            class_type = course["class_type"]
            crn = course["crn"]
            available_seats = course["available_seats"]
            waiting_list_count = course["waiting_list_count"]

            if ("F" in section):
                continue
            elif (course_name != "ICS 104"):
                continue

            if (available_seats > 0):
                color_print(f"[+] - {course_name}-{section},\033[0m \033Type: {class_type},\033[0m Available Seats: {available_seats}, Waiting List: {waiting_list_count}, {crn}", tcolor.OKGREEN)
            elif (waiting_list_count > 0)   :
                color_print(f"[-] - {course_name}-{section}, Type: {class_type}, Available Seats: {available_seats}, Waiting List: {waiting_list_count}, {crn}", tcolor.WARNING)

    time_delay(refreash_time)
    print()
    return True


# def if_statement(course, search_input):
#     print(search_input.keys())
#     if ():
#         pass


def main():
    content = get_registrar_requests()
    term = get_elements("Term", content)
    if (term == False):
        return False
    department = get_elements("Department", content)
    if (department == False):
        return False
    refreash_time = get_time_input()
    if (refreash_time == False):
        return False
    search_input = get_search_input()
    if (search_input == False):
        return False

    while True:
        data = get_api_requests(term, department)
        check_courses(data, refreash_time, search_input)

if __name__ == "__main__":
    main()