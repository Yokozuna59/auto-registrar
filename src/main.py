# import functions from local files
from os import system
from config import get_configs
from registrar_requests import get_term_and_department, get_banner9_requests
from user_search import get_search_input
# from registrar_courses import StartBroswer
from c4c import check_for_changes
from cli import AnsiEscapeCodes, print_colorful_text, progress_bar, time_program_execution
from time import time

def main() -> int:
    """
    Main and start function of this project.\n
    After checking/registraring is done, return `None`.
    """

    # for better colorization
    system("")

    # get config file
    configs = get_configs()
    interface = configs["interface"]
    time_delay = configs["delay"]

    # get term and department
    term_and_department_input = get_term_and_department(interface_config=interface)
    term = term_and_department_input[0]
    department = term_and_department_input[1]

    # get user input/s for search
    search_input = get_search_input(configs_file=configs)

    # if (configs["registrar"]):
    #     StartBroswer()

    registrared = False
    while not registrared:
        courses_requested = get_banner9_requests(term=term, department=department)
        registrared = check_for_changes(content=courses_requested, search_input=search_input, configs_file=configs)
        progress_bar(total_time=time_delay)
    return time()

if __name__ == "__main__":
    # run the main function
    start = time()
    end = main()
    number_of_seconds = time_program_execution(userSeconds=int(end - start))
    print_colorful_text(text_string="The program has finished in {} seconds.".format(number_of_seconds), color=AnsiEscapeCodes.GREEN)