import openai
import os
from dotenv import load_dotenv

# Load the OpenAI API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load the prompt templates once so they're not reloaded every call
with open("backend/models/system_prompt.txt", "r") as sys_file:
    system_prompt = sys_file.read()

with open("backend/models/telecom_prompt.txt", "r") as user_file:
    telecom_prompt = user_file.read()

def analyze_transcript(transcript: str) -> str:
    """
    Given a transcript string, send it to OpenAI GPT with the structured telecom prompt
    and return the insights as a natural language bullet list.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": transcript + "\n\n" + telecom_prompt}
    ]
    # gpt-4o-mini-2024-07-18 is a cheaper model if token cost is a priority
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.9,
            top_p=0.9,
            max_tokens=1000
        )
        return completion.choices[0].message.content.strip()

    except Exception as e:
        return f"[Error generating GPT insights: {e}]"
