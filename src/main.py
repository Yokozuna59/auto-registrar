# import setrecursionlimit to set the recursion limit to 100000
from sys import setrecursionlimit

# import check_configs to check if user has configurated yet or not
from config import check_configs

# import get_term_and_department and get_course_offering_data to request and get data
from registrar_requests import get_term_and_department, get_course_offering_data

# import get_search_input to get user input/s for search
from user_search import get_search_input

# import check_for_changes to check if section/s is/are open
from c4c import check_for_changes

# import progress_bar to print a progress bar
from cli import progress_bar

def main() -> None:
    """
    Main and start function of this project.\n
    After checking/registraring is done, return `None`.
    """

    # set recursion limit to 1000000
    setrecursionlimit(100000)

    # get config file
    configs = check_configs()

    # get term and department
    term_and_department_input = get_term_and_department(request_url="https://reg-serviceapp.kfupm.edu.sa/course-offering/", interface_config=configs["interface"])

    # get user input/s for search
    search_input = get_search_input(configs_file=configs)

    while True:
        # request and get courses from course offering
        courses_requested = get_course_offering_data(term=term_and_department_input[0], department=term_and_department_input[1], interface_config=configs["interface"], user_search=search_input)

        # check if section/s is/are open
        check_for_changes(content=courses_requested, search_input=search_input, configurations=configs)

        # print a progress bar
        progress_bar(total_time=configs["delay"])

if __name__ == "__main__":
    # run the main function
    main()