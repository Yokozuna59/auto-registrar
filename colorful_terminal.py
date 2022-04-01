class tcolor:
    HEADER  = '\033[95m'
    OKBLUE  = '\033[94m'
    OKCYAN  = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL    = '\033[91m'
    ENDC    = '\033[0m'
    BLINK   = '\033[5m'

    LEC     = '\033[48;2;24;100;171m'
    LAB     = '\033[48;2;95,61,196m'
    COP     = '\033[48;2;92,148,13m'
    PRJ     = '\033[48;2;217,72,15m'
    SEM     = '\033[48;2;8,127,91m'
    THS     = '\033[48;2;54,79,199m'
    STD     = '\033[48;2;33,37,41m'
    LLB     = '\033[48;2;33,37,41m'
    RES     = '\033[48;2;201,42,42m'
    SLB     = '\033[48;2;33,37,41m'
    MR      = '\033[48;2;33,37,41m'
    DIS     = '\033[48;2;201,42,42m'
    IND     = '\033[48;2;33,37,41m'
    ST      = '\033[48;2;33,37,41m'
    FLD     = '\033[48;2;33,37,41m'

def color_print(text, color, ends_with = '\n'):
    print(color + text + tcolor.ENDC, end = ends_with)

def color_input(text, color):
    print(color + text + tcolor.ENDC, end = "")
    user_input = input()
    return user_input

def color_choices(questions, color1 = tcolor.OKBLUE, color2 = tcolor.OKCYAN):
    if (type(questions) == dict):
        dict_keys = list(questions.keys())

        if (not list(questions.values())[0].isdigit()):
            index = 0
            for key, value in questions.items():
                if (index % 2 == 0):
                    color_print('[{:}] '.format(index+1), color1, ' ' if index < 9 else '')
                    color_print('{:<4}'.format(value), tcolor.WARNING, ' ')
                    color_print('{:}'.format(key), color1)
                else:
                    color_print('[{:}] '.format(index+1), color2, ' ' if index < 9 else '')
                    color_print('{:<4}'.format(value), tcolor.HEADER, ' ')
                    color_print('{:}'.format(key), color2)
                index+=1
            return
        else:
            questions = dict_keys

    for index, question in enumerate(questions):
        if index % 2 == 0:
            color_print(f"[{index + 1}] {question}", color1)
        else:
            color_print(f"[{index + 1}] {question}", color2)