from os import system, remove

from auto_registrar.config import get_configs, CONFIGS_PATH
from auto_registrar.tui.bar import progress_bar
from auto_registrar.tui.questions import Questions
from auto_registrar.universities import kfupm


def main():
    # Enhance ansi colors for windows
    system("")

    # Get local configuration
    configs = get_configs(print_ask_for_config=True)
    alarm = configs["alarm"]
    browser = configs["browser"]
    delay = configs["delay"]
    interface = configs["interface"]
    username = configs["username"]
    passcode = configs["passcode"]
    university = configs["university"]
    purpose = (
        Questions.list_question(
            question="What do you want to do in this run",
            choices=[
                "Reconfig configuration",
                "Edit schedule",
                "Check courses status",
            ],
        )
        if configs["configured"] == True
        else "Reconfig configuration"
    )

    if university == "kfupm":
        if purpose == "Reconfig configuration":
            remove(CONFIGS_PATH)
            get_configs(print_ask_for_config=False)
            exit()
        elif purpose == "Edit schedule":
            pass
        elif purpose == "Check courses status":
            term, departments = kfupm.KFUPM.get_term_and_department(interface=interface)
            searsh_filter = kfupm.KFUPM.get_search_filter(
                interface=interface, term=term
            )

            registrared = False
            while not registrared:
                courses_requested = kfupm.KFUPM.get_banner9_courses(
                    term=term, departments=departments
                )
                registrared = kfupm.KFUPM.check_for_changes(
                    content=courses_requested,
                    searsh_filter=searsh_filter,
                    configs_file=configs,
                )
                progress_bar(total_time=delay)


"'Too large to show contents. Max items to show: 300'"
main()
