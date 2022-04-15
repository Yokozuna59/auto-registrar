# import loads to load the json data
from json import loads

from colorful_terminal import color_print, tcolor

def check_for_change(content, search_user_input):
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
        available_seats = filter(lambda element: (element["available_seats"] > 0) and (element["waiting_list_count"] > 0),  content_json)
        waiting_sets = filter(lambda element: not (element["available_seats"] > 0) and (element["waiting_list_count"] > 0),  content_json)
        for available_seat in available_seats:
            color_print(f"[+] - {available_seat["course_number"]}-{available_seat["section_number"]},", tcolor.OKGREEN, " ")
            color_print(f"Type: {available_seat['class_type']}", tcolor.LEC if available_seat['class_type'] == "LEC" else tcolor.LAB if available_seat['class_type'] == "LAB" else tcolor.RES, ", ")
            color_print(f"Available Seats: {available_seat['available_seats']}, Waiting List: {available_seat['waiting_list_count']}", tcolor.OKGREEN, ", ")
            color_print(f"CRN: {available_seat['crn']}", tcolor.HEADER)
        for available_seat in waiting_sets:
            color_print(f"[+] - {available_seat["course_number"]}-{available_seat["section_number"]},", tcolor.OKGREEN, " ")
            color_print(f"Type: {available_seat['class_type']}", tcolor.LEC if class_type == "LEC" else tcolor.LAB if class_type == "LAB" else tcolor.RES, ", ")
            color_print(f"Available Seats: {available_seat['available_seats']}, Waiting List: {available_seat['waiting_list_count']}", tcolor.OKGREEN, ", ")
            color_print(f"CRN: {available_seat['crn']}", tcolor.HEADER)