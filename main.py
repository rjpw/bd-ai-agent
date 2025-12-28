import os, argparse
from dotenv import load_dotenv

from google import genai
load_dotenv()

def main():

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=args.user_prompt)
    
    if not response.usage_metadata:
        raise RuntimeError("Gemini did not respond")

    prompt_token_count = response.usage_metadata.prompt_token_count
    candidates_token_count = response.usage_metadata.candidates_token_count

    print(f"Prompt tokens: {prompt_token_count}")
    print(f"Response tokens: {candidates_token_count}")
    print(f"Response:\n{response.text}")

if __name__ == "__main__":
    main()
