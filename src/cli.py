# import functions from modules
from sys import stdout, exit
from readchar import readchar
from os import get_terminal_size
from math import ceil, floor
from time import sleep

class AnsiEscapeCodes:
    # Keys
    NEW_LINE                    = "\n"
    CNTL                        = "\x1B"
    CNTL_C                      = "\x03"
    ENTER                       = "\r"
    DELETE                      = "\x7f"
    ESCAPE                      = "\x1b"

    # Modes
    RESET                       = "\x1B[0m"
    BOLD                        = "\x1B[1m"
    FAINT                       = "\x1B[2m"
    ITALIC_TEXT                 = "\x1B[3m"
    UNDERSCORE                  = "\x1B[4m"
    BLINK                       = "\x1B[5m"

    # Colors
    RED                         = "\x1B[31m"
    GREEN                       = "\x1B[32m"
    YELLOW                      = "\x1B[33m"
    BLUE                        = "\x1B[34m"
    MAGENTA                     = "\x1B[35m"
    CYAN                        = "\x1B[36m"
    LIGHT_GRAY                  = "\x1B[90m"
    LIGHT_RED                   = "\x1B[91m"
    LIGHT_GREEN                 = "\x1B[92m"
    LIGHT_YELLOW                = "\x1B[93m"
    LIGHT_BLUE                  = "\x1B[94m"
    LIGHT_MAGENTA               = "\x1B[95m"
    LIGHT_CYAN                  = "\x1B[96m"

    # Cursor Control
    HIDE_CURSOR                 = "\x1B[?25l"
    SHOW_CURSOR                 = "\x1B[?25h"
    SAVE_POSITION               = "\x1B7\x1B[s"
    RESTORE_POSITION            = "\x1B8\x1B[u"

    # Cursor Movement
    MOVE_UP                     = "\x1B[A"
    MOVE_DOWN                   = "\x1B[B"
    MOVE_LEFT                   = "\x1B[1D"
    MOVE_RIGHT                  = "\x1B[1C"
    MOVE_TO_BEGIN_OF_NEXT_LINE  = "\x1B[1E"

    # Erase
    ERASE_TO_END_OF_LINE        = "\x1B[0K"
    ERASE_ENTIRE_LINE           = "\x1B[2K"

