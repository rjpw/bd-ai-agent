import os

def write_file(working_directory, file_path, content):

    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    parent_dir = os.path.dirname(target_file)

    # ensure the target file_path is inside the working file_path
    valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

    if not valid_target_file:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if os.path.isdir(target_file):
        f'Error: Cannot write to "{file_path}" as it is a directory'

    try:
        os.makedirs(parent_dir, exist_ok=True)
    except Exception as e:
        f'Error: Could not create parent directory for "{file_path} -- {e.msg}"'

    with open(target_file, "w") as f:
        f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

if __name__ == "__main__":
    response = write_file("calculator", "testing/test.txt", "Just a test.")
    print(response)