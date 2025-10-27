import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.config import SYSTEM_PROMPT
from functions.get_files_info import schema_get_files_info



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

    available_functions = types.Tool(function_declarations = [schema_get_files_info,])
    generate_content(client, messages, verbose, available_functions)

def generate_content(client, messages, verbose, tools):
    response = client.models.generate_content(model = 'gemini-2.0-flash-001', contents = messages,  config = types.GenerateContentConfig(tools = [tools], system_instruction = SYSTEM_PROMPT))
    if verbose:
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
    if not response.function_calls:
        return response.text
    for call in response.function_calls:
        print(f"Calling function: {call.name}({call.args})")

if __name__ == "__main__":
    main()
