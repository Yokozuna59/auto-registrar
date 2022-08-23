from cgi import print_arguments
from math import floor
from os import get_terminal_size
from sys import exit, stdout

from auto_registrar.tui.ansi import (
    AnsiColor,
    AnsiCursor,
    AnsiErase,
    AnsiKeys,
    AnsiStyle,
)
from auto_registrar.tui.colored_text import print_more_color_text, print_one_color_text
from auto_registrar.tui.readchars import read_one_char


class Questions:
    """A class contains different type of question."""

    def bool_question(question: str, default: bool = True) -> bool:
        """
        Ask user a boolean question.\n
        Returns answer as `bool`.
        """

        default_answer = "[Y/n]" if default == True else "[y/N]"

        correct_answer = False
        while not correct_answer:
            print_more_color_text(
                "?",
                AnsiColor.GREEN,
                question + "?",
                AnsiStyle.BOLD,
                default_answer,
                AnsiColor.DEFAULT,
                end_with=" ",
            )
            AnsiCursor.save_position()

            try:
                answer = input().lower()
            except KeyboardInterrupt:
                AnsiCursor.restore_position()
                AnsiCursor.move_left(len(question) + 10)
                AnsiErase.erase_entire_line()
                print_more_color_text(
                    "?",
                    AnsiStyle.FAINT,
                    question + "?",
                    AnsiColor.BOLD_LIGHT_GRAY,
                    "Cancelled by user",
                    AnsiColor.LIGHT_RED,
                )
                exit()

            if answer == "":
                answer = default
                correct_answer = True
            else:
                if answer == "y" or answer == "yes":
                    answer = True
                    correct_answer = True
                elif answer == "n" or answer == "no":
                    answer = False
                    correct_answer = True
                else:
                    print_more_color_text(
                        "! Sorry, your reply was invalid:",
                        AnsiColor.LIGHT_RED,
                        '"' + answer + '"',
                        AnsiStyle.BOLD,
                        "is not a valid answer, please try again.",
                        AnsiColor.LIGHT_RED,
                    )

        AnsiCursor.restore_position()
        AnsiCursor.move_left(6)
        AnsiErase.erase_line_to_end()
        print_one_color_text(
            text_string="Yes" if answer == True else "No",
            text_color=AnsiColor.LIGHT_BLUE,
        )
        return answer

    def str_questoin(question: str) -> str:
        """
        Ask user a string question.\n
        Returns answer as `str`.
        """
        print_more_color_text(
            "?",
            AnsiColor.GREEN,
            question + "?",
            AnsiStyle.BOLD,
            end_with=" ",
        )
        AnsiCursor.save_position()

        finished = False
        while not finished:
            try:
                answer = input()
            except KeyboardInterrupt:
                AnsiCursor.restore_position()
                AnsiCursor.move_left(len(question) + 4)
                AnsiErase.erase_entire_line()
                print_more_color_text(
                    "?",
                    AnsiStyle.FAINT,
                    question + "?",
                    AnsiColor.BOLD_LIGHT_GRAY,
                    "Cancelled by user",
                    AnsiColor.LIGHT_RED,
                )
                exit()

            if answer == "":
                AnsiCursor.restore_position()
            else:
                finished = True

        AnsiCursor.restore_position()
        AnsiErase.erase_line_to_end()
        print_one_color_text(text_string=answer, text_color=AnsiColor.BLUE)
        return answer

    def int_question(
        question: str, minimum: int = -1000000000, maximum: int = 1000000000
    ) -> int:
        """
        Ask user an integer question.\n
        Returns answer as `int`.
        """

        finished = False
        correct_answer = False
        while not finished:
            if not correct_answer:
                print_more_color_text(
                    "?",
                    AnsiColor.GREEN,
                    question + "?",
                    AnsiStyle.BOLD,
                    end_with=" ",
                )
                AnsiCursor.save_position()

            try:
                answer = input()
            except KeyboardInterrupt:
                AnsiCursor.restore_position()
                AnsiCursor.move_left(len(question) + 4)
                AnsiErase.erase_entire_line()
                print_more_color_text(
                    "?",
                    AnsiStyle.FAINT,
                    question + "?",
                    AnsiColor.BOLD_LIGHT_GRAY,
                    "Cancelled by user",
                    AnsiColor.LIGHT_RED,
                )
                exit()

            if answer == "":
                AnsiCursor.restore_position()
            else:
                try:
                    answer = int(answer)
                    if (answer >= minimum) and (answer <= maximum):
                        finished = True
                        correct_answer = True
                    else:
                        print_more_color_text(
                            "! Sorry, your reply was invalid:",
                            AnsiColor.LIGHT_RED,
                            '"%s"' % answer,
                            AnsiColor.DEFAULT,
                            "is out of range, please try again.",
                            AnsiColor.LIGHT_RED,
                        )
                except ValueError:
                    print_more_color_text(
                        "! Sorry, your reply was invalid:",
                        AnsiColor.LIGHT_RED,
                        '"%s"' % answer,
                        AnsiColor.DEFAULT,
                        "is not an integer, please try again.",
                        AnsiColor.LIGHT_RED,
                    )

        AnsiCursor.restore_position()
        AnsiErase.erase_line_to_end()
        print_one_color_text(text_string=answer, text_color=AnsiColor.BLUE)
        return answer

    def passcode_question(question: str) -> str:
        """
        Ask user a string question without printing what he wrote.\n
        Returns answer as `str`.
        """

        answer = ""
        letter = ""
        current_index = 0
        print_more_color_text(
            "?",
            AnsiColor.GREEN,
            question + "?",
            AnsiStyle.BOLD,
            end_with=" ",
        )
        AnsiCursor.save_position()
        print("\n(esc to make passcode visible)", end="")
        AnsiCursor.restore_position()

        visible = False
        finished = False
        while not finished:
            letter = read_one_char()

            if letter == AnsiKeys.ENTER:
                if answer != "":
                    AnsiCursor.restore_position()
                    AnsiErase.erase_line_to_end()
                    print_more_color_text(
                        "*" * len(answer),
                        AnsiColor.BLUE,
                    )
                    finished = True
            elif letter == AnsiKeys.CNTL_C:
                AnsiCursor.move_left(len(question) + 41)
                AnsiErase.erase_entire_line()
                print_more_color_text(
                    "?",
                    AnsiStyle.FAINT,
                    question + "?",
                    AnsiColor.BOLD_LIGHT_GRAY,
                    "Cancelled by user",
                    AnsiColor.LIGHT_RED,
                )
                AnsiErase.erase_entire_line()
                exit()
            elif letter.startswith(AnsiKeys.ESCAPE):
                if letter == AnsiKeys.ESCAPE:
                    AnsiCursor.restore_position()
                    AnsiErase.erase_line_to_end()

                    if not visible:
                        stdout.write(answer)
                        visible = True
                    else:
                        stdout.write("*" * len(answer))
                        visible = False
                    if current_index != len(answer):
                        AnsiCursor.move_right(current_index)
                elif (letter == AnsiKeys.ARROW_LEFT) and (current_index != 0):
                    AnsiCursor.move_left()
                    current_index -= 1
                elif (letter == AnsiKeys.ARROW_RIGHT) and (
                    current_index != len(answer)
                ):
                    AnsiCursor.move_right()
                    current_index += 1
                elif letter == AnsiKeys.HOME:
                    current_index = 0
                    AnsiCursor.restore_position()
                elif (letter == AnsiKeys.END) and (current_index != 0):
                    AnsiCursor.restore_position()
                    AnsiCursor.move_right(len(answer))
                elif letter == AnsiKeys.DELETE:
                    answer = AnsiErase.delete(
                        user_input=answer, index=current_index, passcode=not visible
                    )
            elif letter == AnsiKeys.BACKSPACE:
                answer = AnsiErase.backspace(
                    user_input=answer, index=current_index, passcode=not visible
                )
                current_index -= 1
            else:
                answer = answer[:current_index] + letter + answer[current_index:]
                current_index += 1
                if current_index == len(answer):
                    if visible:
                        stdout.write(letter)
                    else:
                        stdout.write("*")
                else:
                    if visible:
                        stdout.write(answer[current_index - 1 :])
                    else:
                        stdout.write("*" * (len(answer[current_index - 1 :])))
                    AnsiCursor.restore_position()
                    AnsiCursor.move_left(current_index)
        return answer

    def list_question(question: str, choices: list) -> str:
        """
        Ask user to select an answer.\n
        return the answer as `str` type.
        """

        current_letter = ""
        word = ""
        all_choices = choices.copy()

        AnsiCursor.hide()
        print_more_color_text(
            "?",
            AnsiColor.GREEN,
            question + "?",
            AnsiStyle.BOLD,
            end_with=" ",
        )
        AnsiCursor.save_position()
        stdout.write(AnsiKeys.NEW_LINE)

        finished = False
        while not finished:
            terminal_columns, terminal_rows = get_terminal_size()
            question_lines = (
                (len(question) + 41)
                - terminal_columns * floor(len(question) + 41) / terminal_columns
                + 1
            )

            if question_lines == 1:
                line_gap = 0
            elif question_lines > 36 and question_lines <= terminal_columns:
                line_gap = 1

            AnsiCursor.restore_position()
            AnsiCursor.move_right(len(word))
            print_one_color_text(
                text_string=" [Use arrows to move, type to filter]",
                text_color=AnsiColor.BLUE,
                end_with="",
            )

            AnsiCursor.restore_position()

            if (current_letter != AnsiKeys.ARROW_UP) and (
                current_letter != AnsiKeys.ARROW_DOWN
            ):
                list_lenght = 0
                choices = []
                AnsiCursor.restore_position()
                AnsiCursor.move_next_line(line_gap + 1)

                printable = True
                for choice in all_choices:
                    if word.lower() in choice.lower():
                        list_lenght += 1
                        choices.append(choice)
                        if list_lenght < terminal_rows:
                            AnsiErase.erase_entire_line()
                            if list_lenght == 1:
                                print_one_color_text(
                                    text_string=f"> {choice}", text_color=AnsiColor.BLUE
                                )
                                answer = choice
                            else:
                                # TODO: edit when list length is as same as list length (quesion disappear)
                                print_one_color_text(
                                    text_string=f"  {choice}", text_color=AnsiStyle.BOLD
                                )
                        else:
                            printable = False
                if not printable:
                    print_one_color_text(
                        text_string="  " + "v" * (len(question) + 1),
                        text_color=AnsiColor.LIGHT_GREEN,
                        end_with="",
                    )

                current_index = 0

            AnsiCursor.restore_position()
            AnsiCursor.move_right(len(word))
            current_letter = read_one_char()

            if current_letter.startswith("\x1B"):
                if current_letter == AnsiKeys.ARROW_UP and list_lenght != 0:
                    AnsiCursor.move_next_line(current_index + line_gap + 1)
                    AnsiErase.erase_entire_line()

                    print_one_color_text(
                        text_string=f"  {choices[current_index]}",
                        text_color=AnsiStyle.BOLD,
                        end_with="",
                    )

                    if current_index == 0:
                        current_index = list_lenght - 1
                    else:
                        current_index -= 1

                    AnsiCursor.restore_position()

                    AnsiCursor.move_next_line(current_index + line_gap + 1)
                    AnsiErase.erase_entire_line()

                    print_one_color_text(
                        text_string=f"> {choices[current_index]}",
                        text_color=AnsiColor.LIGHT_BLUE,
                        end_with="",
                    )

                    answer = choices[current_index]
                elif current_letter == AnsiKeys.ARROW_DOWN and list_lenght != 0:
                    AnsiCursor.move_next_line(current_index + line_gap + 1)
                    AnsiErase.erase_entire_line()

                    print_one_color_text(
                        text_string=f"  {choices[current_index]}",
                        text_color=AnsiStyle.BOLD,
                        end_with="",
                    )

                    AnsiCursor.restore_position()

                    if current_index == list_lenght - 1:
                        current_index = 0
                    else:
                        current_index += 1

                    AnsiCursor.move_next_line(current_index + line_gap + 1)
                    AnsiErase.erase_entire_line()

                    print_one_color_text(
                        text_string=f"> {choices[current_index]}",
                        text_color=AnsiColor.LIGHT_BLUE,
                        end_with="",
                    )
                    answer = choices[current_index]
            elif current_letter == AnsiKeys.ENTER:
                if list_lenght != 0:
                    for _ in range(list_lenght + line_gap + 1):
                        AnsiCursor.move_next_line()
                        AnsiErase.erase_entire_line()
                    AnsiCursor.restore_position()
                    print_one_color_text(
                        text_string=answer, text_color=AnsiColor.BLUE, end_with=""
                    )
                    AnsiErase.erase_line_to_end()
                    AnsiCursor.show()
                    AnsiCursor.move_next_line()
                    finished = True
            elif current_letter == AnsiKeys.CNTL_C:
                AnsiCursor.move_left(len(question) + 41)
                AnsiErase.erase_entire_line()
                print_more_color_text(
                    "?",
                    AnsiStyle.FAINT,
                    question + "?",
                    AnsiColor.BOLD_LIGHT_GRAY,
                    "Cancelled by user",
                    AnsiColor.LIGHT_RED,
                )
                AnsiCursor.save_position()
                for _ in choices:
                    AnsiErase.erase_entire_line()
                    AnsiCursor.move_next_line()
                AnsiCursor.restore_position()
                AnsiCursor.show()
                exit()
            else:
                if current_letter == AnsiKeys.BACKSPACE:
                    word = AnsiErase.backspace(
                        user_input=word, index=current_index + 1, passcode=False
                    )
                else:
                    word += current_letter
                for _ in range(list_lenght + 1):
                    AnsiCursor.move_next_line()
                    AnsiErase.erase_entire_line()
                AnsiCursor.restore_position()
                AnsiErase.erase_line_to_end()
                stdout.write(word)
        return answer

    def dict_question(question: str, choices: dict) -> str:
        """
        Ask user to select an answer.\n
        return the answer's value as `str` type.
        """

        answer = Questions.list_question(
            question=question, choices=list(choices.keys())
        )
        choice_value = choices[answer]
        return choice_value

    def mcq_list_question(question: str, choices: list) -> list:
        """
        Ask user to select an/multi answer/s.\n
        return the answer as `list` type.
        """

        letter = ""
        answers = []
        AnsiCursor.hide()
        print_more_color_text(
            "?",
            AnsiColor.GREEN,
            question + "?",
            AnsiStyle.BOLD,
            "(<up> & <down> to move, <space> to select, <a> to toggle)",
            AnsiColor.BLUE,
            end_with="",
        )
        AnsiCursor.save_position()
        AnsiCursor.move_next_line()

        for index, choice in enumerate(choices):
            if index == 0:
                print_more_color_text(
                    ">", AnsiColor.BLUE, "○", AnsiStyle.BOLD, choice, AnsiColor.BLUE
                )
            else:
                print_one_color_text(
                    text_string=f"  ○ {choice}", text_color=AnsiStyle.BOLD
                )
        current_index = 1

        finished = False
        while not finished:
            AnsiCursor.restore_position()
            letter = read_one_char()

            if letter == AnsiKeys.ARROW_UP:
                AnsiCursor.move_next_line(current_index)
                AnsiErase.erase_entire_line()
                current_index -= 1
                print_one_color_text(
                    text_string="  {} {}".format(
                        "●" if choices[current_index] in answers else "○",
                        choices[current_index],
                    ),
                    text_color=AnsiStyle.BOLD,
                )

                AnsiCursor.restore_position()

                if current_index == 0:
                    current_index = len(choices)
                    AnsiCursor.move_next_line(current_index)
                else:
                    AnsiCursor.move_next_line(current_index)

                AnsiErase.erase_entire_line()

                print_more_color_text(
                    ">",
                    AnsiColor.LIGHT_BLUE,
                    "●" if choices[current_index - 1] in answers else "○",
                    AnsiStyle.BOLD,
                    choices[current_index - 1],
                    AnsiColor.BLUE,
                    end_with="",
                )
            elif letter == AnsiKeys.ARROW_DOWN:
                AnsiCursor.move_next_line(current_index)
                AnsiErase.erase_entire_line()

                print_one_color_text(
                    text_string="  {} {}".format(
                        "●" if choices[current_index - 1] in answers else "○",
                        choices[current_index - 1],
                    ),
                    text_color=AnsiStyle.BOLD,
                )

                AnsiCursor.restore_position()

                if current_index == len(choices):
                    current_index = 1
                else:
                    current_index += 1

                AnsiCursor.move_next_line(current_index)
                AnsiErase.erase_entire_line()

                print_more_color_text(
                    ">",
                    AnsiColor.LIGHT_BLUE,
                    "●" if choices[current_index - 1] in answers else "○",
                    AnsiStyle.BOLD,
                    choices[current_index - 1],
                    AnsiColor.BLUE,
                    end_with="",
                )
            elif letter == AnsiKeys.ENTER:
                if len(answers) != 0:
                    AnsiCursor.move_left(58)
                    AnsiErase.erase_line_to_end()
                    AnsiCursor.save_position()

                    print_one_color_text(
                        text_string=f"({str(len(answers))} answers selected)",
                        text_color=AnsiColor.LIGHT_BLUE,
                        end_with="",
                    )

                    for _ in f"{choices} ":
                        AnsiCursor.move_next_line()
                        AnsiErase.erase_line_to_end()

                    AnsiCursor.restore_position()
                    AnsiCursor.show()
                    AnsiCursor.move_next_line()
                    finished = True
            elif letter == AnsiKeys.CNTL_C:
                AnsiCursor.move_left(len(question) + 62)
                AnsiErase.erase_entire_line()

                print_more_color_text(
                    "?",
                    AnsiStyle.FAINT,
                    question + "?",
                    AnsiColor.BOLD_LIGHT_GRAY,
                    "Cancelled by user",
                    AnsiColor.LIGHT_RED,
                    end_with="",
                )

                AnsiCursor.save_position()

                for _ in choices:
                    AnsiCursor.move_next_line()
                    AnsiErase.erase_entire_line()

                AnsiCursor.restore_position()
                AnsiCursor.move_next_line()
                AnsiCursor.show()
                exit()
            elif letter == " ":
                AnsiCursor.move_next_line(current_index)
                AnsiErase.erase_entire_line()
                if choices[current_index - 1] in answers:
                    stdout.write(
                        "{}>{} {}{} {}{}".format(
                            AnsiColor.LIGHT_BLUE,
                            AnsiStyle.RESET_ALL,
                            AnsiColor.LIGHT_BLUE,
                            "○",
                            choices[current_index - 1],
                            AnsiStyle.RESET_ALL,
                        )
                    )
                    answers.remove(choices[current_index - 1])
                else:
                    print_more_color_text(
                        ">",
                        AnsiColor.LIGHT_BLUE,
                        "●",
                        AnsiStyle.BOLD,
                        choices[current_index - 1],
                        AnsiColor.LIGHT_BLUE,
                        end_with="",
                    )
                    answers.append(choices[current_index - 1])
            elif letter == "a":
                for index, choice in enumerate(choices):
                    AnsiCursor.move_next_line()
                    AnsiErase.erase_entire_line()
                    if index == current_index - 1:
                        print_more_color_text(
                            ">",
                            AnsiColor.LIGHT_BLUE,
                            "○" if len(answers) == len(choices) else "●",
                            AnsiStyle.BOLD,
                            choice,
                            AnsiColor.LIGHT_BLUE,
                            end_with="",
                        )
                    else:
                        print_one_color_text(
                            text_string="  {} {}".format(
                                "○" if len(answers) == len(choices) else "●",
                                choice,
                            ),
                            text_color=AnsiStyle.BOLD,
                            end_with="",
                        )
                answers = [] if len(answers) == len(choices) else choices.copy()
                AnsiCursor.restore_position()
        return answers

    def mcq_dict_question(question: str, choices: dict) -> list:
        """
        Ask user to select an/multi answer/s.\n
        return the answers' values as `list` type.
        """

        answers = Questions.mcq_list_question(
            question=question, choices=list(choices.keys())
        )
        answers_value = []
        for answer in answers:
            answers_value.append(choices[answer])
        return answers_value


# tt1 = Questions.bool_question(question="Sample boolean question", default=True)
# tt2 = Questions.str_questoin(question="Sample string question")
# tt3 = Questions.int_question(question="Sample integer quesion", minimum=10000, maximum=19999)
# tt4 = Questions.passcode_question(question="Sample passcode quesion")
# tt5 = Questions.list_question(
#     question="Sample list question",
#     choices=["Apple", "Banana", "Potato", "TT", "Orange"],
# )
print
