# import setrecursionlimit to set the recursion limit to 100000
from sys import setrecursionlimit

# import check_configuration to check if user has configurated yet or not
from config import check_configurations

# import get_requests to get the content of the url
from registrar_requests import get_requests

# import get_search_input function to get the user input for the search
from user_search import get_search_input

# import check_for_change to check if sections has changed
from c4c import check_for_changes

# import time_delay to make the script wait
from cli import time_delay

def main() -> None:
    """
    Main and start function of this project.\n
    After checking/registraring is done, return `None`.
    """

    # set recursion limit to 1000000
    setrecursionlimit(100)

    # get config file as dict type
    configurations = check_configurations()

    # get term and department as list
    term_dep_input = get_requests(request_url="https://registrar.kfupm.edu.sa/courses-classes/course-offering/", interface_config=configurations["interface"])

    # get the user input for the search
    search_input = get_search_input(interface_config=configurations["interface"])

    while True:
        # get content of the request
        request_content = get_requests(request_url="https://registrar.kfupm.edu.sa/api/course-offering?term_code={}&department_code={}".format(term_dep_input[0], term_dep_input[1]), interface_config=configurations["interface"])

        # check if sections has changed
        check_for_changes(content=request_content, search_input=search_input, configurations=configurations)

        # wait for configured time
        time_delay(refresh_time=configurations["delay"])

if __name__ == "__main__":
    # run the main function
    main()