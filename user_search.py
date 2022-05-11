# import cli_colors and Questions classes to print colorful text and ask user for input
from cli import Questions, cli_colors

# import stdout to write colorful text
from sys import stdout

def get_search_input() -> dict:
    """
    Ask user for what he want to search by each refresh.\n
    return answer as `dict` type.
    """

    filter_dictionary = {}
    search_by = Questions.mcq_list_question(question="What filters you wany to check each refresh", choices=["Check `ALL` courses of the department", "Section/Sections", "Activity/Activities", "CRN/CRNs", "Course/Courses Name", "Instructor/Instructors", "Day/Days", "Time/Times","Building/Buildings", "Status/Statuses", "Gender"])

    if ("Check ALL courses of the department" in search_by):
        return None
    else:
        for i in search_by:
            if (i == "Section/Sections"):
                sections_list = []
                while True:
                    activities_list = Questions.str_questoin("Enter Section/Sections you want to check each refresh")
                    ans = True
                    for i in activities_list.strip().split(" "):
                        if (i.isdigit()):
                            sections_list.append(i if int(i) > 9 else f"0{i}" if len(i) == 1 else f"{i}")
                        else:
                            stdout.write("\x1b[91m! Sorry, your reply was invalid: '\x1b[0m\x1b[1m{}\x1b[0m\x1b[91m' is not a valid answer, please try again\n".format(i))
                            stdout.flush()
                            ans = False
                            break

                    if (ans == False):
                        sections_list = []
                        continue
                    else:
                        break
                filter_dictionary["section"] = sections_list
            elif (i == "Activity/Activities"):
                activities_list = Questions.mcq_list_question(question="Select type of activity you want to check each refresh", choices=["COP", "DIS", "FLD", "IND", "LAB", "LLB", "LEC", "MR", "PRJ", "RES", "SEM", "SLB", "ST", "STD", "THS"])
                if (len(activities_list) == 15):
                    pass
                else:
                    filter_dictionary["activity"] = activities_list
            elif (i == "CRN/CRNs"):
                crns_list = []
                while True:
                    ans = True
                    activities_list = Questions.str_questoin("Enter CRN/CRNs you want to check each refresh")
                    for i in activities_list.strip().split(" "):
                        if (i.isdigit()):
                            crns_list.append(i if int(i) > 9 else f"0{i}" if len(i) == 1 else f"{i}")
                            ans = True
                        else:
                            stdout.write("\x1b[91m! Sorry, your reply was invalid: '\x1b[0m\x1b[1m{}\x1b[0m\x1b[91m' is not a valid answer, please try again\n".format(i))
                            ans = False
                            break

                    if (ans == False):
                        crns_list = []
                        continue
                    else:
                        break
                filter_dictionary["section"] = crns_list
            elif (i == "Course/Courses Name"):
                course_names_list = []
                while True:
                    index = 0
                    ans = True
                    courses_names_str = Questions.str_questoin(question="Enter Course/Courses Name you want to check each refresh")
                    for element in courses_names_str.split(" "):
                        if (element.isalpha()):
                            if (index%2 == 1):
                                stdout.write(f"\x1b[91m! Sorry, there isn't course such as: '\x1b[0m\x1b[1m{element}\x1b[0m\x1b[91m', please try again\n")
                                stdout.flush()
                                ans = False
                                break
                            course = element
                            index += 1
                        elif (element.isdigit()):
                            if (index%2 == 0):
                                stdout.write(f"\x1b[91m! Sorry, there isn't course such as: '\x1b[0m\x1b[1m{element}\x1b[0m\x1b[91m', please try again\n")
                                stdout.flush()
                                ans = False
                                break
                            course += element
                            course_names_list.append(course)
                            index+=1
                        elif (element.isalnum()):
                            course_names_list.append(element)
                            index += 2

                    if (ans == False):
                        continue
                    else:
                        stdout.write("\x1b[u\x1b[0K")
                        stdout.write("\x1b[94m{}\x1b[0m\n".format(" ".join(course_names_list).upper()))
                        break
                filter_dictionary["name"] = course_names_list
            elif (i == "Instructor/Instructors"):
                instructors_list = Questions.str_questoin("Enter Instructor/Instructor you want to check each refresh")
                filter_list = instructors_list
            elif (i == "Day/Days"):
                days_list = Questions.mcq_dict_question(question="Select the Day/Days Course/Courses occurs", choices={"U, Sunday":"U", "M, Monday":"M", "T, Tuesday":"T", "W, Wednesday":"W", "R, Thursday":"R", "F, Friday":"F", "S, Saturday":"S"})
                if (len(days_list) == 7):
                    pass
                else:
                    filter_dictionary["day"] = days_list
            elif (i == "Time/Times"):
                cli_colors.colorful_print(text_string="e.g. 1000-1050 1300-1350", text_color=cli_colors.BRIGHT_CYAN)
                str_answer = Questions.str_questoin("Enter Time/Times you want to check each refresh")
                filter_dictionary["time"] = str_answer.split(" ")
            elif (i == "Building/Buildings"):
                buildings_list = []
                while True:
                    activities_list = Questions.str_questoin("Enter Building/Buildings you want to check each refresh")
                    for i in activities_list.strip().split(" "):
                        if (i.isdigit()):
                            buildings_list.append(i)
                            ans = True
                        else:
                            stdout.write("\x1b[91m! Sorry, your reply was invalid: '\x1b[0m\x1b[1m{}\x1b[0m\x1b[91m' is not a valid answer, please try again\n".format(i))
                            ans = False
                            break

                    if (ans == False):
                        crns_list = []
                        continue
                    else:
                        break
                filter_dictionary["buildings"] = buildings_list
            elif (i == "Status/Statuses"):
                status_list = Questions.mcq_list_question(question="Select status of course/courses", choices=["Open", "Wait list"])
                if (status_list == 2):
                    pass
                else:
                    filter_dictionary["status"] = status_list
            elif (i == "Gender"):
                genders_list = Questions.mcq_list_question(question="Select the gender of course/courses meant to have", choices=["Open", "Wait list"])
                if (genders_list == 2):
                    pass
                else:
                    filter_dictionary["gender"] = genders_list

    return filter_dictionary