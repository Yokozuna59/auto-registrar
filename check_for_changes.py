# import loads to load the json data
from json import loads

from sys import stdout

def check_for_change(content, search_user_input, driver_path):
    content_json = loads(str(content))["data"]
    all_colors = {"COP":"\x1b[48;2;92;148;13m",
                  "DIS":"\x1b[48;2;201;42;42m",
                  "FLD":"\x1b[48;2;33;37;41m",
                  "IND":"\x1b[48;2;33;37;41m",
                  "LAB":"\x1b[48;2;95;61;196m",
                  "LEC":"\x1b[48;2;24;100;171m",
                  "LLB":"\x1b[48;2;33;37;41m",
                  "MR":"\x1b[48;2;33;37;41m",
                  "PRJ":"\x1b[48;2;217;72;15m",
                  "RES":"\x1b[48;2;201;42;42m",
                  "SEM":"\x1b[48;2;8;127;91m",
                  "SLB":"\x1b[48;2;33;37;41m",
                  "ST":"\x1b[48;2;33;37;41m",
                  "STD":"\x1b[48;2;33;37;41m",
                  "THS":"\x1b[48;2;54;79;199m"
                 }

    if (search_user_input != None):
        found_elements = filter(lambda j: j["crn"] in search_user_input["crn"],  content_json)
        id2dict = dict((d['crn'], d) for d in found_elements)
        try:
            found_elements_sorted = [id2dict[x] for x in search_user_input["crn"]]
            for element in found_elements_sorted:
                if element['available_seats'] and element['waiting_list_count']:
                    print(f"available_seats CRN: {element['crn']}")
                elif element['waiting_list_count']:
                    print(f"waiting_list CRN: {element['crn']}")
        except KeyError:
            # one or more CRNs are not in the department and term specified
            pass
    else:
        found_elements = filter(lambda i: int(i["available_seats"]) > 0 or int(i["waiting_list_count"]) > 0,  content_json)
        for index, element in enumerate(found_elements):
            crn                 = element["crn"]
            course_name         = element["course_number"]
            section             = element["section_number"]
            available_seats     = element["available_seats"]
            waiting_list_count  = element["waiting_list_count"]
            class_type          = element["class_type"]

            if (available_seats > 0):
                colors = "92"
                signs = "+"
            elif (waiting_list_count > 0):
                colors = "93"
                signs = "-"
            stdout.write("\x1b[{}m[{}] - {}-{}, ".format(colors, signs, course_name, section))
            stdout.write("Type:\x1b[0m {}{}\x1b[0m\x1b[{}m, ".format(all_colors[class_type], class_type, colors))
            stdout.write("Available Seats: {}, Waiting List: {} ".format(available_seats, waiting_list_count))
            stdout.write("CRN:\x1b[0m \x1b[{}m{}\n".format("94" if index%2==0 else "95", crn))