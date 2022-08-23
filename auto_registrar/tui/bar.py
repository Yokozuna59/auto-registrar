from math import ceil, floor
from os import get_terminal_size
from sys import exit, stdout
from time import sleep

from auto_registrar.tui.ansi import AnsiColor, AnsiCursor, AnsiErase, AnsiKeys
from auto_registrar.tui.colored_text import print_one_color_text


def progress_bar(total_time: int) -> None:
    """
    Print a progress bar.\n
    Return `None`.
    """

    REFRESH_RATE = 10

    try:
        AnsiCursor.hide()
        AnsiCursor.save_position()

        total_time *= REFRESH_RATE
        lines_moved = 0
        columns = list(get_terminal_size())[0] - 22
        current_columns = columns

        for index in range(1, total_time + 1):
            if current_columns != columns:
                if current_columns > columns:
                    lines_moved = ceil(current_columns / columns)
                elif current_columns > columns:
                    lines_moved = ceil(columns / current_columns)

                for _ in range(lines_moved):
                    AnsiErase.erase_entire_line()
                    AnsiCursor.move_next_line()
                current_columns = columns

            AnsiCursor.restore_position()
            AnsiErase.erase_entire_line()

            if index == 1:
                progress = 0
                full = "█" * progress
                empty = "░" * (columns - 1)
            elif index != total_time:
                progress = index / total_time
                full = "█" * floor(columns * progress)
                empty = "░" * (ceil((columns * (total_time - index) / total_time)) - 1)
            else:
                full = "█" * (columns - 1)
                empty = ""

            output = "Next Refresh: [%3d%%] |%s%s|" % (
                ceil(progress * 100),
                full,
                empty,
            )
            stdout.write(output)
            stdout.flush()
            sleep(1 / REFRESH_RATE)
            columns = list(get_terminal_size())[0] - 22
    except KeyboardInterrupt:
        AnsiCursor.restore_position()
        AnsiErase.erase_entire_line()
        print_one_color_text(text_string=output, text_color=AnsiColor.RED)
        AnsiCursor.show()
        exit()

    AnsiCursor.show()
    stdout.write(AnsiKeys.NEW_LINE)
    stdout.flush()
