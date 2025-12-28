import os, subprocess

def run_python_file(working_directory, file_path, args=None):

    working_dir_abs = os.path.abspath(working_directory)
    absolute_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

    # ensure the target file_path is inside the working file_path
    valid_target_file = os.path.commonpath([working_dir_abs, absolute_file_path]) == working_dir_abs

    if not valid_target_file:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(absolute_file_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", absolute_file_path]
    if args:
        command.extend(args)
    
    try:
        completed_process = subprocess.run(command, cwd=working_dir_abs, text=True,
            capture_output=True, timeout=30.0)
        if completed_process.returncode != 0:
            return f"Process exited with code {completed_process.returncode}"
        if completed_process.stdout == None and completed_process.stderr == None:
            return "No output produced"
        
        output = ["STDOUT:"]
        
        if completed_process.stdout:
            output.append(f"{completed_process.stdout}")
        
        output.append("STDERR:")

        if completed_process.stderr:
            output.append(f"{completed_process.stderr}")
    
        return "\n".join(output)
    
    except subprocess.TimeoutExpired as timeout_exc:
        return f"Error: {timeout_exc.stdout}"
    except Exception as e:
        return f"Error: {e.msg}"
    
if __name__ == "__main__":
    response = run_python_file("calculator", "main.py", ["3 + 5"])
    print(f"response: {response}")
    
