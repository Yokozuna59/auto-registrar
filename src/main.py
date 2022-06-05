from sys import setrecursionlimit
from config import check_configurations
from registrar_requests import get_requests
from user_search import get_search_input
from c4c import check_for_changes
from cli import progress_bar

def main() -> None:
    """
    Main and start function of this project.\n
    After checking/registraring is done, return `None`.
    """

    # set recursion limit to 1000000
    setrecursionlimit(1000000)

    # get config file as dict type
    configurations = check_configurations()

    # get term and department as list
    term_dep_input = get_requests(request_url="https://reg-serviceapp.kfupm.edu.sa/course-offering/", interface_config=configurations["interface"])

    # get the user input for the search
    search_input = get_search_input(config_file=configurations)

    while True:
        # get content of the request
        request_content = get_requests(request_url="https://registrar.kfupm.edu.sa/api/course-offering?term_code={}&department_code={}".format(term_dep_input[0], term_dep_input[1]), interface_config=configurations["interface"])

        # check if sections has changed
        check_for_changes(content=request_content, search_input=search_input, configurations=configurations)

        # wait for configured time
        progress_bar(total_time=configurations["delay"])

if __name__ == "__main__":
    # run the main function
    main()