class Questions:
    """
    A class contains different type of question.
    """

    def bool_question(question: str, default: bool = True) -> bool:
        """
        Ask user a boolean question.\n
        Return the answer as `bool` type if he answered correctly.
        """

        default_answer = "[Y/n]" if default == True else "[y/N]"

        correct_answer = False
        while not correct_answer:
            stdout.write(f"{AnsiEscapeCodes.GREEN}?{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}{question}?{AnsiEscapeCodes.RESET} {default_answer} ")
            stdout.write(AnsiEscapeCodes.SAVE_POSITION)

            try:
                answer = input().lower()
            except KeyboardInterrupt:
                stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                stdout.write(AnsiEscapeCodes.MOVE_LEFT * (len(question) + 10))
                stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                stdout.write(f"{AnsiEscapeCodes.FAINT}?{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}\x1b[38;2;175;175;175m{question}?{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.RED}Cancelled by user{AnsiEscapeCodes.RESET}{AnsiEscapeCodes.NEW_LINE}")
                exit()

            if (answer == ""):
                answer = default
                correct_answer = True
            else:
                if (answer == "y" or answer == "yes"):
                    answer = True
                    correct_answer = True
                elif (answer == "n" or answer == "no"):
                    answer = False
                    correct_answer = True
                else:
                    stdout.write(f"{AnsiEscapeCodes.RED}! Sorry, your reply was invalid:{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}\"{answer}\"{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.RED}is not a valid answer, please try again.{AnsiEscapeCodes.RESET}{AnsiEscapeCodes.NEW_LINE}")

        stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
        stdout.write(AnsiEscapeCodes.MOVE_LEFT * 6)
        stdout.write(AnsiEscapeCodes.ERASE_TO_END_OF_LINE)
        stdout.write("{}{}{}{}".format(AnsiEscapeCodes.BLUE, "Yes" if answer == True else "No", AnsiEscapeCodes.RESET, AnsiEscapeCodes.NEW_LINE))
        stdout.flush()
        return answer

    def str_questoin(question: str) -> str:
        """
        Ask user a string question.\n
        Return the answer as `str` type.
        """

        stdout.write(f"{AnsiEscapeCodes.GREEN}?{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}{question}?{AnsiEscapeCodes.RESET} ")
        stdout.write(AnsiEscapeCodes.SAVE_POSITION)

        finished = False
        while not finished:
            try:
                answer = input()
            except KeyboardInterrupt:
                stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                stdout.write(AnsiEscapeCodes.MOVE_LEFT * (len(question) + 4))
                stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                stdout.write(f"{AnsiEscapeCodes.FAINT}?{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}\x1b[38;2;175;175;175m{question}?{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.RED}Cancelled by user{AnsiEscapeCodes.RESET}{AnsiEscapeCodes.NEW_LINE}")
                exit()

            if (answer == ""):
                stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
            else:
                finished = True

        stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
        stdout.write(AnsiEscapeCodes.ERASE_TO_END_OF_LINE)
        stdout.write(f"{AnsiEscapeCodes.BLUE}{answer}{AnsiEscapeCodes.RESET}{AnsiEscapeCodes.NEW_LINE}")
        stdout.flush()
        return answer

    def int_question(question: str, minimum: int = -1000000000000000, maximum: int = 1000000000000000) -> int:
        """
        Ask user an integer question.\n
        Return the answer as `int` type.
        """

        stdout.write(f"{AnsiEscapeCodes.GREEN}?{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}{question}?{AnsiEscapeCodes.RESET} ")
        stdout.write(AnsiEscapeCodes.SAVE_POSITION)

        correct_answer = False
        while not correct_answer:
            try:
                answer = input()
            except KeyboardInterrupt:
                stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                stdout.write(AnsiEscapeCodes.MOVE_LEFT * (len(question) + 4))
                stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                stdout.write(f"{AnsiEscapeCodes.FAINT}?{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}\x1b[38;2;175;175;175m{question}?{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.RED}Cancelled by user{AnsiEscapeCodes.RESET}{AnsiEscapeCodes.NEW_LINE}")
                exit()

            answer = input()
            if (answer == ""):
                stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
            else:
                try:
                    answer = int(answer)
                    if ((answer >= minimum) and (answer <= maximum)):
                        correct_answer = True
                    else:
                        stdout.write(f"{AnsiEscapeCodes.RED}! Sorry, your reply was invalid:{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}\"{answer}\"{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.RED}is out of range, please try again.{AnsiEscapeCodes.RESET}{AnsiEscapeCodes.NEW_LINE}")
                except ValueError:
                    stdout.write(f"{AnsiEscapeCodes.RED}! Sorry, your reply was invalid:{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}\"{answer}\"{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.RED}is not a valid answer, please try again.{AnsiEscapeCodes.RESET}{AnsiEscapeCodes.NEW_LINE}")

        stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
        stdout.write(AnsiEscapeCodes.ERASE_TO_END_OF_LINE)
        stdout.write(f"{AnsiEscapeCodes.BLUE}{answer}{AnsiEscapeCodes.RESET}{AnsiEscapeCodes.NEW_LINE}")
        stdout.flush()
        return answer

    def passcode_question(question: str) -> str:
        """
        Ask user a string question without printing what he wrote.\n
        return the answer as `str` type.
        """

        answer = ""
        letter = ""
        stdout.write(AnsiEscapeCodes.HIDE_CURSOR)
        stdout.write(f"{AnsiEscapeCodes.GREEN}?{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}{question}?{AnsiEscapeCodes.RESET} (Press Esc to make passcode visible) ")
        stdout.write(AnsiEscapeCodes.SAVE_POSITION)

        visibility = False
        finished = False
        while not finished:
            stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
            stdout.flush()

            letter = readchar()
            if (letter == AnsiEscapeCodes.ENTER):
                if (answer != ""):
                    stdout.write(AnsiEscapeCodes.ERASE_TO_END_OF_LINE)
                    stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                    stdout.write("{}{}{}{}".format(AnsiEscapeCodes.BLUE, "*" * len(answer), AnsiEscapeCodes.RESET, AnsiEscapeCodes.NEW_LINE))
                    stdout.flush()
                    finished = True
            elif (letter == AnsiEscapeCodes.CNTL_C):
                stdout.write(AnsiEscapeCodes.MOVE_LEFT * (len(question) + 41))
                stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                stdout.write(f"{AnsiEscapeCodes.FAINT}?{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}\x1b[38;2;175;175;175m{question}?{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.RED}Cancelled by user{AnsiEscapeCodes.RESET}{AnsiEscapeCodes.NEW_LINE}")
                stdout.flush()
                stdout.write(AnsiEscapeCodes.SHOW_CURSOR)
                exit()
            elif (letter == AnsiEscapeCodes.ESCAPE):
                stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                stdout.write(AnsiEscapeCodes.ERASE_TO_END_OF_LINE)

                if not visibility:
                    stdout.write(answer)
                    visibility = True
                else:
                    stdout.write("*" * len(answer))
                    visibility = False
            else:
                if (letter == AnsiEscapeCodes.DELETE):
                    if (answer != ""):
                        stdout.write(AnsiEscapeCodes.MOVE_LEFT)
                        answer = answer[:-1]
                else:
                    answer += letter
                stdout.write(AnsiEscapeCodes.ERASE_TO_END_OF_LINE)
                stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                if (visibility):
                    stdout.write(answer)
                else:
                    stdout.write("*" * len(answer))
        stdout.write(AnsiEscapeCodes.SHOW_CURSOR)
        return answer

    def list_question(question: str, choices: list) -> str:
        """
        Ask user to select an answer.\n
        return the answer as `str` type.
        """

        word = ""
        letter = ""
        ALL_CHOICES = choices.copy()
        stdout.write(AnsiEscapeCodes.HIDE_CURSOR)
        stdout.write(f"{AnsiEscapeCodes.GREEN}?{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}{question}?{AnsiEscapeCodes.RESET} ")
        stdout.write(AnsiEscapeCodes.SAVE_POSITION)

        finished = False
        while not finished:
            stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
            terminal_columns = get_terminal_size()[0]
            question_lines = (len(question)+41)-(terminal_columns)*floor((len(question)+41)/terminal_columns)+1
            line_gap = 0 if (question_lines == 1) else 0 if (question_lines > 36 and question_lines <= terminal_columns) else 1
            stdout.write(f"{AnsiEscapeCodes.BLUE} [Use arrows to move, type to filter]{AnsiEscapeCodes.RESET}")

            if ((letter != AnsiEscapeCodes.MOVE_UP) and (letter != AnsiEscapeCodes.MOVE_DOWN)):
                list_lenght = 0
                choices = []
                stdout.write(AnsiEscapeCodes.NEW_LINE * (len(choices)))
                stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE) if line_gap == 1 else None

                for index, choice in enumerate(ALL_CHOICES):
                    if (word.lower() in choice.lower()):
                        list_lenght += 1
                        choices.append(choice)
                        stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE)
                        stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                        if (list_lenght == 1):
                            stdout.write(f"{AnsiEscapeCodes.BLUE}> {choice}{AnsiEscapeCodes.RESET}")
                            answer = choice
                        else:
                            stdout.write(f"{AnsiEscapeCodes.BOLD}  {choice}{AnsiEscapeCodes.RESET}")
                index = 1

            stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
            stdout.flush()
            letter = readchar()

            if (letter == AnsiEscapeCodes.CNTL):
                letter += readchar() + readchar()
                if (letter == AnsiEscapeCodes.MOVE_UP and list_lenght != 0):
                    stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE * (index + line_gap))
                    index -= 1
                    stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                    stdout.write(f"{AnsiEscapeCodes.BOLD}  {choices[index]}{AnsiEscapeCodes.RESET}")
                    stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                    if (index == 0):
                        index = list_lenght
                        stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE * (index + line_gap))
                    else:
                        stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE * (index + line_gap))
                    stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                    stdout.write(f"{AnsiEscapeCodes.BLUE}> {choices[index - 1]}{AnsiEscapeCodes.RESET}")
                    answer = choices[index - 1]
                elif (letter == AnsiEscapeCodes.MOVE_DOWN and list_lenght != 0):
                    stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE * (index + line_gap))
                    stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                    stdout.write(f"{AnsiEscapeCodes.BOLD}  {choices[index - 1]}{AnsiEscapeCodes.RESET}")
                    stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                    if (index == list_lenght):
                        index = 1
                    else:
                        index += 1
                    stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE * (index + line_gap))
                    stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                    stdout.write(f"{AnsiEscapeCodes.BLUE}> {choices[index - 1]}{AnsiEscapeCodes.RESET}")
                    answer = choices[index - 1]
            elif (letter == AnsiEscapeCodes.ENTER):
                if (list_lenght != 0):
                    stdout.write(AnsiEscapeCodes.SAVE_POSITION)
                    stdout.write(AnsiEscapeCodes.ERASE_TO_END_OF_LINE)
                    stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE)
                    stdout.write(AnsiEscapeCodes.ERASE_TO_END_OF_LINE)
                    stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                    stdout.write(f"{AnsiEscapeCodes.BLUE}{answer}{AnsiEscapeCodes.RESET}")
                    stdout.write(AnsiEscapeCodes.SAVE_POSITION)
                    for _ in range(list_lenght+line_gap):
                        stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE)
                        stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                    stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                    stdout.write(AnsiEscapeCodes.SHOW_CURSOR)
                    stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE)
                    stdout.flush()
                    finished = True
            elif (letter == AnsiEscapeCodes.CNTL_C):
                stdout.write(AnsiEscapeCodes.MOVE_LEFT * (len(question) + 41))
                stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                stdout.write(f"{AnsiEscapeCodes.FAINT}?{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}\x1b[38;2;175;175;175m{question}?{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.RED}Cancelled by user{AnsiEscapeCodes.RESET}")
                stdout.write(AnsiEscapeCodes.SAVE_POSITION)
                for _ in choices:
                    stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE)
                    stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE)
                stdout.write(AnsiEscapeCodes.HIDE_CURSOR)
                stdout.flush()
                exit()
            else:
                if (letter == AnsiEscapeCodes.DELETE):
                    if (word != ""):
                        stdout.write(AnsiEscapeCodes.MOVE_LEFT)
                        word = word[:-1]
                else:
                    word += letter
                for _ in range(list_lenght+1):
                    stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE)
                    stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                stdout.write(AnsiEscapeCodes.ERASE_TO_END_OF_LINE)
                stdout.write(word)
        return answer

    def dict_question(question: str, choices: dict) -> str:
        """
        Ask user to select an answer.\n
        return the answer's value as `str` type.
        """

        answer = Questions.list_question(question=question, choices=list(choices.keys()))
        choice_value = choices[answer]
        return choice_value

    def mcq_list_question(question: str, choices: list) -> list:
        """
        Ask user to select an/multi answer/s.\n
        return the answer as `list` type.
        """

        letter = ""
        answers = []
        stdout.write(AnsiEscapeCodes.HIDE_CURSOR)
        stdout.write(f"{AnsiEscapeCodes.LIGHT_GREEN}?{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}{question}{AnsiEscapeCodes.RESET}? {AnsiEscapeCodes.BLUE} (<up> & <down> to move, <space> to select, <a> to toggle){AnsiEscapeCodes.RESET}")
        stdout.write(AnsiEscapeCodes.SAVE_POSITION)

        for index, choice in enumerate(choices):
            stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE)
            if (index == 0):
                stdout.write(f"{AnsiEscapeCodes.BLUE}>{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}○{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BLUE}{choice}{AnsiEscapeCodes.RESET}")
            else:
                stdout.write(f"  {AnsiEscapeCodes.BOLD}○ {choice}{AnsiEscapeCodes.RESET}")
        index = 1

        finished = False
        while not finished:
            stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
            stdout.flush()
            letter = readchar()

            if (letter == AnsiEscapeCodes.CNTL):
                letter += readchar() + readchar()

                if (letter == AnsiEscapeCodes.MOVE_UP):
                    stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE * index)
                    stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                    index -= 1
                    stdout.write("  {}{} {}{}".format(AnsiEscapeCodes.BOLD,"●" if choices[index] in answers else "○", choices[index], AnsiEscapeCodes.RESET))
                    stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                    if (index == 0):
                        index = len(choices)
                        stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE * index)
                    else:
                        stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE * index)
                    stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                    stdout.write("{}>{} {}{} {}{}".format(AnsiEscapeCodes.LIGHT_BLUE, AnsiEscapeCodes.RESET, AnsiEscapeCodes.LIGHT_BLUE, "●"  if choices[index-1] in answers else "○", choices[index-1], AnsiEscapeCodes.RESET))
                elif (letter == AnsiEscapeCodes.MOVE_DOWN):
                    stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE * index)
                    stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                    stdout.write("{}  {} {}{}".format(AnsiEscapeCodes.BOLD, "●"  if choices[index - 1] in answers else "○", choices[index - 1], AnsiEscapeCodes.RESET))
                    stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                    if (index == len(choices)):
                        index = 1
                    else:
                        index += 1
                    stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE * index)
                    stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                    stdout.write("{}>{} {}{} {}{}".format(AnsiEscapeCodes.LIGHT_BLUE, AnsiEscapeCodes.RESET, AnsiEscapeCodes.LIGHT_BLUE, "●"  if choices[index - 1] in answers else "○", choices[index - 1], AnsiEscapeCodes.RESET))
            elif (letter == AnsiEscapeCodes.ENTER):
                if (len(answers) != 0):
                    stdout.write(AnsiEscapeCodes.MOVE_LEFT * 58)
                    stdout.write(AnsiEscapeCodes.ERASE_TO_END_OF_LINE)
                    stdout.write(AnsiEscapeCodes.SAVE_POSITION)
                    stdout.write("{}({} answers selected){}".format(AnsiEscapeCodes.LIGHT_BLUE, str(len(answers)), AnsiEscapeCodes.RESET))
                    for _ in f"{choices} ":
                        stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE)
                        stdout.write(AnsiEscapeCodes.ERASE_TO_END_OF_LINE)
                    stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                    stdout.write(AnsiEscapeCodes.SHOW_CURSOR)
                    stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE)
                    stdout.flush()
                    finished = True
            elif (letter == AnsiEscapeCodes.CNTL_C):
                stdout.write(AnsiEscapeCodes.MOVE_LEFT * (len(question) + 62))
                stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                stdout.write(f"{AnsiEscapeCodes.FAINT}?{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}\x1b[38;2;175;175;175m{question}?{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.RED}Cancelled by user{AnsiEscapeCodes.RESET}{AnsiEscapeCodes.NEW_LINE}")
                stdout.write(AnsiEscapeCodes.SAVE_POSITION)
                for _ in choices:
                    stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE)
                    stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE)
                stdout.write(AnsiEscapeCodes.HIDE_CURSOR)
                stdout.flush()
                exit()
            elif (letter == " "):
                stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE * index)
                stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                if (choices[index - 1] in answers):
                    stdout.write("{}>{} {}{} {}{}".format(AnsiEscapeCodes.LIGHT_BLUE, AnsiEscapeCodes.RESET, AnsiEscapeCodes.LIGHT_BLUE, "○", choices[index - 1], AnsiEscapeCodes.RESET))
                    answers.remove(choices[index - 1])
                else:
                    stdout.write("{}>{} {}{} {}{}".format(AnsiEscapeCodes.LIGHT_BLUE, AnsiEscapeCodes.RESET, AnsiEscapeCodes.LIGHT_BLUE, "●", choices[index - 1], AnsiEscapeCodes.RESET))
                    answers.append(choices[index - 1])
            elif (letter == "a"):
                current_index = index
                for index, choice in enumerate(choices):
                    stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE)
                    stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                    if (current_index == (index + 1)):
                        stdout.write("{}>{} {}{}{} {}{}{}".format(AnsiEscapeCodes.LIGHT_BLUE, AnsiEscapeCodes.RESET, AnsiEscapeCodes.BOLD, "○" if len(answers) == len(choices) else "●", AnsiEscapeCodes.RESET, AnsiEscapeCodes.LIGHT_BLUE,choice, AnsiEscapeCodes.RESET))
                    else:
                        stdout.write("  {}{} {}{}".format(AnsiEscapeCodes.BOLD ,"○" if len(answers) == len(choices) else "●", choice, AnsiEscapeCodes.RESET))
                answers = [] if len(answers) == len(choices) else choices.copy()
                index = current_index
                stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
        return answers

    def mcq_dict_question(question: str, choices: dict) -> list:
        """
        Ask user to select an/multi answer/s.\n
        return the answers' values as `list` type.
        """

        answers = Questions.mcq_list_question(question=question, choices=list(choices.keys()))
        answers_value = []
        for answer in answers:
            answers_value.append(choices[answer])
        return answers_value

