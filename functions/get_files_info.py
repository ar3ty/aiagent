import os


def get_files_info(working_directory, directory="."):
    try:
        cwd = os.getcwd()
        abs_path = os.path.abspath(os.path.join(cwd, working_directory))
        path = os.path.join(abs_path, directory)
        if path not in os.listdir(abs_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(path):
            return f'Error: "{path}" is not a directory'

        result = ""
        items = os.listdir(path)
        for item in items:
            result += f" - {item.rsplit("/", 2)[1]}: file_size={os.path.getsize(item)}bytes, is_dir={os.path.isdir(item)}\n"

        return result
    except Exception as e:
        return f"Error: {e}"