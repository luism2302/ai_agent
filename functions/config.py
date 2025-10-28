MAX_CHARS = 10000
SYSTEM_PROMPT = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
The directory you are executing files from is called calculator.

In your responses, always include the functions you used.
"""

WORKING_DIR = './calculator'

MAX_ITERS = 20