import os
from google.genai import types

def write_file(working_directory, file_path, content):
	full_path = os.path.join(working_directory, file_path)
	working_directory_abs = os.path.abspath(working_directory)
	full_path_abs = os.path.abspath(full_path)

	if not full_path_abs.startswith(working_directory_abs):
		return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
	if not os.path.exists(full_path_abs):
		print(f'Path doesnt exist, attempting to create it...')
		try:
			os.makedirs(os.path.dirname(full_path_abs), exist_ok = True)
		except Exception as e:
			return f'Error: couldnt create new directory: {e}'
	if os.path.exists(full_path_abs) and os.path.isdir(full_path_abs):
		return f'Error: "{file_path}" is a directory, not a file'

	try:
		with open(full_path_abs, "w") as f:
			f.write(content)
			return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
	except Exception as e:
		return f'Error: couldnt write to {file_path}: {e}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the argument 'content' to the file located at 'file_path'. If the directory provided at file path doesn't exist, it creates it and then writes to it. The location of the python file is constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
			"content": types.Schema(
				type=types.Type.STRING,
				description="The contents to write to the specified file located at file_path"
			)
        },
    ),
)