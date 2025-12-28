from config import MAX_CHARS
import os

def get_file_content(working_directory, file_path):

    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

    # ensure the target file_path is inside the working file_path
    valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

    if not valid_target_file:
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    with open(target_file, "r") as f:
        file_content_string = f.read(int(MAX_CHARS))
        # After reading the first MAX_CHARS...
        if f.read(1):
            file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return f"{file_content_string}"

if __name__ == "__main__":
    response = get_file_content("calculator", "tests.py")
    print(response)