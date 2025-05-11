import openai
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set. Please set it in your .env file or environment variables.")


client = OpenAI(
    api_key= api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def extract_risks(text):
    try:
        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Extract risks from the following text: {text}"}
            ]
        )
        risks_text = response.choices[0].message.content
        # Split risks by newline and return as an array
        risks_array = [risk.strip() for risk in risks_text.split('\n') if risk.strip()]
        return risks_array
    except Exception as e:
        return [f"Error: {str(e)}"]