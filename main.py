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

def check_for_change(content, search_user_input):
    content_json = json.loads(content)["data"]
    found_elements = filter(lambda j: j["crn"] in search_user_input["CRN"],  content_json)
    id2dict = dict((d['crn'], d) for d in found_elements)
    try:
        found_elements_sorted = [id2dict[x] for x in search_user_input["CRN"]]
        for element in found_elements_sorted:
            if element['available_seats'] and element['waiting_list_count']:
                print(f"available_seats CRN: {element['crn']}")
            elif element['waiting_list_count']:
                print(f"waiting_list CRN: {element['crn']}")
    except KeyError:
        # one or more CRNs are not in the department and term specified
        pass

def main():
    set_recursion_limit()
    configurations = check_config()
    registrar_user_input = get_requests("https://registrar.kfupm.edu.sa/courses-classes/course-offering/")
    search_user_input = get_search_input()
    print(search_user_input)

    while True:
        content = get_requests(f"https://registrar.kfupm.edu.sa/api/course-offering?term_code={registrar_user_input[0]}&department_code={registrar_user_input[1]}")
        print(content)
        check_for_change(content, search_user_input)
        time_delay(configurations["delay"])

if __name__ == "__main__":
    main()
