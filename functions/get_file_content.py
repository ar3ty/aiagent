import os

def get_file_content(working_directory, file_path):
    try:
        abs_path = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not target_path.startswith(abs_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_path, "r", encoding="utf-8") as f:
            buffer = f.read(10000)

        if len(buffer) == 10000:
            buffer += f'[...File "{file_path}" truncated at 10000 characters]'

        return buffer
    except Exception as e:
        return f"Error: {e}"