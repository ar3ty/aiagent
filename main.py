import os, sys, json
from dotenv import load_dotenv
from groq import Groq, types
from functions.get_files_info import schema_get_files_info

def main():
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print('Usage: uv run main.py <prompt> [--verbose]')
        sys.exit(1)

    user_prompt = " ".join(args)

    load_dotenv()
    api_key = os.environ.get("GROQ_API_KEY")

    client = Groq(api_key=api_key)

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ]

    tools = [
        schema_get_files_info
    ]

    generate_content(client, messages, tools, verbose)


def generate_content(client, messages, tools, verbose):
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama-3.3-70b-versatile",
        tools=tools,
        tool_choice="auto"
    )

    calls = chat_completion.choices[0].message.tool_calls
    if calls:
        for call in calls:
            to_print = f"Calling function: {call.function.name}( {call.function.arguments})"
            to_print = to_print.replace('"', "'")
            print(to_print)
    print(chat_completion.choices[0].message.content)
    if verbose:
        print(f"Prompt tokens: {chat_completion.usage.prompt_tokens}")
        print(f"Response tokens: {chat_completion.usage.completion_tokens}")

if __name__ == "__main__":
    main()