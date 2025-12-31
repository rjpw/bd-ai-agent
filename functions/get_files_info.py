import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[schema_get_files_info],
)

def get_files_info(working_directory, directory="."):

    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

    # ensure the target directory is inside the working directory
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    output = []

    for subpath in os.listdir(target_dir):
        item = os.path.join(target_dir, subpath)
        file_size = os.path.getsize(item)
        item_isdir = os.path.isdir(item)
        output.append(f"- {subpath}: file_size={file_size} bytes, is_dir={item_isdir}")

    return "\n".join(output)

if __name__ == "__main__":
    response = get_files_info(".", "calculator/")
    print(response)