import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.config import SYSTEM_PROMPT
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function
from functions.config import MAX_ITERS


def main():
    load_dotenv()
    api_key = os.environ.get('GEMINI_API_KEY')
    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)
    if not args:
        print('Usage: uv run main.py <prompt> [--verbose]')
        sys.exit(1)

    prompt = " ".join(args)
    messages = [types.Content(role = 'user', parts = [types.Part(text = prompt)]),]
    client = genai.Client(api_key = api_key)

    if verbose:
        print(f'User prompt: {prompt}')

    available_functions = types.Tool(function_declarations = [schema_get_files_info, schema_write_file, schema_get_file_content, schema_run_python_file])
    iters = 0
    while True:
        iters += 1
        if iters >= MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached")
            sys.exit(1)
        try:
            final_response = generate_content(client, messages, verbose, available_functions)
            if final_response:
                print("Final response")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")


def generate_content(client, messages, verbose, tools):
    response = client.models.generate_content(model = 'gemini-2.0-flash-001', contents = messages,  config = types.GenerateContentConfig(tools = [tools], system_instruction = SYSTEM_PROMPT))
    if verbose:
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)
    if not response.function_calls:
        return response.text
    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (not function_call_result.parts or not function_call_result.parts[0].function_response):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])
    if not function_responses:
        raise Exception("no function responses generated, exiting")
    messages.append(types.Content(role="user", parts=function_responses))

if __name__ == "__main__":
    main()
