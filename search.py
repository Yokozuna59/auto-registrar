from color_terminal import *
from main import *

def get_example(i):
    status = ["Open","Wait list", "Both"]
    gender = ("Male","Female","Any")

    if (i == 9):
        lists = status
    else:
        lists = gender

    return lists


def get_search_input():
    filters = int(color_input("[*] - How many fliters you want to check each time: ", tcolor.LIGHT_GREEN))
    filter_dictionary = {}

    for i in range(filters):
        element_list = ["Section/Sections","Activity/Activities","CRN/CRNs","Course Name/Courses","Instructor/Instructors","Day/Days","Time/Times","Building/Buildings","Status/Statuses","Gender","All Department Courses"]
        show_choices(element_list, None, tcolor.LIGHT_BLUE, tcolor.CYAN)
        search_by = int(color_input("[*] - Search by: ", tcolor.LIGHT_GREEN))

        fliter_list = []
        if (search_by > 0 and search_by <= 11):
            search_type = element_list[search_by - 1]
            if (search_by == 7):
                color_print("e.g. 1000-1050 1300-1350", tcolor.LIGHT_BLUE)
            elif (search_by == 9 or search_by == 10):
                example = get_example(search_by)
                show_choices(example, None, tcolor.LIGHT_BLUE, tcolor.CYAN)

            if (search_by != 11):
                user_input = color_input(f"[*] - Enter {search_type}: ", tcolor.LIGHT_GREEN)

            if (search_by != 9 and search_by != 10 and search_by != 11):
                fliter_list.extend(user_input.split(" "))
                filter_dictionary[element_list[search_by - 1].split("/")[0].lower()] = fliter_list
            elif (search_by == 11):
                filter_dictionary = None
                return filter_dictionary
            else:
                fliter_list.extend(user_input.split(" "))
                filter_dictionary[element_list[search_by - 1].split("/")[0].lower()] = fliter_list
        else:
            print("You can't choose a number out of range!")
            return False
    return filter_dictionary
