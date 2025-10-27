import os
import subprocess
import sys
from google.genai import types

def run_python_file(working_directory, file_path, args = []):
	full_path = os.path.join(working_directory, file_path)
	working_directory_abs = os.path.abspath(working_directory)
	full_path_abs = os.path.abspath(full_path)

	if not full_path_abs.startswith(working_directory_abs):
		return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
	if not os.path.exists(full_path_abs):
		return f'Error: File "{file_path}" not found.' 
	if not full_path_abs.endswith(".py"):
		return f'Error: "{file_path}" is not a Python file.'		

	try:
		commands = ['python', full_path_abs]
		if args:
			commands.extend(args)
		results = subprocess.run(commands ,timeout= 30, capture_output=True, cwd = working_directory_abs, text = True)

		output = []
		if results.stdout:
			output.append(f'STDOUT: {results.stdout}')
		if results.stderr:
			output.append(f'STDERR: {results.stderr}')
		if results.returncode != 0:
			output.append(f'Process exited with code: {results.returncode}')

		return "\n".join(output) if output else "No output produced"

	except Exception as e:
		return f"Error: error executing. {e}"
		
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a python file, using the subprocess.run function from pythons standard library. If the execution is succesful, it will return the outputs produced by the python script, if it did not produce any output, then the return will be 'No output produced'. The location of the python file is constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the python file to execute, relative to the working directory.",
            ),
			"args": types.Schema(
				type=types.Type.ARRAY,
				description="The arguments passed to the console when executing the file, they will vary depending on what the script needs to execute.",
				items=types.Schema(type=types.Type.STRING),
			),
        },
    ),
)