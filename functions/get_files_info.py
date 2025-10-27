import os
from google.genai import types

def get_files_info(working_directory, directory = '.'):
	full_path = os.path.join(working_directory, directory)
	working_directory_abs = os.path.abspath(working_directory)
	full_path_abs = os.path.abspath(full_path)
	if not full_path_abs.startswith(working_directory_abs):
		return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
	if not os.path.isdir(full_path_abs):
		return f'Error: "{directory}" is not a directory'

	contents = os.listdir(full_path_abs)
	info = []	
	for file in contents:
		info.append(f'	- {file}: file_size={os.path.getsize(os.path.join(full_path_abs,file))} bytes, is_dir={not os.path.isfile(file)}')
	return '\n'.join(info)	

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


