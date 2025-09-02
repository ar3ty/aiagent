import os
import subprocess

schema_run_python_file = {
            "type": "function",
            "function": {
                "name": "run_python_file",
                "description": "Runs specified file with python, constrained to the working directory. Uses arguments, if provided. Returns output from the interpreter.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to the file to run, relative to the working directory.",
                        },
                        "arg": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "description": "One of the optional arguments for running file"
                                },
                            "description": "Arguments for running file. Defaults to empty list",
                        }
                    },
                    "required": ["file_path"]
                }
            }
        }

def run_python_file(working_directory, file_path, arg=[]):
    abs_path = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_path.startswith(abs_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
    if not os.path.exists(target_path):
        return f'Error: File "{file_path}" not found.'
        
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    args = ["python3", f"{file_path}"]
    if len(arg) > 0:
        args.extend(arg)
    try:
        completed_process = subprocess.run(cwd=abs_path, args=args, timeout=30, capture_output=True, text=True)
    except Exception as e:
        return f"Error: executing Python file: {e}"

    result = ""
    if completed_process.stdout:
        result += "STDOUT:\n" + completed_process.stdout
    if completed_process.stderr:
        result += "STDERR:\n" + completed_process.stderr
    
    if completed_process.returncode != 0:
        result += f"\nProcess exited with code {completed_process.returncode}"
    return result if result else "No output produced."