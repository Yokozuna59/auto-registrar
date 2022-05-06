from cli import Questions, Color_cli

from sys import stdout

from PyInquirer import prompt

def get_search_input():
    while True:
        str_answer = Questions.str_questoin("How many filters you want to chech each refresh")
        if (str_answer.isdigit()):
            str_answer = int(str_answer)
            return get_filters(str_answer)
        else:
            stdout.write("\x1b[91m! Sorry, your reply was invalid: '\x1b[0m\x1b[1m{}\x1b[0m\x1b[91m' is not a valid answer, please try again\n".format(str_answer))
            continue

def get_filters(filters):
    filter_dictionary = {}

    for i in range(filters):
        fliters_list = []

        search_by = Questions.list_question(question="Search by", choices=["Section/Sections", "Activity/Activities", "Course/Courses Name", "Instructor/Instructors", "Day/Days", "Time/Times","Building/Buildings", "Status/Statuses", "Gender", "All Department Courses"])
        if (search_by == "All Department Courses"):
            return None
        elif (search_by == "Section/Sections"):
            while True:
                str_answer = Questions.str_questoin("Enter {} you want to chech each refresh".format(search_by))
                for i in str_answer.strip().split(" "):
                    if (i.isdigit()):
                        fliters_list.append(i if int(i) > 9 else f"0{i}" if len(i) == 1 else f"{i}")
                    else:
                        stdout.write("\x1b[91m! Sorry, your reply was invalid: '\x1b[0m\x1b[1m{}\x1b[0m\x1b[91m' is not a valid answer, please try again\n".format(i))
                        continue
        elif (search_by == "Activity/Activities"):
            section_answer=list((prompt(questions={'type': 'checkbox', 'qmark': '?', "name": "Activity", 'message': 'Select type of activity?', "choices":[{"name":"COP"}, {"name":"DIS"}, {"name":"FLD"}, {"name":"IND"}, {"name":"LAB"}, {"name":"LLB"}, {"name":"LEC"}, {"name":"MR"}, {"name":"PRJ"}, {"name":"RES"}, {"name":"SEM"}, {"name":"SLB"},  {"name":"ST"}, {"name":"STD"}, {"name":"THS"}]})).values())
            fliters_list = section_answer
            """activity = Questions.list_question(question="Select type of activity", choices=["COP", "DIS", "FLD", "IND", "LAB", "LLB", "LEC", "MR", "PRJ", "RES", "SEM", "SLB", "ST", "STD", "THS", "All"])
            fliters_list.append(activity if activity != "All" else None)"""
        elif (search_by == "Course/Courses Name"):
            str_answer = Questions.str_questoin("Enter {} you want to chech each refresh".format(search_by))
            fliters_list = str_answer.split(" ")
        elif (search_by == "Instructor/Instructors"):
            str_answer = Questions.str_questoin("Enter {} you want to chech each refresh".format(search_by))
            fliters_list = str_answer.split(" ")
        elif (search_by == "Day/Days"):
            section_answer=list((prompt(questions={'type': 'checkbox', 'qmark': '?', "name": "day", 'message': 'Select days of course/courses occurs?', "choices":[{"name":"U"}, {"name":"M"}, {"name":"T"}, {"name":"W"}, {"name":"T"}]})).values())
            fliters_list = "".join(section_answer)
        elif (search_by == "Time/Times"):
            Color_cli.colorful_print(text="e.g. 1000-1050 1300-1350", text_color=Color_cli.BRIGHT_CYAN)
            str_answer = Questions.str_questoin("Enter {} you want to chech each refresh".format(search_by))
            fliters_list = str_answer.split(" ")
        elif (search_by == "Building/Buildings"):
            while True:
                str_answer = Questions.str_questoin("Enter {} you want to chech each refresh".format(search_by))
                for i in str_answer.strip().split(" "):
                    if (i.isdigit()):
                        fliters_list.append(i)
                    else:
                        stdout.write("\x1b[91m! Sorry, your reply was invalid: '\x1b[0m\x1b[1m{}\x1b[0m\x1b[91m' is not a valid answer, please try again\n".format(i))
                        continue
        elif (search_by == "Status/Statuses"):
            dict_answer = Questions.dict_question(question="Select status of course/courses", choices={"Open":"open","Wait list":"wait_list", "Any":None})
            fliters_list = dict_answer
        elif (search_by == "Gender"):
            dict_answer = Questions.dict_question(question="Select status of course/courses", choices={"Male":"male","Female":"female","Any":None})
            fliters_list = dict_answer

        filter_dictionary[search_by.split("/")[0].lower()] = fliters_list

    return filter_dictionary