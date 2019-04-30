#!./bin/python3
try:
    import sys
    import readline
    from src.processing import process_input, print_storage, print_manual
    from src.settings import *
except Exception as error:
    print(error)
    print("ERROR: Run ./install.sh to install all dependencies")
    exit()

if __name__ == "__main__":
    input_line = str()
    STORAGE = {
        VARS: {},
        FUNC: {},
        MATR: {},
        COMP: {}
    }
    while True:
        try:
            input_line = input("> ")
        except BaseException:
            print("\nSomething died :(")
            sys.exit()

        if input_line.lower() == EXIT or input_line.lower() == QUIT:
            print("See you next time :)")
            break
        
        if input_line.lower() == HELP:
            print_manual()
        
        if input_line.lower() == VARS:
            print("Printing storage..")
            print_storage(STORAGE)

        if input_line.lower() == CLEAR:
            STORAGE = {
                VARS: {},
                FUNC: {},
                MATR: {},
                COMP: {}
            }

        try:
            process_input(input_line.lower(), STORAGE)
        except Exception as error:
            print(error)