from src.settings import *
import re


def reorder_storage(storage):
    list_tuples = sorted(storage.items(),  key=lambda x: len (x[0]), reverse=True)
    new_storage = {}
    for item in list_tuples:
        new_storage[item[0]] = item[1]
    return new_storage


def print_manual():
    print("Commands:")
    print("\tHELP/help              - invokates help menu")
    print("\tVARS/vars              - lists all stored data")
    print("\tQUIT/EXIT/exit/quit    - quits the program")


def print_storage_item(storage_item, name):
    if len(storage_item) > 0: print(name + ":")
    for var_key, var_val in storage_item.items():
        print("\t" + var_key + " = " + str(var_val))


def print_storage(storage):
    print_storage_item(storage[VARS], "Variables")
    print_storage_item(storage[MATR], "Matrices")
    print_storage_item(storage[FUNC], "Functions")
    print_storage_item(storage[COMP], "Complex numbers")


def func_calculation(func, number):
    error = str()
    solution = 0
    func_number = func.replace("x", number)
    try:
        solution = eval(func_number)
    except Exception:
        raise Exception("ERROR: Unknown variable")
    return str(solution)


def replace_args_in_function(func, storage):
    right_side = func
    flag = True
    while(flag):
        funcs = re.findall(RE_FUNCTION_CALCULATE, right_side)
        if len(funcs) == 0:
            flag = False
        for func in funcs:
            func_name = func[:func.find("(")]
            if func_name + "(x)" not in storage[FUNC]:
                raise Exception("ERROR: Unknown function " + func)
            else:
                func_occurences = re.findall(func_name + "\((\d+)\)", right_side)
                for occ in func_occurences:
                    solution = func_calculation(str(storage[FUNC][func_name + "(x)"]), str(occ))
                    right_side = right_side.replace(str(func), solution)
    return right_side


def convert_to_equation(input):
    input = input.replace("**", "^")
    input = input.replace("x", "X")
    input = input.replace("X+", "X^1+")
    input = input.replace("X-", "X^1-")
    input = input.replace("X=", "X^1=")
    input = input.replace("X", "X^1")
    input = input.replace("X^1^", "X^")
    input = input.replace("*", " * ")
    return input


