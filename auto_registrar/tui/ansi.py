from sys import stdout


class AnsiKeys:
    """A class contains some keyboard keys."""

    ENTER = "\r"
    NEW_LINE = "\n"
    TAB = "\t"

    BACKSPACE = "\x7f"
    DELETE = "\x1B[3~"

    ESCAPE = "\x1B"
    CNTL_A = "\x01"
    CNTL_C = "\x03"
    CNTL_V = "\x16"

    ARROW_UP = "\x1B[A"
    ARROW_DOWN = "\x1B[B"
    ARROW_RIGHT = "\x1B[C"
    ARROW_LEFT = "\x1B[D"

    HOME = "\x1B[H"
    END = "\x1B[F"


class AnsiStyle:
    """A class contains some ansi styles."""

    RESET_ALL = "\x1B[0m"

    BOLD = "\x1B[1m"
    FAINT = "\x1B[2m"
    ITALIC = "\x1B[3m"
    UNDERLINE = "\x1B[4m"
    BLINK = "\x1B[5m"
    INVERSE = "\x1B[7m"
    HIDDEN = "\x1B[8m"
    STRIKETHROUGH = "\x1B[9m"

    BOLD_RESET = "\x1B[22m"
    FAINT_RESET = "\x1B[22m"
    ITALIC_RESET = "\x1B[23m"
    UNDERLINE_RESET = "\x1B[24m"
    BLINK_RESET = "\x1B[25m"
    INVERSE_RESET = "\x1B[27m"
    HIDDEN_RESET = "\x1B[28m"
    STRIKETHROUGH_RESET = "\x1B[29m"


class AnsiColor:
    """A class contains asni colors."""

    GRAY = "\x1B[30m"
    RED = "\x1B[31m"
    GREEN = "\x1B[32m"
    YELLOW = "\x1B[33m"
    BLUE = "\x1B[34m"
    MAGENTA = "\x1B[35m"
    CYAN = "\x1B[36m"
    WHITE = "\x1B[37m"

    DEFAULT = "\x1B[39m"

    LIGHT_GRAY = "\x1B[90m"
    LIGHT_RED = "\x1B[91m"
    LIGHT_GREEN = "\x1B[92m"
    LIGHT_YELLOW = "\x1B[93m"
    LIGHT_BLUE = "\x1B[94m"
    LIGHT_MAGENTA = "\x1B[95m"
    LIGHT_CYAN = "\x1B[96m"
    LIGHT_WHITE = "\x1B[97m"

    BOLD_LIGHT_GRAY = "\x1B[1m\x1b[38;2;175;175;175m"


class AnsiCursor:
    def hide():
        stdout.write("\x1B[?25l")
        stdout.flush()

    def show():
        stdout.write("\x1B[?25h")
        stdout.flush()

    def save_position():
        stdout.write("\x1B7\x1B[s")
        stdout.flush()

    def restore_position():
        stdout.write("\x1B8\x1B[u")
        stdout.flush()

    def move_up(n: int = 1):
        if n != 0:
            stdout.write("\x1B[%dA" % n)
            stdout.flush()

    def move_down(n: int = 1):
        if n != 0:
            stdout.write("\x1B[%dB" % n)
            stdout.flush()

    def move_right(n: int = 1):
        if n != 0:
            stdout.write("\x1B[%dC" % n)
            stdout.flush()

    def move_left(n: int = 1):
        if n != 0:
            stdout.write("\x1B[%dD" % n)
            stdout.flush()

    def move_next_line(n: int = 1):
        if n != 0:
            stdout.write("\x1B[%dE" % n)
            stdout.flush()


class AnsiErase:
    def backspace(user_input: str, index: int, passcode=False) -> str:
        AnsiCursor.move_left()
        AnsiErase.erase_line_to_end()

        index -= 1
        if passcode:
            stdout.write("*" * (len(user_input[index:-1])))
        else:
            stdout.write(user_input[index:-1])
        AnsiCursor.restore_position()
        if index != 0:
            AnsiCursor.move_right(index)

        edited_user_input = user_input[:index] + user_input[index + 1 :]
        return edited_user_input

    def delete(user_input: str, index: int, passcode=False) -> str:
        AnsiErase.erase_line_to_end()

        index += 1
        if passcode:
            stdout.write("*" * (len(user_input[index:])))
        else:
            stdout.write(user_input[index:])
        AnsiCursor.restore_position()
        AnsiCursor.move_right(index - 1)

        edited_user_input = user_input[: index - 1] + user_input[index:]
        return edited_user_input

    def erase_line_to_end():
        stdout.write("\x1B[0K")
        stdout.flush()

    def erase_entire_line():
        stdout.write("\x1B[2K")
        stdout.flush()
