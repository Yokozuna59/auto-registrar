from sys import stdout
from readchar import readchar
from os import get_terminal_size
from math import floor

class Questions:
    def bool_question(question:str, default:bool = True):
        while True:
            stdout.write("\x1b[92m?\x1b[0m \x1b[1m{}\x1b[0m? {} ".format(question, "[Y/n]" if default == True else "[y/N]"))
            stdout.write("\x1b[s")
            answer = input().lower()

            if (len(answer) == 0):
                return default
            else:
                if (answer == "y" or answer == "yes"):
                    answer = True
                elif (answer == "n" or answer == "no"):
                    answer = False
                else:
                    stdout.write('\x1b[91m! Sorry, your reply was invalid: "\x1b[0m\x1b[1m{}\x1b[0m\x1b[91m" is not a valid answer, please try again.\x1b[0m\n'.format(answer))
                    continue

            stdout.write("\x1b[u")
            stdout.write("\x1b[6D")
            stdout.write("\x1b[0K")
            stdout.write("\x1b[94m{}\x1b[0m\n".format("Yes" if answer == True else "No"))
            return answer

    def str_questoin(question:str):
        stdout.write("\x1b[92m?\x1b[0m \x1b[1m{}\x1b[0m? ".format(question))
        stdout.write("\x1b[s")
        while True:
            answer = input()
            if (answer == "\r"):
                continue
            else:
                stdout.write("\x1b[u")
                stdout.write("\x1b[0K")
                stdout.write("\x1b[94m{}\x1b[0m\n".format(answer))
                return answer

    def passcode_question(question:str):
        answer, letter = "", ""
        stdout.write('\x1b[?25l')
        stdout.write("\x1b[92m?\x1b[0m \x1b[1m{}\x1b[0m? ".format(question))
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
                return answer
            elif (letter == "\x03"):
                stdout.write("\x1b[0K^C")
                stdout.write("\x1b[u")
                stdout.write("\x1b[1E")
                stdout.write("\x1b[?25h")
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

    def list_question(question:str, choices:list):
        CHOICES = choices
        word, letter = "", ""
        stdout.write('\x1b[?25l')
        stdout.write("\x1b[92m?\x1b[0m \x1b[1m{}\x1b[0m? ".format(question))
        stdout.write("\x1b[s")

        while True:
            terminal_columns = get_terminal_size()[0]
            question_lines = (len(question)+41)-(terminal_columns)*floor((len(question)+41)/terminal_columns)+1
            line_gap = 0 if (question_lines == 1) else 0 if (question_lines > 36 and question_lines <= terminal_columns) else 1
            stdout.write("\x1b[38;5;39m [Use arrows to move, type to filter]\x1b[0m")

            if (letter != "\x1b[A" and letter != "\x1b[B"):
                list_lenght = 0
                choices_ = []

                stdout.write("\n" * (len(choices)))
                stdout.write("\x1b[u")
                stdout.write("\x1b[1E") if line_gap == 1 else None

                for index, choice in enumerate(CHOICES):
                    if (word in choice.lower()):
                        list_lenght += 1
                        choices_.append(choice)
                        stdout.write("\x1b[1E")
                        stdout.write("\x1b[2K")
                        if (list_lenght == 1):
                            stdout.write("\x1b[94m> {}\x1b[0m".format(choice))
                            answer = choice
                        else:
                            stdout.write("\x1b[1m  {}\x1b[0m".format(choice))
                index = 1
                choices = choices_

            stdout.write("\x1b[u")
            stdout.flush()

            letter = readchar()
            if (letter == '\x1b'):
                letter += readchar() + readchar()

                if (letter == '\x1b[A' and list_lenght != 0):
                    stdout.write('\x1b[{}E'.format(index + line_gap))
                    stdout.write("\x1b[2K")
                    index -= 1
                    stdout.write("\x1b[1m  {}\x1b[0m".format(choices[index]))
                    stdout.write("\x1b[u")
                    if (index == 0):
                        index=list_lenght
                        stdout.write('\x1b[{}E'.format(index + line_gap))
                        index-=1
                    else:
                        index -= 1
                        stdout.write('\x1b[{}E'.format(index+1 + line_gap))
                    stdout.write("\x1b[2K")
                    stdout.write("\x1b[94m> {}\x1b[0m".format(choices[index]))
                    answer = choices[index]
                    index+=1
                elif (letter == '\x1b[B' and list_lenght != 0):
                    stdout.write('\x1b[{}E'.format(index + line_gap))
                    stdout.write("\x1b[2K")
                    stdout.write("\x1b[1m  {}\x1b[0m".format(choices[index - 1]))
                    stdout.write("\x1b[u")
                    if (index == list_lenght):
                        index = 1
                    else:
                        index+=1
                    stdout.write('\x1b[{}E'.format(index + line_gap))
                    stdout.write("\x1b[2K")
                    stdout.write("\x1b[94m> {}\x1b[0m".format(choices[index - 1]))
                    answer = choices[index-1]
            elif (letter == '\r'):
                if (list_lenght == 0):
                    continue
                stdout.write("\x1b[s")
                stdout.write("\x1b[0K\x1b[1E\x1b[0K")
                stdout.write("\x1b[u")
                stdout.write("\x1b[94m{}\x1b[0m\n".format(answer))
                stdout.write("\x1b[s")

                for i in range(list_lenght+line_gap):
                    stdout.write("\x1b[2K")
                    stdout.write("\x1b[1E")
                stdout.write("\x1b[u")
                stdout.write("\x1b[?25h")
                return answer
            elif (letter == "\x03"):
                stdout.write("\x1b[0K^C")
                for i in range(list_lenght+1):
                    stdout.write("\x1b[1E")
                    stdout.write("\x1b[2K")
                stdout.write("\x1b[u")
                stdout.write("\x1b[1E")
                stdout.write("\x1b[?25h")
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

    def dict_question(question:str, choices:dict):
        answer = Questions.list_question(question=question, choices=list(choices.keys()))
        return choices[answer]

class Color_cli:
    END             = '\x1B[0m'
    BOLD            = '\x1B[1m'
    BLINK           = '\x1B[5m'

    BRIGHT_RED      = '\x1B[91m'
    BRIGHT_GREEN    = '\x1B[92m'
    BRIGHT_YELLOW   = '\x1B[93m'
    BRIGHT_BLUE     = '\x1B[94m'
    BRIGHT_MAGENTA  = '\x1B[95m'
    BRIGHT_CYAN     = '\x1B[96m'

    COP             = '\x1b[48;2;92;148;13m'
    DIS             = '\x1b[48;2;201;42;42m'
    FLD             = '\x1b[48;2;33;37;41m'
    IND             = '\x1b[48;2;33;37;41m'
    LAB             = '\x1b[48;2;95;61;196m'
    LEC             = '\x1b[48;2;24;100;171m'
    LLB             = '\x1b[48;2;33;37;41m'
    MR              = '\x1b[48;2;33;37;41m'
    PRJ             = '\x1b[48;2;217;72;15m'
    RES             = '\x1b[48;2;201;42;42m'
    SEM             = '\x1b[48;2;8;127;91m'
    SLB             = '\x1b[48;2;33;37;41m'
    ST              = '\x1b[48;2;33;37;41m'
    STD             = '\x1b[48;2;33;37;41m'
    THS             = '\x1b[48;2;54;79;199m'

    def colorful_print(text:str, text_color:str):
        print("{}{}\x1b[0m".format(text_color, text))