import os, argparse
from config import GEMINI_API_KEY
from google import genai
from google.genai import types
from prompts import system_prompt

from functions.get_files_info import available_functions as gfi_functions
from functions.get_file_content import available_functions as gfc_functions
from functions.run_python_file import available_functions as rpf_functions
from functions.write_file import available_functions as wf_functions
from functions.call_function import call_function

def call_ai(args, client):
    
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[gfi_functions, gfc_functions, rpf_functions, wf_functions], 
            system_instruction=system_prompt)
        )
    
    if not response.usage_metadata:
        raise RuntimeError("Gemini did not respond")

    prompt_token_count = response.usage_metadata.prompt_token_count
    candidates_token_count = response.usage_metadata.candidates_token_count

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_token_count}")
        print(f"Response tokens: {candidates_token_count}")

    # f"Calling function: {function_call.name}({function_call.args})"
    if response.function_calls and len(response.function_calls) > 0:
        function_results = []
        for function_call in response.function_calls:
            # print(f"Calling function: {function_call.name}({function_call.args})")
            function_call_result = call_function(function_call, args.verbose)
            if not function_call_result.parts or len(function_call_result.parts) == 0:
                raise Exception("Unexpected result from calling local function")
            if function_call_result.parts[0].function_response == None:
                raise Exception("No response from local function")
            if function_call_result.parts[0].function_response.response == None:
                raise Exception("No response found in function_response")
            function_results.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(f"Response:\n{response.text}")

def main():

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    client = genai.Client(api_key=GEMINI_API_KEY)

    call_ai(args, client)


if __name__ == "__main__":
    main()
