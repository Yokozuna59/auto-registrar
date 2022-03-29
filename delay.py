import time, sys

def delay(time_delay):
    for i in range(1, time_delay+1):
        sys.stdout.write("\rNext Refresh: [" + "#" * i + " " * (time_delay - i) + "] | " + str(round(i/time_delay * 100, 2)) + "%")
        time.sleep(1)
    sys.stdout.write("\r")
    sys.stdout.flush()