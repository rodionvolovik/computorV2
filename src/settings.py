VARS = "vars"
FUNC = "func"
MATR = "matr"
COMP = "comp"

CLEAR = "clear"
HELP = "help"
EXIT = "exit"
QUIT = "quit"

RE_ALL_LOWER_CASE = "^[a-z]+$"
RE_FUNCTION = "[a-z]+\([a-z]+\)"
RE_FUNCTION_CALCULATE = "[a-z]+\([0-9]+\)"
RE_FUNCTION_BODY = "[a-wy-z]"
RE_EXPRESSION = "^[0-9+-\/%\(\)]+$"
RE_EXPRESSION_WITH_VAR = "^[\(\)\*a-hj-z0-9+-\/%]+$"
RE_EXPRESSION_COMPLEX = "*i"

NOT_FOUND = -1