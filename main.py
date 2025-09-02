import os, sys
from dotenv import load_dotenv
from groq import Groq
from tools import system_prompt, available_tools, call_function

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
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ]

    tools = available_tools

    for i in range(20):
        try:
            result = generate_content(client, messages, tools, verbose)
            if isinstance(result, str):
                print("Final response:")
                print(result)
                break
            messages = result
        except Exception as e:
            print(f"Error: {e}")
    
    if i == 20:
        print('max iterations limit is reached')


def generate_content(client, messages, tools, verbose):
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama-3.3-70b-versatile",
        tools=tools,
        tool_choice="auto"
    )

    if verbose:
        print(f"Prompt tokens: {chat_completion.usage.prompt_tokens}")
        print(f"Completion tokens: {chat_completion.usage.completion_tokens}")

    for choice in chat_completion.choices:
        messages.append(choice.message)

    calls = chat_completion.choices[0].message.tool_calls

    if not calls:
        return chat_completion.choices[0].message.content

    function_responses = []
    for call in calls:
        result = call_function(call, verbose)
        if len(result) == 0:
            raise Exception(f"smth is wrong: no content in result of function {call.function.name}")
        if verbose:
            print(f"-> {result}")
        result_message = {
            "tool_call_id": call.id,
            "role": "tool",
            "name": call.function.name,
            "content": result
        }
        
        function_responses.append(result_message)
        messages.append(result_message)
    
    return messages

if __name__ == "__main__":
    main()