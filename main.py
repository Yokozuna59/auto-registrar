# import setrecursionlimit to set the recursion limit to 43200
from sys import setrecursionlimit

# import check_config to check if user has configurate yet or not
from config import check_config

# import get_requests to get the content of the url
from registrar_requests import get_requests

# import time_delay to make the script wait
from delay import time_delay

# import get_search_input function to get the user input for the search
from user_search import get_search_input

def set_recursion_limit():
    # set the recursion limit to 43200
    setrecursionlimit(43200)

def main():
    set_recursion_limit()
    configurations = check_config()
    registrar_user_input = get_requests("https://registrar.kfupm.edu.sa/courses-classes/course-offering/")
    search_user_input = get_search_input()
    print(search_user_input)

    while True:
        content = get_requests(f"https://registrar.kfupm.edu.sa/api/course-offering?term_code={registrar_user_input[0]}&department_code={registrar_user_input[1]}")
        print(content)
        check_ = json.loads(request.content)
        checks = check_["data"]
        z = filter(lambda j: j["crn"] in crn, checks)
        for x in z:
            if x['available_seats'] and x['waiting_list_count']:
                register(crn, username, password)
                break
        time_delay(configurations["delay"])

if __name__ == "__main__":
    main()
