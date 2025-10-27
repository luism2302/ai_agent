from functions.get_file_info import get_file_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file

def main():
	result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
	print(result)
	result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
	print(result)
	result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
	print(result)
if __name__ == "__main__":
	main()