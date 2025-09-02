import os

schema_get_files_info = {
            "type": "function",
            "function": {
                "name": "get_files_info",
                "description": "Lists files in the specified directory along with their sizes, constrained to the working directory.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "directory": {
                            "type": "string",
                            "description": "Directory to list from, relative to the working directory. Use '.' for root.",
                        }
                    },
                    "required": ["directory"]
                }
            }
        }

def get_files_info(working_directory, directory="."):
    try:
        abs_path = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, directory))
        if directory != "." and not full_path.startswith(abs_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(full_path):
            return f'Error: "{full_path}" is not a directory'

        result = ""
        items = os.listdir(full_path)
        for item in items:
            current = os.path.join(full_path, item)
            result += f" - {item}: file_size={os.path.getsize(current)}bytes, is_dir={os.path.isdir(current)}\n"

        return result
    except Exception as e:
        return f"Error: {e}"