from sys import stdout

from auto_registrar.tui.ansi import AnsiCursor, AnsiKeys, AnsiStyle


def print_one_color_text(
    text_string: str, text_color: str, end_with: str = AnsiKeys.NEW_LINE
) -> None:
    """
    Prints colorful text with one color.\n
    Returns `None`.
    """

    stdout.write(f"{text_color}{text_string}{AnsiStyle.RESET_ALL}{end_with}")
    stdout.flush()


def print_more_color_text(
    *args: str, end_with: str = AnsiKeys.NEW_LINE
) -> None:
    """
    Prints colorful text with more than one color.\n
    Returns `None`.
    """

    index = 0
    while len(args) > index:
        text_string = args[index]
        text_color = args[index + 1]
        stdout.write(f"{text_color}{text_string}{AnsiStyle.RESET_ALL} ")
        index += 2
    AnsiCursor.move_left()
    stdout.write(end_with)
    stdout.flush()
