import os, sys
from dotenv import load_dotenv
from groq import Groq, types

def main():

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
            "role": "user",
            "content": user_prompt,
        }
    ]

    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-8b-8192",
    )

    print(chat_completion.choices[0].message.content)
    if verbose:
        #print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {chat_completion.usage.prompt_tokens}")
        print(f"Response tokens: {chat_completion.usage.completion_tokens}")

if __name__ == "__main__":
    main()