def print_colorful_text(text_string: str, text_color: str, end_with = AnsiEscapeCodes.NEW_LINE) -> str:
    """
    Print colorful text.\n
    Return `None` after printing.
    """

    stdout.write(f"{text_color}{text_string}{AnsiEscapeCodes.RESET}{end_with}")
    return None

def progress_bar(total_time: int) -> None:
    """
    Print a progress bar with a total time.\n
    Return `None` after that.
    """

    stdout.write(AnsiEscapeCodes.HIDE_CURSOR)
    stdout.write(AnsiEscapeCodes.SAVE_POSITION)

    columns = list(get_terminal_size())[0]-15
    current_columns = columns

    for i in range(1, total_time+1):
        if (current_columns != columns):
            lines = ceil(current_columns/columns) if (current_columns > columns) else ceil(columns/current_columns)
            for _ in range(lines):
                stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE)
            current_columns = columns
        stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
        stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)

        if (i == 1):
            stdout.write("Next Refresh: |{}|".format(" " * (columns-1)))
        else:
            stdout.write("Next Refresh: |{}".format("█" * (floor(columns * (i/total_time))-1)))
            stdout.write("{}".format(" " * ceil(columns * (total_time-i)/total_time)) + "|" if (columns-i) !=0 else "|")
        stdout.flush()
        sleep(1)
        columns = list(get_terminal_size())[0]-15
    stdout.write(AnsiEscapeCodes.NEW_LINE)
    return None

def time_program_execution(userSeconds: int) -> str:
    SECONDS_IN_A_MINUTE = 60
    SECONDS_IN_A_HOUR = 3600
    SECONDS_IN_A_DAY = 86400

    numberOfSeconds = userSeconds % SECONDS_IN_A_MINUTE

    remainingMinutes = userSeconds % SECONDS_IN_A_HOUR
    numberOfMinutes = remainingMinutes // SECONDS_IN_A_MINUTE

    remainingHours = userSeconds % SECONDS_IN_A_DAY
    numberOfHours = remainingHours // SECONDS_IN_A_HOUR

    numberOfDays = userSeconds // SECONDS_IN_A_DAY

    program_execution = "%d days, %02d hours, %02d minutes and %02d seconds" %(numberOfDays, numberOfHours, numberOfMinutes, numberOfSeconds)
    return program_execution