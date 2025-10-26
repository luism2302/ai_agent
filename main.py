import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types



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

    generate_content(client, messages, verbose)

def generate_content(client, messages, verbose):
    response = client.models.generate_content(model = 'gemini-2.0-flash-001', contents = messages)
    print(response.text)
    if verbose:
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')

if __name__ == "__main__":
    main()
