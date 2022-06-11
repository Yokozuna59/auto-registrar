from sys import stdout
from cli import AnsiEscapeCodes

def check_for_changes(content: dict, search_input: dict, configurations: str) -> None:
    """
    Checks if there is available seats in courses.\n
    after checking, return `None`.
    """

    content_json = content["data"]
    all_colors = {"COP":"\x1b[48;2;92;148;13m",
                  "DIS":"\x1b[48;2;201;42;42m",
                  "FLD":"\x1b[48;2;33;37;41m",
                  "IND":"\x1b[48;2;33;37;41m",
                  "LAB":"\x1b[48;2;95;61;196m",
                  "LEC":"\x1b[48;2;24;100;171m",
                  "LLB":"\x1b[48;2;33;37;41m",
                  "LPJ":"\x1b[48;2;33;37;41m",
                  "MR":"\x1b[48;2;33;37;41m",
                  "PRJ":"\x1b[48;2;217;72;15m",
                  "REC":"\x1b[48;2;166,30,77m",
                  "RES":"\x1b[48;2;201;42;42m",
                  "SEM":"\x1b[48;2;8;127;91m",
                  "SLB":"\x1b[48;2;33;37;41m",
                  "ST":"\x1b[48;2;33;37;41m",
                  "STD":"\x1b[48;2;33;37;41m",
                  "THS":"\x1b[48;2;54;79;199m"
                 }

    if (search_input == None):
        found_elements = filter(lambda x: int(x["available_seats"]) > 0 or int(x["waiting_list_count"]) > 0,  content_json)
        if (configurations["interface"] == "cli"):
            for index, element in enumerate(found_elements):
                crn                 = element["crn"]
                course_name         = element["course_number"].replace(" ", "")
                section             = element["section_number"]
                available_seats     = element["available_seats"]
                waiting_list_count  = element["waiting_list_count"]
                class_type          = element["class_type"]

                if (available_seats > 0):
                    colors = AnsiEscapeCodes.LIGHT_GREEN
                    signs = "+"
                elif (waiting_list_count > 0):
                    colors = AnsiEscapeCodes.LIGHT_YELLOW
                    signs = "-"
                else:
                    continue

                stdout.write(f"{colors}[{signs}] - {course_name}-{section}, ")
                stdout.write(f"Type:{AnsiEscapeCodes.RESET} {all_colors[class_type]}{class_type}{AnsiEscapeCodes.RESET}{colors}, ")
                stdout.write(f"Available Seats: {available_seats}, Waiting List: {waiting_list_count} ")
                stdout.write("CRN:{} {}{}{}\n".format(AnsiEscapeCodes.RESET, AnsiEscapeCodes.LIGHT_BLUE if index%2==0 else AnsiEscapeCodes.LIGHT_MAGENTA, crn, AnsiEscapeCodes.RESET))
    else:
        found_elements = filter(lambda x: int(x["available_seats"]) > 0 or int(x["waiting_list_count"]) > 0,  content_json)
        if (configurations["interface"] == "cli"):
            for i in search_input:
                if (i == "section"):
                    found_elements = list(filter(lambda x: x["section_number"] in search_input["section"],  found_elements))
                elif (i == "activity"):
                    found_elements = list(filter(lambda x: x["class_type"] in search_input["activity"],  found_elements))
                elif (i == "crn"):
                    found_elements = list(filter(lambda x: x["crn"] in search_input["crn"],  found_elements))
                elif (i == "course_number"):
                    found_elements = list(filter(lambda x: x["course_number"].replace(" ", "") in search_input["course_number"], found_elements))
                elif (i == "instructor_name"):
                    found_elements = list(filter(lambda x: x["instructor_name"] in search_input["instructor_name"], found_elements))
                elif (i == "class_days"):
                    found_elements = list(filter(lambda x: x["class_days"] in search_input["class_days"], found_elements))
                # elif (i == "time"):
                #     (filter(lambda x: x["building"] in search_user_input["building"], found_elements))
                elif (i == "building"):
                    found_elements = list(filter(lambda x: x["building"] in search_input["building"], found_elements))
                elif (i == "status"):
                    if (search_input["status"] == "Open"):
                        found_elements = list(filter(lambda x: x["available_seats"] > 0, found_elements))
                    else:
                        found_elements = list(filter(lambda x: x["waiting_list_count"] > 0 and x["available_seats"] <= 0, found_elements))
                elif (i == "gender"):
                    found_elements = list(filter(lambda x: "F" in x["section_number"] if search_input["gender"] == "F" else "F" not in x["section_number"], found_elements))

            for index, element in enumerate(found_elements):
                crn                 = element["crn"]
                course_name         = element["course_number"].replace(" ", "")
                section             = element["section_number"]
                available_seats     = element["available_seats"]
                waiting_list_count  = element["waiting_list_count"]
                class_type          = element["class_type"]

                if (available_seats > 0):
                    colors = AnsiEscapeCodes.LIGHT_GREEN
                    signs = "+"
                elif (waiting_list_count > 0):
                    colors = AnsiEscapeCodes.LIGHT_YELLOW
                    signs = "-"
                else:
                    continue

                try:
                    stdout.write(f"{colors}[{signs}] - {course_name}-{section}, ")
                    stdout.write(f"Type:{AnsiEscapeCodes.RESET} {all_colors[class_type]}{class_type}{AnsiEscapeCodes.RESET}{colors}, ")
                    stdout.write(f"Available Seats: {available_seats}, Waiting List: {waiting_list_count} ")
                    stdout.write("CRN:{} {}{}{}\n".format(AnsiEscapeCodes.RESET, AnsiEscapeCodes.LIGHT_BLUE if index%2==0 else AnsiEscapeCodes.LIGHT_MAGENTA, crn, AnsiEscapeCodes.RESET))
                except:
                    continue
    return None