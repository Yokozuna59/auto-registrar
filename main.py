# import setrecursionlimit to set the recursion limit to 100000
from sys import setrecursionlimit

# import check_configuration to check if user has configurated yet or not
from config import check_configuration

# import get_requests to get the content of the url
from registrar_requests import get_requests

# import get_search_input function to get the user input for the search
from user_search import get_search_input

# import check_platform to get driver's path
from check_platforms import check_platform

# import check_for_change to check if sections has changed
from check_for_changes import check_for_change

# import time_delay to make the script wait
from delay import time_delay

def main() -> None:
    """
    This is the main and start function of this project.
    """

    # set recursion limit to 1000000
    setrecursionlimit(100000)

    # get config file as dict type
    configuration = check_configuration()

    # get term and department as list
    registrar_user_input = get_requests(request_url="https://registrar.kfupm.edu.sa/courses-classes/course-offering/")

    search_user_input = get_search_input()

    driver_path = check_platform(browser=configuration["browser"])

    while True:
        request_content = get_requests(request_url="https://registrar.kfupm.edu.sa/api/course-offering?term_code={}&department_code={}".format(registrar_user_input[0], registrar_user_input[1]))
        check_for_change(content=request_content, search_input=search_user_input, driver_path=driver_path)
        time_delay(refresh_time=configuration["delay"])

if __name__ == "__main__":
    # run the main function
    main()