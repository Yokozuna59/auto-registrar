# import sleep from time to delay the program
from time import sleep

# improt stdout from sys to use stdout.write and stdout.flush
from sys import stdout

def time_delay(refresh_time):
    for i in range(1, refresh_time+1):
        stdout.write("\r\033[46mNext Refresh: [{}{}] | {}%".format("#" * i, "." * (refresh_time - i), str(round(i/refresh_time * 100, 2))))
        sleep(1)
    stdout.write("\033[0m\n")
    stdout.flush()