from sys import stdout
from readchar import readchar
from os import get_terminal_size
from math import ceil, floor
from time import sleep

class AnsiEscapeCodes:
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
    MOVE_UP                     = "\x1B[1A"
    MOVE_DOWN                   = "\x1B[1B"
    MOVE_LEFT                   = "\x1B[1D"
    MOVE_RIGHT                  = "\x1B[1C"
    MOVE_TO_BEGIN_OF_NEXT_LINE  = "\x1B[1E"

    # Erase
    ERASE_TO_END_OF_LINE        = "\x1B[0K"
    ERASE_ENTIRE_LINE           = "\x1B[2K"

class Questions:
    def bool_question(question: str = "", default: bool = True) -> bool:
        """
        Ask user a boolean question.\n
        Return the answer as `bool` type if he answered correctly.
        """

        while True:
            default_answer = "[Y/n]" if default == True else "[y/N]"
            stdout.write(f"{AnsiEscapeCodes.GREEN}?{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}{question}?{AnsiEscapeCodes.RESET} {default_answer} ")
            stdout.write(AnsiEscapeCodes.SAVE_POSITION)
            answer = input().lower()

            if (len(answer) == 0):
                answer = default
            else:
                if (answer == "y" or answer == "yes"):
                    answer = True
                elif (answer == "n" or answer == "no"):
                    answer = False
                else:
                    stdout.write(f"{AnsiEscapeCodes.RED}! Sorry, your reply was invalid:{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}\"{answer}\"{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.RED}is not a valid answer, please try again.{AnsiEscapeCodes.RESET}\n")
                    continue

            stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
            stdout.write(AnsiEscapeCodes.MOVE_LEFT * 6)
            stdout.write(AnsiEscapeCodes.ERASE_TO_END_OF_LINE)
            stdout.write("{}{}{}\n".format(AnsiEscapeCodes.BLUE, "Yes" if answer == True else "No", AnsiEscapeCodes.RESET))
            stdout.flush()
            return answer

    def str_questoin(question: str) -> str:
        """
        Ask user a string question.\n
        return the answer as `str` type.
        """

        stdout.write(f"{AnsiEscapeCodes.GREEN}?{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}{question}?{AnsiEscapeCodes.RESET} ")
        stdout.write(AnsiEscapeCodes.SAVE_POSITION)

        while True:
            answer = input()
            if (answer == ""):
                stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                continue
            else:
                stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                stdout.write(AnsiEscapeCodes.ERASE_TO_END_OF_LINE)
                stdout.write(f"{AnsiEscapeCodes.BLUE}{answer}{AnsiEscapeCodes.RESET}\n")
                stdout.flush()
                return answer

    def passcode_question(question: str) -> str:
        """
        Ask user a string question without printing what he wrote.\n
        return the answer as `str` type.
        """

        answer = ""
        letter = ""
        stdout.write(f"{AnsiEscapeCodes.GREEN}?{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}{question}?{AnsiEscapeCodes.RESET} ")
        stdout.write(AnsiEscapeCodes.SAVE_POSITION)

        while True:
            stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
            stdout.flush()
            letter = readchar()

            if (letter == '\r'):
                if (answer == 0):
                    continue
                stdout.write(AnsiEscapeCodes.ERASE_TO_END_OF_LINE)
                stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                stdout.write("{}{}{}\n".format(AnsiEscapeCodes.BLUE, "*" * len(answer), AnsiEscapeCodes.RESET))
                stdout.flush()
                return answer
            elif (letter == "\x03"):
                stdout.write(AnsiEscapeCodes.MOVE_LEFT * (len(question) + 5))
                stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                stdout.write(f"{AnsiEscapeCodes.FAINT}?{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}\x1b[38;2;175;175;175m{question}?{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.RED}Cancelled by user{AnsiEscapeCodes.RESET}\n")
                stdout.flush()
                exit()
            else:
                if (letter == "\x7f"):
                    if (len(answer) == 0):
                        pass
                    else:
                        stdout.write(AnsiEscapeCodes.MOVE_LEFT)
                        answer = answer[:-1]
                else:
                    answer += letter
                stdout.write(AnsiEscapeCodes.ERASE_TO_END_OF_LINE)
                stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                stdout.write("*" * len(answer))

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

        while True:
            terminal_columns = get_terminal_size()[0]
            question_lines = (len(question)+41)-(terminal_columns)*floor((len(question)+41)/terminal_columns)+1
            line_gap = 0 if (question_lines == 1) else 0 if (question_lines > 36 and question_lines <= terminal_columns) else 1
            stdout.write(f"{AnsiEscapeCodes.BLUE} [Use arrows to move, type to filter]{AnsiEscapeCodes.RESET}")

            if (letter != "\x1b[A" and letter != "\x1b[B"):
                list_lenght = 0
                choices = []
                stdout.write("\n" * (len(choices)))
                stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE) if line_gap == 1 else None

                for index, choice in enumerate(ALL_CHOICES):
                    if (word in choice.lower()):
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

            if (letter == '\x1b'):
                letter += readchar() + readchar()
                if (letter == '\x1b[A' and list_lenght != 0):
                    stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE * (index + line_gap))
                    index -= 1
                    stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                    stdout.write(f"{AnsiEscapeCodes.BOLD}  {choices[index]}{AnsiEscapeCodes.RESET}")
                    stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                    if (index == 0):
                        index=list_lenght
                        stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE * (index + line_gap))
                        index-=1
                    else:
                        index -= 1
                        stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE * (index + 1 + line_gap))
                    stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                    stdout.write(f"{AnsiEscapeCodes.BLUE}> {choices[index]}{AnsiEscapeCodes.RESET}")
                    answer = choices[index]
                    index+=1
                elif (letter == '\x1b[B' and list_lenght != 0):
                    stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE * (index + line_gap))
                    stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                    stdout.write(f"{AnsiEscapeCodes.BOLD}  {choices[index - 1]}{AnsiEscapeCodes.RESET}")
                    stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                    if (index == list_lenght):
                        index = 1
                    else:
                        index+=1
                    stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE * (index + line_gap))
                    stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                    stdout.write(f"{AnsiEscapeCodes.BLUE}> {choices[index - 1]}{AnsiEscapeCodes.RESET}")
                    answer = choices[index-1]
            elif (letter == '\r'):
                if (list_lenght == 0):
                    continue
                stdout.write(AnsiEscapeCodes.SAVE_POSITION)
                # TODO
                stdout.write("\x1b[0K\x1b[1E\x1b[0K")
                stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                stdout.write(f"{AnsiEscapeCodes.BLUE}{answer}{AnsiEscapeCodes.RESET}")
                stdout.write(AnsiEscapeCodes.SAVE_POSITION)

                for _ in range(list_lenght+line_gap):
                    stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE)
                    stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                stdout.write(AnsiEscapeCodes.HIDE_CURSOR)
                stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE)
                stdout.flush()
                return answer
            elif (letter == "\x03"):
                stdout.write("\x1b[{}D\x1b[2K".format(len(question) + 41))
                stdout.write(f"{AnsiEscapeCodes.FAINT}?{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}\x1b[38;2;175;175;175m{question}?{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.RED}Cancelled by user{AnsiEscapeCodes.RESET}\n")
                stdout.write(AnsiEscapeCodes.SAVE_POSITION)
                for _ in range(len(choices)):
                    stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE)
                    stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE)
                stdout.write(AnsiEscapeCodes.HIDE_CURSOR)
                stdout.flush()
                exit()
            else:
                if (letter == "\x7f"):
                    if (len(word) == 0):
                        pass
                    else:
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

    def dict_question(question: str, choices: dict) -> str:
        """
        Ask user to select an answer.\n
        return the answer's value as `str` type.
        """

        answer = Questions.list_question(question=question, choices=list(choices.keys()))
        return choices[answer]

    def mcq_list_question(question: str, choices: list) -> list:
        """
        Ask user to select an/multi answer/s.\n
        return the answer as `list` type.
        """

        letter = ""
        answer = []
        stdout.write(AnsiEscapeCodes.HIDE_CURSOR)
        stdout.write(f"{AnsiEscapeCodes.LIGHT_GREEN}?{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}{question}{AnsiEscapeCodes.RESET}? {AnsiEscapeCodes.BLUE} (<up> & <down> to move, <space> to select, <a> to toggle){AnsiEscapeCodes.RESET}")
        stdout.write(AnsiEscapeCodes.SAVE_POSITION)
        stdout.write("\n" * len(choices))
        stdout.write(AnsiEscapeCodes.RESTORE_POSITION)

        for index, choice in enumerate(choices):
            stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE)
            if (index == 0):
                stdout.write(f"{AnsiEscapeCodes.BLUE}>{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}○{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BLUE}{choice}{AnsiEscapeCodes.RESET}")
            else:
                stdout.write(f"  {AnsiEscapeCodes.BOLD}○ {choice}{AnsiEscapeCodes.RESET}")
        index = 1

        while True:
            stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
            stdout.flush()
            letter = readchar()
            if (letter == '\x1b'):
                letter += readchar() + readchar()

                if (letter == '\x1b[A'):
                    stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE * index)
                    stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                    index -= 1
                    stdout.write("  \x1b[1m{} {}\x1b[0m".format("●" if choices[index] in answer else "○", choices[index]))
                    stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                    if (index == 0):
                        index=len(choices)
                        stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE * index)
                        index-=1
                    else:
                        index -= 1
                        stdout.write('\x1b[{}E'.format(index+1))
                    stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                    stdout.write("\x1b[94m>\x1b[0m {} \x1b[94m{}\x1b[0m".format("●"  if choices[index] in answer else "○", choices[index]))
                    index+=1
                elif (letter == '\x1b[B'):
                    stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE * index)
                    stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                    stdout.write("\x1b[1m  {} {}\x1b[0m".format("●"  if choices[index - 1] in answer else "○", choices[index - 1]))
                    stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                    if (index == len(choices)):
                        index = 1
                    else:
                        index+=1
                    stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE * index)
                    stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                    stdout.write("\x1b[94m>\x1b[0m {} \x1b[94m{}\x1b[0m".format("●"  if choices[index - 1] in answer else "○", choices[index - 1]))
            elif (letter == '\r'):
                if (len(answer) == 0):
                    continue
                stdout.write("\x1b[58D\x1b[0K")
                stdout.write(AnsiEscapeCodes.SAVE_POSITION)
                stdout.write("\x1b[94m({} answers selected)\x1b[0m".format(str(len(answer))))
                for _ in range(len(choices) +1):
                    stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE)
                    stdout.write(AnsiEscapeCodes.ERASE_TO_END_OF_LINE)

                stdout.write(AnsiEscapeCodes.RESTORE_POSITION)
                stdout.write(AnsiEscapeCodes.HIDE_CURSOR)
                stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE)
                stdout.flush()
                return answer
            elif (letter == "\x03"):
                stdout.write("\x1b[{}D\x1b[2K".format(len(question) + 62))
                stdout.write(f"{AnsiEscapeCodes.FAINT}?{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.BOLD}\x1b[38;2;175;175;175m{question}?{AnsiEscapeCodes.RESET} {AnsiEscapeCodes.RED}Cancelled by user{AnsiEscapeCodes.RESET}\n")
                stdout.write(AnsiEscapeCodes.SAVE_POSITION)
                for _ in range(len(choices)):
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
                if (choices[index - 1] in answer):
                    stdout.write("\x1b[94m>\x1b[0m {} \x1b[94m{}\x1b[0m".format("○", choices[index - 1]))
                    answer.remove(choices[index - 1])
                else:
                    stdout.write("\x1b[94m>\x1b[0m {} \x1b[94m{}\x1b[0m".format("●", choices[index - 1]))
                    answer.append(choices[index - 1])
            elif (letter == "a"):
                current_index = index
                for index, choice in enumerate(choices):
                    stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE)
                    stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                    if (current_index== index+1):
                        stdout.write("\x1b[94m>\x1b[0m \x1b[1m{}\x1b[0m \x1b[94m{}\x1b[0m".format("○" if len(answer) == len(choices) else "●", choice))
                    else:
                        stdout.write("  \x1b[1m{} {}\x1b[0m".format("○" if len(answer) == len(choices) else "●", choice))
                answer = [] if len(answer) == len(choices) else choices.copy()
                index = current_index
                stdout.write(AnsiEscapeCodes.RESTORE_POSITION)

    def mcq_dict_question(question: str, choices: dict) -> list:
        """
        Ask user to select an/multi answer/s.\n
        return the answers' values as `list` type.
        """

        answers = Questions.mcq_list_question(question=question, choices=list(choices.keys()))
        answers_value = []
        for i in answers:
            answers_value.append(choices[i])
        return answers_value

def colorful_text(text_string: str, text_color: str, end_with = "\n") -> str:
    """
    Print colorful text.\n
    Return `None` after that.
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

    for i in range(1, total_time+1):
        columns = list(get_terminal_size())[0]-15
        try:
            if (current_columns != columns):
                lines = ceil(current_columns/columns) if (current_columns > columns) else ceil(columns/current_columns)
                for _ in range(lines):
                    stdout.write(AnsiEscapeCodes.ERASE_ENTIRE_LINE)
                    stdout.write(AnsiEscapeCodes.MOVE_TO_BEGIN_OF_NEXT_LINE)
                current_columns = columns
        except:
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
    stdout.write("\n")
    return None