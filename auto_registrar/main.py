from auto_registrar.config import get_configs, write_config_file
from auto_registrar.tui.questions import Questions
from auto_registrar.tui.colored_text import print_one_color_text
from auto_registrar.tui.ansi import AnsiColor
from auto_registrar.universities.kfupm import KFUPM
from auto_registrar.tui.bar import progress_bar


def main() -> None:
    """The main the start of the program."""

    # Get local configuration
    configs = get_configs(ask_for_config=True)
    alarm_path = configs["alarm"]
    browser = configs["browser"]
    delay = configs["delay"]
    driver_path = configs["driver_path"]
    interface = configs["interface"]
    username = configs["username"]
    passcode = configs["passcode"]
    university = configs["university"]
    if configs["configured"]:
        purpose = Questions.list_question(
            question="What do you want to do in this run",
            choices=[
                "Reconfig configuration",
                "Edit schedule",
                "Check courses status",
            ],
        )
    else:
        purpose = "Reconfig configuration"

    if university == "kfupm":
        if purpose == "Reconfig configuration":
            configs["configured"] = False
            write_config_file(configs_file=configs)
            get_configs(ask_for_config=False)
            exit()
        elif purpose == "Edit schedule":
            print_one_color_text(
                text_string="Currently the instructors filter is not supported!",
                text_color=AnsiColor.RED,
            )
            exit()
            # term, departments = KFUPM.get_term_and_department(interface=interface)
            # schedule = KFUPM.get_schedule(
            #     username=username, passcode=passcode, term=term
            # )
        elif purpose == "Check courses status":
            term, departments, source = KFUPM.get_term_and_departments(interface=interface)
            search_filter = KFUPM.get_search_filter(interface=interface, term=term, registration=False)

            finished = False
            while not finished:
                courses_requested, source = KFUPM.get_courses(
                    term=term, departments=departments, interface=interface
                )
                finished = KFUPM.check_for_changes(
                    content=courses_requested,
                    search_filter=search_filter,
                    interface=interface,
                    source=source,
                    alarm_path=alarm_path,
                )
                progress_bar(total_time=delay)
    return
