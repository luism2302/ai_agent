from functions.get_file_info import get_file_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
def main():
	results = run_python_file("calculator", "main.py")
	print(results)
	results = run_python_file("calculator", "main.py", ["3 + 5"])
	print(results)
	results = run_python_file("calculator", "tests.py")
	print(results)
	results = run_python_file("calculator", "../main.py")
	print(results)
	results = run_python_file("calculator", "nonexistent.py")
	print(results)
	results = run_python_file("calculator", "lorem.txt")
	print(results)
if __name__ == "__main__":
	main()