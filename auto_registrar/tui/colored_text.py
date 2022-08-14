from sys import stdout

from auto_registrar.tui.ansi import AnsiKeys, AnsiStyle


def print_one_color_text(text_string: str, text_color: str, end_with=AnsiKeys.NEW_LINE):
    stdout.write(f"{text_color}{text_string}{AnsiStyle.RESET_ALL}{end_with}")
    stdout.flush()


def print_more_color_text(*args, end_with=AnsiKeys.NEW_LINE):
    index = 0
    while len(args) > index:
        text_string = args[index]
        text_color = args[index + 1]
        stdout.write(f"{text_color}{text_string}{AnsiStyle.RESET_ALL} ")
        index += 2
    stdout.write(end_with)
    stdout.flush()
