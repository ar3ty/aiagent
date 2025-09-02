from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file
from config import WORKING_DIR
import json

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

Working directory may be nested. If you are looking for anything, you can check nested directories also.
If you are called to fix some bug, you are free to fix code in places where it is needed. Rewrite the problematic file.
Scheduled function will be executed and you will receive result of execution in message. Comment you tool_calls in message.content. Leave tool_calls empty only in final answer. When writing a final answer, return your answer in regular message.content, don't schedule any tool_calls. 
All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_tools = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file
]

names_to_functions = {
    "run_python_file": run_python_file,
    "write_file": write_file,
    "get_files_info": get_files_info, 
    "get_file_content": get_file_content
}

def call_function(tool_call, verbose=False):
    if verbose:
        print(f"Calling function: {tool_call.function.name}({tool_call.function.arguments})")
    else:
        print(f" - Calling function: {tool_call.function.name}")
    
    args = json.loads(tool_call.function.arguments)
    args["working_directory"] = WORKING_DIR

    if tool_call.function.name not in names_to_functions:
        return json.dumps({"error":f"Unknown function: {tool_call.function.name}."})
    
    func_to_call = names_to_functions[tool_call.function.name]

    output = func_to_call(**args)

    return json.dumps({"result": f"{output}"})