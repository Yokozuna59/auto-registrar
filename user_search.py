# import cli_colors and Questions classes to print colorful text and ask user for input
from cli import Questions, cli_colors

# import stdout to write colorful text
from sys import stdout

# import prompt to ask user for input
from PyInquirer import prompt

def get_search_input() -> dict:
    """
    Ask user how many filters he want to check eash refresh.
    """

    while True:
        str_answer = Questions.str_questoin(question="How many filters you want to check each refresh")
        if (str_answer.isdigit()):
            str_answer = int(str_answer)
            return get_filters(filters=str_answer)
        else:
            stdout.write("\x1b[91m! Sorry, your reply was invalid: '\x1b[0m\x1b[1m{}\x1b[0m\x1b[91m' is not a valid answer, please try again\n".format(str_answer))
            continue

def get_filters(filters: int) -> dict:
    """
    Ask user for what he want to search by each refresh.\n
    return answer as `dict` type.
    """

    filter_dictionary = {}

    for i in range(filters):
        filter_list = []
        search_by = Questions.list_question(question="Search by", choices=["Section/Sections", "Activity/Activities", "CRN/CRNs", "Course/Courses Name", "Instructor", "Day/Days", "Time/Times","Building/Buildings", "Status/Statuses", "Gender", "All Department Courses"])
        if (search_by == "All Department Courses"):
            return
        elif (search_by == "Section/Sections"):
            while True:
                str_answer = Questions.str_questoin("Enter {} you want to check each refresh".format(search_by))
                for i in str_answer.strip().split(" "):
                    if (i.isdigit()):
                        filter_list.append(i if int(i) > 9 else f"0{i}" if len(i) == 1 else f"{i}")
                    else:
                        stdout.write("\x1b[91m! Sorry, your reply was invalid: '\x1b[0m\x1b[1m{}\x1b[0m\x1b[91m' is not a valid answer, please try again\n".format(i))
                        filter_list = []
                        continue
        elif (search_by == "Activity/Activities"):
            section_answer=list((prompt(questions={'type': 'checkbox', 'qmark': '?', "name": "Activity", 'message': 'Select type of activity?', "choices":[{"name":"COP"}, {"name":"DIS"}, {"name":"FLD"}, {"name":"IND"}, {"name":"LAB"}, {"name":"LLB"}, {"name":"LEC"}, {"name":"MR"}, {"name":"PRJ"}, {"name":"RES"}, {"name":"SEM"}, {"name":"SLB"},  {"name":"ST"}, {"name":"STD"}, {"name":"THS"}]})).values())
            filter_list = section_answer
            """activity = Questions.list_question(question="Select type of activity", choices=["COP", "DIS", "FLD", "IND", "LAB", "LLB", "LEC", "MR", "PRJ", "RES", "SEM", "SLB", "ST", "STD", "THS", "All"])
            filters_list.append(activity if activity != "All" else None)"""
        elif (search_by == "CRN/CRNs"):
            while True:
                str_answer = Questions.str_questoin("Enter {} you want to check each refresh".format(search_by))
                for i in str_answer.strip().split(" "):
                    if (i.isdigit()):
                        filter_list.append(i)
                    else:
                        stdout.write("\x1b[91m! Sorry, your reply was invalid: '\x1b[0m\x1b[1m{}\x1b[0m\x1b[91m' is not a valid answer, please try again\n".format(i))
                        filter_list = []
                        continue
        elif (search_by == "Course/Courses Name"):
            str_answer = Questions.str_questoin("Enter {} you want to check each refresh".format(search_by))
            for i in str_answer.split(" "):
                if (i.isalpha()):
                    course = i
                elif (i.isdigit()):
                    course += i
                    filter_list.append(course)
                elif (i.isalnum()):
                    filter_list.append(i)
        elif (search_by == "Instructor"):
            str_answer = Questions.str_questoin("Enter {} you want to check each refresh".format(search_by))
            filter_list = str_answer
        elif (search_by == "Day/Days"):
            section_answer=list((prompt(questions={'type': 'checkbox', 'qmark': '?', "name": "day", 'message': 'Select days of course/courses occurs?', "choices":[{"name":"U"}, {"name":"M"}, {"name":"T"}, {"name":"W"}, {"name":"T"}]})).values())
            filter_list = "".join(section_answer)
        elif (search_by == "Time/Times"):
            cli_colors.colorful_print(text_string="e.g. 1000-1050 1300-1350", text_color=cli_colors.BRIGHT_CYAN)
            str_answer = Questions.str_questoin("Enter {} you want to check each refresh".format(search_by))
            filter_list = str_answer.split(" ")
        elif (search_by == "Building/Buildings"):
            while True:
                str_answer = Questions.str_questoin("Enter {} you want to check each refresh".format(search_by))
                for i in str_answer.strip().split(" "):
                    if (i.isdigit()):
                        filter_list.append(i)
                    else:
                        stdout.write("\x1b[91m! Sorry, your reply was invalid: '\x1b[0m\x1b[1m{}\x1b[0m\x1b[91m' is not a valid answer, please try again\n".format(i))
                        filter_list = []
                        continue
        elif (search_by == "Status/Statuses"):
            dict_answer = Questions.dict_question(question="Select status of course/courses", choices={"Open":"open","Wait list":"wait_list", "Any":None})
            filter_list = dict_answer
        elif (search_by == "Gender"):
            dict_answer = Questions.dict_question(question="Select status of course/courses", choices={"Male":"male","Female":"female","Any":None})
            filter_list = dict_answer

        filter_dictionary[search_by.split("/")[0].lower()] = filter_list

    return filter_dictionary