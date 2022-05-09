# import stdout to write colorful text
from sys import stdout

# import readchar to get one character
from readchar import readchar

# import get_terminal_size to get terminal size
from os import get_terminal_size

# import floor to get the floor of float number
from math import floor

class Questions:
    def bool_question(question: str = "", default: bool = True) -> bool:
        """
        Ask user a boolean question.\n
        If he answered correctly, return the answer as `bool` type.
        """

        while True:
            stdout.write("\x1b[92m?\x1b[0m \x1b[1m{}\x1b[0m? {} ".format(question, "[Y/n]" if default == True else "[y/N]"))
            stdout.write("\x1b[s")
            answer = input().lower()

            if (len(answer) == 0):
                answer = default
            else:
                if (answer == "y" or answer == "yes"):
                    answer = True
                elif (answer == "n" or answer == "no"):
                    answer = False
                else:
                    stdout.write(f'\x1b[91m! Sorry, your reply was invalid: "\x1b[0m\x1b[1m{answer}\x1b[0m\x1b[91m" is not a valid answer, please try again.\x1b[0m\n')
                    continue

            stdout.write("\x1b[u")
            stdout.write("\x1b[6D")
            stdout.write("\x1b[0K")
            stdout.write("\x1b[94m{}\x1b[0m\n".format("Yes" if answer == True else "No"))
            stdout.flush()
            return answer

    def str_questoin(question: str) -> str:
        """
        Ask user a string question.\n
        return the answer as `str` type.
        """

        stdout.write(f"\x1b[92m?\x1b[0m \x1b[1m{question}\x1b[0m? ")
        stdout.write("\x1b[s")

        while True:
            answer = input()
            if (answer == "\r"):
                continue
            else:
                stdout.write("\x1b[u")
                stdout.write("\x1b[0K")
                stdout.write(f"\x1b[94m{answer}\x1b[0m\n")
                stdout.flush()
                return answer

    def passcode_question(question: str) -> str:
        """
        Ask user a string question without printing what he wrote.\n
        return the answer as `str` type.
        """

        answer = ""
        letter = ""
        stdout.write('\x1b[?25l')
        stdout.write(f"\x1b[92m?\x1b[0m \x1b[1m{question}\x1b[0m? ")
        stdout.write("\x1b[s")

        while True:
            stdout.flush()
            letter = readchar()

            if (letter == '\r'):
                if (answer == 0):
                    continue
                stdout.write("\x1b[0K")
                stdout.write("\x1b[u")
                stdout.write("\x1b[94m{}\x1b[0m\n".format("*" * len(answer)))
                stdout.write("\x1b[?25h")
                stdout.flush()
                return answer
            elif (letter == "\x03"):
                stdout.write("\x1b[0K^C")
                stdout.write("\x1b[u")
                stdout.write("\x1b[1E")
                stdout.write("\x1b[?25h")
                stdout.flush()
                exit()
            else:
                if (letter == "\x7f"):
                    if (len(answer) == 0):
                        pass
                    else:
                        stdout.write("\x1b[1D")
                        stdout.write("\x1b[0K")
                        answer = answer[:-1]
                else:
                    answer += letter
                    stdout.write("*")

    def list_question(question: str, choices: list) -> str:
        """
        Ask user to select an answer.\n
        return the answer as `str` type.
        """

        word = ""
        letter = ""
        ALL_CHOICES = choices
        stdout.write('\x1b[?25l')
        stdout.write(f"\x1b[92m?\x1b[0m \x1b[1m{question}\x1b[0m? ")
        stdout.write("\x1b[s")

        while True:
            terminal_columns = get_terminal_size()[0]
            question_lines = (len(question)+41)-(terminal_columns)*floor((len(question)+41)/terminal_columns)+1
            line_gap = 0 if (question_lines == 1) else 0 if (question_lines > 36 and question_lines <= terminal_columns) else 1
            stdout.write("\x1b[38;5;39m [Use arrows to move, type to filter]\x1b[0m")

            if (letter != "\x1b[A" and letter != "\x1b[B"):
                stdout.write("\n" * (len(choices)))
                stdout.write("\x1b[u")
                stdout.write("\x1b[1E") if line_gap == 1 else None

                list_lenght = 0
                choices = []

                for index, choice in enumerate(ALL_CHOICES):
                    if (word in choice.lower()):
                        list_lenght += 1
                        choices.append(choice)
                        stdout.write("\x1b[1E")
                        stdout.write("\x1b[2K")
                        if (list_lenght == 1):
                            stdout.write(f"\x1b[94m> {choice}\x1b[0m")
                            answer = choice
                        else:
                            stdout.write(f"\x1b[1m  {choice}\x1b[0m")
                index = 1

            stdout.write("\x1b[u")
            stdout.flush()

            letter = readchar()
            if (letter == '\x1b'):
                letter += readchar() + readchar()

                if (letter == '\x1b[A' and list_lenght != 0):
                    stdout.write('\x1b[{}E'.format(index + line_gap))
                    stdout.write("\x1b[2K")
                    index -= 1
                    stdout.write(f"\x1b[1m  {choices[index]}\x1b[0m")
                    stdout.write("\x1b[u")
                    if (index == 0):
                        index=list_lenght
                        stdout.write('\x1b[{}E'.format(index + line_gap))
                        index-=1
                    else:
                        index -= 1
                        stdout.write('\x1b[{}E'.format(index+1 + line_gap))
                    stdout.write("\x1b[2K")
                    stdout.write(f"\x1b[94m> {choices[index]}\x1b[0m")
                    answer = choices[index]
                    index+=1
                elif (letter == '\x1b[B' and list_lenght != 0):
                    stdout.write('\x1b[{}E'.format(index + line_gap))
                    stdout.write("\x1b[2K")
                    stdout.write(f"\x1b[1m  {choices[index - 1]}\x1b[0m")
                    stdout.write("\x1b[u")
                    if (index == list_lenght):
                        index = 1
                    else:
                        index+=1
                    stdout.write('\x1b[{}E'.format(index + line_gap))
                    stdout.write("\x1b[2K")
                    stdout.write(f"\x1b[94m> {choices[index - 1]}\x1b[0m")
                    answer = choices[index-1]
            elif (letter == '\r'):
                if (list_lenght == 0):
                    continue
                stdout.write("\x1b[s")
                stdout.write("\x1b[0K\x1b[1E\x1b[0K")
                stdout.write("\x1b[u")
                stdout.write(f"\x1b[94m{answer}\x1b[0m")
                stdout.write("\x1b[s")

                for i in range(list_lenght+line_gap):
                    stdout.write("\x1b[1E")
                    stdout.write("\x1b[2K")
                stdout.write("\x1b[u")
                stdout.write("\x1b[?25h")
                stdout.write("\x1b[1E")
                stdout.flush()
                return answer
            elif (letter == "\x03"):
                stdout.write("\x1b[0K^C")
                for i in range(list_lenght+1):
                    stdout.write("\x1b[1E")
                    stdout.write("\x1b[2K")
                stdout.write("\x1b[u")
                stdout.write("\x1b[1E")
                stdout.write("\x1b[?25h")
                stdout.flush()
                exit()
            else:
                if (letter == "\x7f"):
                    if (len(word) == 0):
                        pass
                    else:
                        stdout.write("\x1b[1D")
                        word = word[:-1]
                else:
                    word += letter

                for i in range(list_lenght+1):
                    stdout.write("\x1b[1E")
                    stdout.write("\x1b[2K")
            stdout.write("\x1b[u")
            stdout.write("\x1b[0K")
            stdout.write(word)

    def dict_question(question: str, choices: dict) -> str:
        """
        Ask user to select an answer.\n
        return the answer's value as `str` type.
        """

        answer = Questions.list_question(question=question, choices=list(choices.keys()))
        return choices[answer]

class cli_colors:
    END             = '\x1B[0m'
    BOLD            = '\x1B[1m'
    BLINK           = '\x1B[5m'

    BRIGHT_RED      = '\x1B[91m'
    BRIGHT_GREEN    = '\x1B[92m'
    BRIGHT_YELLOW   = '\x1B[93m'
    BRIGHT_BLUE     = '\x1B[94m'
    BRIGHT_MAGENTA  = '\x1B[95m'
    BRIGHT_CYAN     = '\x1B[96m'

    def colorful_print(text_string: str, text_color: str) -> None:
        """
        Print colorful text.\n
        after prtinting, return `None`
        """

        print(f"{text_color}{text_string}{cli_colors.END}")
        return