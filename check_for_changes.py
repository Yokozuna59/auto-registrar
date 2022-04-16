# import loads to load the json data
from json import loads

from colorful_terminal import color_print, tcolor

def check_for_change(content, search_user_input, driver_path):
    content_json = loads(str(content))["data"]

    if (search_user_input != None):
        found_elements = filter(lambda j: j["crn"] in search_user_input["CRN"],  content_json)
        id2dict = dict((d['crn'], d) for d in found_elements)
        try:
            found_elements_sorted = [id2dict[x] for x in search_user_input["CRN"]]
            for element in found_elements_sorted:
                if element['available_seats'] and element['waiting_list_count']:
                    print(f"available_seats CRN: {element['crn']}")
                elif element['waiting_list_count']:
                    print(f"waiting_list CRN: {element['crn']}")
        except KeyError:
            # one or more CRNs are not in the department and term specified
            pass
    else:
        for i in content_json:
            crn = i["crn"]
            course_name = i["course_number"]
            section = i["section_number"]
            available_seats = i["available_seats"]
            waiting_list_count = i["waiting_list_count"]
            class_type = i["class_type"]

            if (available_seats > 0):
                color_print(f"[+] - {course_name}-{section},", tcolor.OKGREEN, " ")
                color_print(f"Type: {class_type}", tcolor.LEC if class_type == "LEC" else tcolor.LAB if class_type == "LAB" else tcolor.RES, ", ")
                color_print(f"Available Seats: {available_seats}, Waiting List: {waiting_list_count}", tcolor.OKGREEN, ", ")
                color_print(f"CRN: {crn}", tcolor.HEADER)
            elif (waiting_list_count > 0)   :
                color_print(f"[-] - {course_name}-{section},", tcolor.WARNING, " ")
                color_print(f"Type: {class_type}",  tcolor.LEC if class_type == "LEC" else tcolor.LAB if class_type == "LAB" else tcolor.RES, ", ")
                color_print(f"Available Seats: {available_seats}, Waiting List: {waiting_list_count}", tcolor.WARNING, ", ")
                color_print(f"CRN: {crn}", tcolor.HEADER)