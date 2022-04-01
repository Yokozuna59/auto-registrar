from colorful_terminal import color_input, tcolor
from errors import *

def get_user_input(lists):
    user_input = color_input("[*] - Enter number: ", tcolor.OKGREEN)

    if (not len(lists) > 0 and not len(lists) >= int(user_input)):
        number_out_of_range()

    return user_input