import os
from functions.config import MAX_CHARS

def get_file_content(working_directory, file_path):
	full_path = os.path.join(working_directory, file_path)
	working_directory_abs = os.path.abspath(working_directory)
	full_path_abs = os.path.abspath(full_path)

	if not full_path_abs.startswith(working_directory_abs):
		return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
	if not os.path.isfile(full_path_abs):
		return f'Error: File not found or is not a regular file: "{file_path}"'
 
	with open(full_path_abs, 'r') as f:
		file_content_string = f.read(MAX_CHARS)
	
	if os.path.getsize(full_path_abs) > MAX_CHARS:
		file_content_string += f'[...File] "{file_path}" truncated at {MAX_CHARS} characters'
	return file_content_string