import os
import sys
from functions.config import MAX_CHARS

def get_file_info(working_directory, directory = '.'):
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

def get_file_content(working_directory, file_path):
	full_path = os.path.join(working_directory, file_path)
	working_directory_abs = os.path.abspath(working_directory)
	full_path_abs = os.path.abspath(full_path)

	if not full_path_abs.startswith(working_directory_abs):
		return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
	if not os.path.isfile(file_path):
		return f'Error: File not found or is not a regular file: "{file_path}"'

 
	with open(file_path, 'r') as f:
		file_content_string = f.read(MAX_CHARS)

	return file_content_string