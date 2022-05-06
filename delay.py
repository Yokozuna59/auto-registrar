# import sleep from time to delay the program
from time import sleep

# improt stdout from sys to use stdout.write and stdout.flush
from sys import stdout

# import get_terminal_size from os to get terminal size
from os import get_terminal_size

# import ceil and floor to get ceiling adn floor of float numbers
from math import ceil, floor

def time_delay(refresh_time:int):
    stdout.write("\x1b[s")
    stdout.write("\x1b[?25l")
    for i in range(1, refresh_time+1):
        sleep(1)
        terminal_columns = get_terminal_size()[0]-15
        stdout.write("\x1b[2K")
        stdout.write("\x1b[39mNext Refresh: |{}".format("█" * (floor(terminal_columns * (i/refresh_time))-1)))
        stdout.write("{}".format(" " * ceil(terminal_columns * (refresh_time - i)/refresh_time)) + "|" if (terminal_columns-i)!=0 else "|")
        stdout.write("\x1b[u")
        stdout.flush()
    stdout.write("\033[0m\n")