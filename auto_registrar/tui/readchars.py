from concurrent.futures import ThreadPoolExecutor

try:
    from sys import stdin
    from termios import tcgetattr, tcsetattr, TCSADRAIN
    from tty import setraw

    unix = True
except ImportError:
    from msvcrt import kbhit, getch

    unix = False


def read_one_char() -> str:
    if unix:
        fd = stdin.fileno()
        old_settings = tcgetattr(fd)
        try:
            setraw(fd=fd)
            char = stdin.read(1)
            if char == "\x1B":
                executor = ThreadPoolExecutor()
                future = executor.submit(read_more_chars)
                try:
                    return_value = future.result(timeout=0.01)
                    future.cancel()
                    char += return_value
                finally:
                    stdin.flush()
        finally:
            tcsetattr(fd, TCSADRAIN, old_settings)
    else:
        if kbhit():
            char = getch()
    stdin.flush()
    return char


def read_more_chars() -> str:
    chars = stdin.read(2)
    if chars[-1].isdigit():
        chars += stdin.read(1)
    return chars
