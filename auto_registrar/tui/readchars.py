from concurrent.futures import ThreadPoolExecutor, TimeoutError

try:
    from sys import stdin
    from termios import TCSADRAIN, tcgetattr, tcsetattr
    from tty import setraw

    unix = True
except ImportError:
    from msvcrt import getch

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
                except TimeoutError:
                    pass
                finally:
                    stdin.flush()
        finally:
            tcsetattr(fd, TCSADRAIN, old_settings)
    else:
        char = getch().decode("utf-8")
        if char == "\x00":
            executor = ThreadPoolExecutor()
            future = executor.submit(read_more_chars)
            try:
                return_value = future.result(timeout=0.01)
                future.cancel()
                char += return_value
            finally:
                stdin.flush()
    stdin.flush()
    return char


def read_more_chars() -> str:
    if unix:
        chars = stdin.read(2)
        if chars[-1].isdigit():
            chars += stdin.read(1)
    else:
        chars = getch().decode("utf-8")
    return chars


# def echo_mode_off() -> tuple:
#     fd = stdin.fileno()
#     if unix:
#         old_settings = tcgetattr(fd)
#         setraw(fd=fd)
#     else:
#         pass

#     return fd, old_settings


# def echo_mode_on(fd: int, old_settings: list) -> None:
#     if unix:
#         tcsetattr(fd, TCSADRAIN, old_settings)
#     else:
#         pass


# def read_one_char() -> str:
#     if unix:
#         char = stdin.read(1)
#         if char == "\x1B":
#             executor = ThreadPoolExecutor()
#             future = executor.submit(read_more_chars)
#             try:
#                 return_value = future.result(timeout=0.01)
#                 future.cancel()
#                 char += return_value
#             except TimeoutError:
#                 future.cancel()
#                 stdout.flush()
#                 stdin.flush()

#     else:
#         if kbhit():
#             char = getch()
#     return char


# fd, old = echo_mode_off()
# tt = ""
# while True:
#     tt += read_one_char()
# echo_mode_on(fd, old)
