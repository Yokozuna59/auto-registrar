# import setrecursionlimit to set the recursion limit to 100000
from sys import setrecursionlimit

# import check_config to check if user has configurate yet or not
from config import check_config

# import get_requests to get the content of the url
from registrar_requests import get_requests

# import time_delay to make the script wait
from delay import time_delay

# import get_search_input function to get the user input for the search
from user_search import get_search_input

# import check_platform to get driver path
from check_platforms import check_platform

# import check_for_change to check if section has changed
from check_for_changes import check_for_change

def main():
    setrecursionlimit(100000)
    configurations = check_config()
    registrar_user_input = get_requests("https://registrar.kfupm.edu.sa/courses-classes/course-offering/")
    search_user_input = get_search_input()
    driver_path = check_platform(configurations["browser"])

    while True:
        content = get_requests(f"https://registrar.kfupm.edu.sa/api/course-offering?term_code={registrar_user_input[0]}&department_code={registrar_user_input[1]}")
        check_for_change(content, search_user_input, driver_path)
        time_delay(configurations["delay"])

if __name__ == "__main__":
    main()