def process_input(input_line, storage):
    error, need_to_evaluate = str(), False
    input_line = input_line.replace("^", "**")
    # Prevent error cases with more than 1 '=' sign
    if input_line.count("=") > 1:
        raise Exception("ERROR: Unrecognizable expression")
    elif input_line.count("=") == 1:
        left_side, right_side = input_line.split("=")
        left_side = left_side.strip().replace(' ', '')
        right_side = right_side.strip().replace(' ', '')

        # Check if answer requested
        if right_side == "?":
            if bool(re.findall(RE_FUNCTION, left_side)):
                for var in storage[VARS]:
                    if left_side.find("(" + var) != NOT_FOUND:
                        left_side = left_side.replace("(" + var, "(" + str(storage[VARS][var]))
                error, need_to_evaluate = "ERROR: Unknown function", False
            if bool(re.findall(RE_FUNCTION_CALCULATE, left_side)):
                error, need_to_evaluate = "ERROR: Unknown function", True
                left_side = replace_args_in_function(left_side, storage)
            if bool(re.match(RE_EXPRESSION_WITH_VAR, left_side)):
                for var in storage[VARS]:
                    left_side = left_side.replace(var, str(storage[VARS][var]))
            try:
                print(eval(left_side))
            except Exception:
                raise Exception("ERROR: Check format and available VARS with 'vars' command")
        elif right_side.find("?") != NOT_FOUND and right_side.count("?") == 1:
            right_side = right_side.replace("?", "")
            if bool(re.findall(RE_FUNCTION, right_side)):
                for var in storage[VARS]:
                    if right_side.find("(" + var) != NOT_FOUND:
                        right_side = right_side.replace("(" + var, "(" + str(storage[VARS][var]))
                error, need_to_evaluate = "ERROR: Unknown function", False
            if bool(re.findall(RE_FUNCTION_CALCULATE, right_side)):
                error, need_to_evaluate = "ERROR: Unknown function", True
                right_side = replace_args_in_function(right_side, storage)
            if bool(re.match(RE_EXPRESSION_WITH_VAR, right_side)):
                for var in storage[VARS]:
                    right_side = right_side.replace(var, str(storage[VARS][var]))
            if bool(re.findall(RE_FUNCTION, left_side)):
                for var in storage[VARS]:
                    if left_side.find("(" + var) != NOT_FOUND:
                        left_side = left_side.replace("(" + var, "(" + str(storage[VARS][var]))
                error, need_to_evaluate = "ERROR: Unknown function", False
            if bool(re.findall(RE_FUNCTION_CALCULATE, left_side)):
                error, need_to_evaluate = "ERROR: Unknown function", True
                left_side = replace_args_in_function(left_side, storage)
            if bool(re.match(RE_EXPRESSION_WITH_VAR, left_side)):
                for var in storage[VARS]:
                    left_side = left_side.replace(var, str(storage[VARS][var]))
            
            raise Exception(convert_to_equation(left_side) + " = " + convert_to_equation(right_side))

        # Prevent variable naming as 'i'
        elif left_side == "i":
            raise Exception("ERROR: You cannot name variable as 'i'. Not saved.")
        
        # Detect variable/matrix or function
        elif bool(re.match(RE_ALL_LOWER_CASE, left_side)):

            # Parse matrix
            if right_side.count('[') > 0 or right_side.count(']'):
                if right_side.count('[') == right_side.count(']'):
                    right_side = right_side.replace(";", ",")
                    try:
                        storage[MATR][left_side] = eval(right_side)
                    except Exception:
                        raise Exception("ERROR: Matrix format should be as [[1, 2]; [3, 4]]")
                
                    size_prev = len(storage[MATR][left_side][0])
                    size = 0
                    for i in range(1, len(storage[MATR][left_side])):
                        size = len(storage[MATR][left_side][i])
                        if size != size_prev:
                            raise Exception("ERROR: This is not a matrix")
                else:
                    raise Exception("ERROR: Invalid matrix syntax")
                print(storage[MATR][left_side])

            # Parse simple expression and save to variable
            elif bool(re.match(RE_EXPRESSION, right_side)):
                error, need_to_evaluate = "ERROR: Expression formatting error", True

            # Parse expression with another variable
            elif bool(re.match(RE_EXPRESSION_WITH_VAR, right_side)):
                for var in storage[VARS]:
                    right_side = right_side.replace(var, str(storage[VARS][var]))
                error, need_to_evaluate = "ERROR: Unknown variable", True

            # Parse expression with complex number
            elif right_side.find(RE_EXPRESSION_COMPLEX) != NOT_FOUND:
                storage[COMP][left_side] = right_side
                error, need_to_evaluate = "", False

            # Parse expression with function
            if bool(re.findall(RE_FUNCTION, right_side)):
                for var in storage[VARS]:
                    if right_side.find("(" + var) != NOT_FOUND:
                        right_side = right_side.replace("(" + var, "(" + str(storage[VARS][var]))
                error, need_to_evaluate = "ERROR: Unknown function", False
            if bool(re.findall(RE_FUNCTION_CALCULATE, right_side)):
                error, need_to_evaluate = "ERROR: Unknown function", True
                right_side = replace_args_in_function(right_side, storage)

            if need_to_evaluate:
                try:
                    evaluated = eval(right_side)
                    storage[VARS][left_side] = evaluated
                    print(storage[VARS][left_side])
                except Exception:
                    raise Exception("ERROR: Syntax error")

        # Parse function
        elif bool(re.match(RE_FUNCTION, left_side)):
            args = re.findall("x", left_side)
            if len(args) != 1:
                raise Exception("ERROR: Use x as argument")
            if right_side.find(left_side) != NOT_FOUND:
                raise Exception("ERROR: Seems to be death recursion xxx")
            # Parse expression with function
            for var in storage[VARS]:
                    right_side = right_side.replace(var, str(storage[VARS][var]))
            funcs = re.findall(RE_FUNCTION, right_side)
            for func in funcs:
                if func in storage[FUNC]:
                    right_side = right_side.replace(func, "(" + str(storage[FUNC][func]) + ")")
                else:
                    raise Exception("ERROR: Unknown function")
            if bool(re.findall(RE_FUNCTION, right_side)):
                for var in storage[VARS]:
                    if right_side.find("(" + var) != NOT_FOUND:
                        right_side = right_side.replace("(" + var, "(" + str(storage[VARS][var]))
            if bool(re.findall(RE_FUNCTION_CALCULATE, right_side)):
                print("REPLACE ARGS", right_side)
                right_side = replace_args_in_function(right_side, storage)
            
            if len(re.findall(RE_FUNCTION_BODY, right_side)) != 0:
                raise Exception("ERROR: Unknown argument, use 'x'")
            
            try:
                storage[FUNC][left_side] = eval(right_side)
            except:
                storage[FUNC][left_side] = right_side
            print(storage[FUNC][left_side])

        # Other case
        else:
            print("ERROR: Maybe you forgot to ask a result '?'")
    
    storage[VARS] = reorder_storage(storage[VARS])
    storage[FUNC] = reorder_storage(storage[FUNC])
    storage[MATR] = reorder_storage(storage[MATR])
    storage[COMP] = reorder_storage(storage[COMP])
 
        