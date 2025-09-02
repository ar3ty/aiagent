import os

def write_file(working_directory, file_path, content):
    try:
        abs_path = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not target_path.startswith(abs_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(target_path):
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
        if os.path.exists(target_path) and os.path.isdir(target_path):
            return f"Error: {file_path} is a directory, not a file"

        with open(target_path, "w", encoding="utf-8") as f:
            n = f.write(content)

        return f'Successfully wrote to "{file_path}" ({n} characters written)'
    except Exception as e:
        return f"Error: {e}"