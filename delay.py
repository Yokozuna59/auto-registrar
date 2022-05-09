# import sleep from time to delay the program
from time import sleep

# improt stdout to use stdout.write and stdout.flush
from sys import stdout

# import get_terminal_size from os to get terminal size
from os import get_terminal_size

# import ceil and floor to get ceiling adn floor of float numbers
from math import ceil, floor

def time_delay(refresh_time: int) -> None:
    """
    Takes int number and wait until that amount of time while printing a progress par.\n
    return `None` after that.
    """

    stdout.write("\x1b[s")
    stdout.write("\x1b[?25l")
    for i in range(1, refresh_time+1):
        stdout.write("\x1b[u")
        terminal_columns = get_terminal_size()[0]-15
        if (i==1):
            stdout.write("\x1b[0mNext Refresh: |{}|".format(" " * (terminal_columns-1)))
            stdout.write("\x1b[u")
            stdout.flush()
        sleep(1)
        stdout.write("\x1b[2K")
        stdout.write("\x1b[39mNext Refresh: |{}".format("█" * (floor(terminal_columns * (i/refresh_time))-1)))
        stdout.write("{}".format(" " * ceil(terminal_columns * (refresh_time - i)/refresh_time)) + "|" if (terminal_columns-i)!=0 else "|")
        stdout.flush()
    print()
    return