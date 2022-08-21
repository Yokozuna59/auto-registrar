from auto_registrar.config import get_configs, ALARM_PATH, write_config_file
from auto_registrar.tui.questions import Questions
from auto_registrar.tui.colored_text import print_one_color_text
from auto_registrar.tui.ansi import AnsiColor
from auto_registrar.universities.kfupm import KFUPM, KFUPM_banner9
from auto_registrar.tui.bar import progress_bar


def main() -> None:
    """The main the start of the program."""

    # Get local configuration
    configs = get_configs(ask_for_config=True)
    alarm_path = ALARM_PATH.joinpath(configs["alarm"])
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
                text_string="Currently the edit schedule is not supported!",
                text_color=AnsiColor.RED,
            )
            exit()
            # term, departments  = KFUPM.get_term_and_departments(
            #     interface=interface
            # )
            # schedule = KFUPM_banner9.get_user_schedule(
            #     username=username, passcode=passcode, term=term
            # )
        elif purpose == "Check courses status":
            term, departments = KFUPM.get_term_and_departments(interface=interface)
            search_filter = KFUPM.get_search_filter(
                interface=interface, term=term, registration=False
            )

            finished = False
            while not finished:
                courses_requested = KFUPM.get_courses(
                    term=term, departments=departments, interface=interface
                )
                finished = KFUPM.check_for_changes(
                    courses_strucured=courses_requested,
                    search_filter=search_filter,
                    interface=interface,
                    alarm_path=alarm_path,
                )
                progress_bar(total_time=delay)
    return
