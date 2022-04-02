# import tcolor class and color_input and color_choices functions to print colored text
from colorful_terminal import *

# import input_not_int and number_out_of_range function to show the error messages
from errors import input_not_int, number_out_of_range

def search_choices(i):
    if (i == 2):
        questions = ["LEC","LAB","COP","PRJ","SEM","THS","STD","LLB","RES","SLB","MR","DIS","IND","ST","FLD", "Any"]
    elif (i == 9):
        questions = ["Open","Wait list", "Any"]
    elif (i == 10):
        questions = ("Male","Female","Any")

    color_choices(questions)
    return questions

def get_search_input():
    filters = color_input("[*] - How many fliters you want to check each time: ", tcolor.OKGREEN)
    if (filters.isdigit()):
        filters = int(filters)
    else:
        input_not_int(filters)

    return get_filters(filters)

def get_filters(filters):
    filter_dictionary = {}

    for i in range(filters):
        element_list = ["Section/Sections","Activity/Activities","CRN/CRNs","Course/Courses Name","Instructor/Instructors","Day/Days","Time/Times","Building/Buildings","Status/Statuses","Gender","All Department Courses"]
        color_choices(element_list)

        search_by = color_input("[*] - Search by: ", tcolor.OKGREEN)
        if (search_by.isdigit()):
            search_by = int(search_by)
        else:
            input_not_int(search_by)

        fliters_list = []
        if (search_by > 0 and search_by <= 11):
            search_type = element_list[search_by - 1]

            if (search_by == 2 or search_by == 9 or search_by == 10):
                choices = search_choices(search_by)
            elif (search_by == 7):
                color_print("e.g. 1000-1050 1300-1350", tcolor.OKBLUE)

            if (search_by != 11):
                user_input = color_input(f"[*] - Enter {search_type}: ", tcolor.OKGREEN)
            else:
                return None

            if (search_by == 1):
                for i in user_input.split(" "):
                    if (i.isdigit()):
                        fliters_list.append(i if int(i) > 9 else f"0{i}" if len(i) == 1 else f"{i}")
                    else:
                        input_not_int(user_input)
            elif (search_by == 2):
                if (user_input.isdigit()):
                    if (int(user_input) > 0 and int(user_input) <= len(choices)):
                        fliters_list.append(choices[int(user_input) - 1])
                    else:
                        number_out_of_range()
                else:
                    input_not_int(user_input)
            elif (search_by == 3 or search_by == 7):
                fliters_list = user_input.split(" ")
            elif (search_by == 4):
                fliters_list.append(user_input.replace(" ", ""))
            elif (search_by == 5):
                fliters_list.append(user_input)
            elif (search_by == 6):
                fliters_list.append(user_input.upper())
            elif (search_by == 8):
                for i in user_input.split(" "):
                    if (i.isdigit()):
                        fliters_list.append(user_input)
                    else:
                        input_not_int(user_input)
            elif (search_by == 9 or search_by == 10):
                if (user_input.isdigit()):
                    if (int(user_input) > 0 and int(user_input) <= len(choices)):
                        fliters_list = choices[int(user_input) - 1].lower()
                    else:
                        number_out_of_range()
                else:
                    input_not_int(user_input)
        else:
            number_out_of_range()
        filter_dictionary[search_type.split("/")[0].lower()] = fliters_list

    return filter_dictionary