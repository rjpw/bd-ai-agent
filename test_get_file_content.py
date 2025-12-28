from functions.get_file_content import get_file_content
from config import *

def run_tests(working_directory, file_path):

    results = get_file_content(working_directory, file_path)
    print(f"{results}")

if __name__ == "__main__":
    # print(f"max chars: {MAX_CHARS}")
    run_tests("calculator", "main.py")
    run_tests("calculator", "pkg/calculator.py")
    run_tests("calculator", "/bin/cat")
    run_tests("calculator", "pkg/does_not_exist.py")
    #run_tests("calculator", "lorem.txt")

