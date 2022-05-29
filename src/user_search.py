from cli import Questions, AnsiEscapeCodes, colorful_text
from sys import stdout

def get_search_input(config_file: str) -> dict:
    """
    Ask user for what he want to search by each refresh.\n
    return answer as `dict` type.
    """

    filter_dictionary = {}
    if (config_file["interface"] == "cli"):
        if (config_file["browser"] != None):
            registrar_answer = Questions.bool_question(question="Do you want to registrar course/courses", default=False)
            if (registrar_answer == True):
                while True:
                    crns_list = []
                    crns_str = Questions.str_questoin("Enter CRN/CRNs you want to registrar")
                    for crn in crns_str.strip().split(" "):
                        if (crn.isdigit()):
                            crns_list.append(crn)
                            ans = True
                        else:
                            stdout.write(f"{AnsiEscapeCodes.RED}! Sorry, your reply was invalid:{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}\"{crn}\"{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.RED}is not a valid answer, please try again.{AnsiEscapeCodes.RESET}\n")
                            ans = False
                            break

                    if (ans != False):
                        break
                filter_dictionary["registrar"] = True
                filter_dictionary["crn"] = crns_list
                return filter_dictionary

        search_by = Questions.mcq_list_question(question="What filters you wany to check each refresh", choices=["Check `ALL` courses of the department", "Section/Sections", "Activity/Activities", "CRN/CRNs", "Course/Courses Name", "Instructor/Instructors", "Day/Days", "Time/Times","Building/Buildings", "Status/Statuses", "Gender"])
        if ("Check `ALL` courses of the department" in search_by):
            return None
        else:
            for i in search_by:
                if (i == "Section/Sections"):
                    while True:
                        ans = True
                        sections_list = []
                        sections_str = Questions.str_questoin("Enter Section/Sections you want to check each refresh")
                        for section in sections_str.strip().split(" "):
                            if (section.isdigit()):
                                sections_list.append(section if int(section) > 9 else f"0{section}" if len(section) == 1 else f"{section}")
                            else:
                                stdout.write(f"{AnsiEscapeCodes.RED}! Sorry, your reply was invalid:{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}\"{section}\"{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.RED}is not a valid answer, please try again.{AnsiEscapeCodes.RESET}\n")
                                stdout.flush()
                                ans = False
                                break

                        if (ans != False):
                            break
                    filter_dictionary["section"] = sections_list
                elif (i == "Activity/Activities"):
                    activities_str = Questions.mcq_list_question(question="Select type of activity you want to check each refresh", choices=["COP", "DIS", "FLD", "IND", "LAB", "LLB", "LEC", "MR", "PRJ", "RES", "SEM", "SLB", "ST", "STD", "THS"])
                    if (len(activities_str) != 15):
                        filter_dictionary["activity"] = activities_str
                elif (i == "CRN/CRNs"):
                    while True:
                        crns_list = []
                        crns_str = Questions.str_questoin("Enter CRN/CRNs you want to check each refresh")
                        for crn in crns_str.strip().split(" "):
                            if (crn.isdigit()):
                                crns_list.append(crn)
                                ans = True
                            else:
                                stdout.write(f"{AnsiEscapeCodes.RED}! Sorry, your reply was invalid:{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}\"{crn}\"{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.RED}is not a valid answer, please try again.{AnsiEscapeCodes.RESET}\n")
                                ans = False
                                break

                        if (ans != False):
                            break
                    filter_dictionary["crn"] = crns_list
                elif (i == "Course/Courses Name"):
                    while True:
                        ans = True
                        course_names_list = []
                        courses_names_str = Questions.str_questoin(question="Enter Course/Courses Name you want to check each refresh")
                        for index, element in enumerate(courses_names_str.split(" ")):
                            if (element.isalpha()):
                                if (index%2 == 1):
                                    stdout.write(f"{AnsiEscapeCodes.RED}! Sorry, your reply was invalid:{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}\"{crn}\"{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.RED}is not a valid answer, please try again.{AnsiEscapeCodes.RESET}\n")
                                    stdout.flush()
                                    ans = False
                                    break
                                course = element
                                index += 1
                            elif (element.isdigit()):
                                if (index%2 == 0):
                                    stdout.write(f"{AnsiEscapeCodes.RED}! Sorry, your reply was invalid:{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}\"{crn}\"{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.RED}is not a valid answer, please try again.{AnsiEscapeCodes.RESET}\n")
                                    stdout.flush()
                                    ans = False
                                    break
                                course += element
                                course_names_list.append(course.upper())
                                index+=1
                            elif (element.isalnum()):
                                course_names_list.append(element.upper())
                                index += 2

                        if (ans != False):
                            stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                            stdout.write(AnsiEscapeCodes.ERASE_TO_END_OF_LINE)
                            stdout.write("{}{}{}\n".format(AnsiEscapeCodes.LIGHT_BLUE, " ".join(course_names_list).upper(), AnsiEscapeCodes.RESET))
                            break
                    filter_dictionary["course_number"] = course_names_list
                elif (i == "Instructor/Instructors"):
                    colorful_text(text_string="Currently the instructors filter is not supported!", text_color=AnsiEscapeCodes.RED)
                    continue
                #     colorful_text(text_string="e.g. ABDULRAHMAN AL-ARFAJ; MOHAMMAD SIDDIQUI", text_color=AnsiEscapeCodes.BRIGHT_CYAN)
                #     instructors_list = Questions.str_questoin("Enter Instructor/Instructor you want to check each refresh (type the full name of instructor, each instructor separate with ;)")
                #     filter_dictionary["instructor_name"] = instructors_list.split(";")
                elif (i == "Day/Days"):
                    days_list = Questions.mcq_dict_question(question="Select the Day/Days Course/Courses occurs", choices={"U, Sunday":"U", "M, Monday":"M", "T, Tuesday":"T", "W, Wednesday":"W", "R, Thursday":"R", "F, Friday":"F", "S, Saturday":"S"})
                    if (len(days_list) != 7):
                        filter_dictionary["class_days"] = days_list
                elif (i == "Time/Times"):
                    colorful_text(text_string="Currently the instructors filter is not supported!", text_color=AnsiEscapeCodes.RED)
                    continue
                #     colorful_text(text_string="e.g. 0800-1050 1300-1350", text_color=cli_colors.BRIGHT_CYAN)
                #     times_str = Questions.str_questoin("Enter Time/Times you want to check each refresh")
                #     filter_dictionary["course_number"] = times_str.split(" ")
                elif (i == "Building/Buildings"):
                    while True:
                        buildings_list = []
                        buildings_str = Questions.str_questoin("Enter Building/Buildings you want to check each refresh")
                        for building in buildings_str.strip().split(" "):
                            if (building.isdigit()):
                                buildings_list.append(building)
                                ans = True
                            else:
                                stdout.write(f"{AnsiEscapeCodes.RED}! Sorry, your reply was invalid:{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}\"{building}\"{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.RED}is not a valid answer, please try again.{AnsiEscapeCodes.RESET}\n")
                                ans = False
                                break

                        if (ans != False):
                            break
                    filter_dictionary["building"] = buildings_list
                elif (crn == "Status/Statuses"):
                    status_list = Questions.mcq_list_question(question="Select status of course/courses", choices=["Open", "Wait list"])
                    if (status_list != 2):
                        filter_dictionary["status"] = status_list[0]
                elif (crn == "Gender"):
                    genders_list = Questions.mcq_dict_question(question="Select the gender of course/courses meant to have", choices={"Male":"M", "Female":"F"})
                    if (genders_list != 2):
                        filter_dictionary["gender"] = genders_list[0]
        filter_dictionary["registrar"] = False
    return filter_dictionary