class tcolor:
    END = "\033[0m"
    BLINK = "\033[5m"
    LIGHT_RED = "\033[91m"
    LIGHT_GREEN = "\033[92m"
    LIGHT_YELLOW = "\033[93m"
    LIGHT_BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"

def color_print(text, color):
    print(color + text + tcolor.END)

def color_input(text, color):
    print(color + text + tcolor.END, end = "")
    user_input = input()
    return user_input
