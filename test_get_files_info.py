from functions.get_files_info import get_files_info
from config import *

def run_tests(working_directory, directory):

    if directory == ".":
        print("Result for current directory:")
    else:
        print(f"Result for '{directory}' directory:")

    results = get_files_info(working_directory, directory)
    for line in results.split("\n"):
        print(f"  {line}")

if __name__ == "__main__":
    run_tests("calculator", ".")
    run_tests("calculator", "pkg")
    run_tests("calculator", "/bin")
    run_tests("calculator", "../")
