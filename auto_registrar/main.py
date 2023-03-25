from pathlib import Path

from auto_registrar.config import SOUNDS_PATH, get_configs, write_configs_file
from auto_registrar.tui.ansi import AnsiColor
from auto_registrar.tui.bar import progress_bar
from auto_registrar.tui.colored_text import print_one_color_text
from auto_registrar.tui.questions import Questions
from auto_registrar.universities.kfupm.kfupm import KFUPM


def main() -> None:
    """The main and start function of the program.

    Args:
        None

    Returns:
        None
    """

    # Get local configuration
    configs: dict = get_configs()
    delay: int = configs["delay"]
    interface: str = configs["interface"]
    # username: str = configs["username"]
    # passcode: str = configs["passcode"]
    university: str = configs["university"]

    if configs["configured"]:
        purpose: str = Questions.list_question(
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
            write_configs_file(configs_contents=configs)
            get_configs(ask_for_configs=False)
        elif purpose == "Edit schedule":
            print_one_color_text(
                text_string="! Sorry, editing schedule is not supported currently!",
                text_color=AnsiColor.RED,
            )
            # term, departments  = KFUPM.get_term_and_departments(
            #     interface=interface
            # )
            # schedule = KFUPM_banner9.get_user_schedule(
            #     username=username, passcode=passcode, term=term
            # )
        elif purpose == "Check courses status":
            alarm_path: Path = SOUNDS_PATH.joinpath("alarm.mp3")

            term, departments = KFUPM.get_term_and_departments(
                interface=interface
            )
            search_filter: dict = KFUPM.get_search_filter(
                interface=interface, term=term, registration=False
            )

            finished: bool = False
            while not finished:
                courses_requested: list = KFUPM.get_courses(
                    term=term, departments=departments, interface=interface
                )
                finished = KFUPM.check_for_changes(
                    courses_strucured=courses_requested,
                    search_filter=search_filter,
                    interface=interface,
                    alarm_path=alarm_path,
                )
                progress_bar(total_time=delay)
