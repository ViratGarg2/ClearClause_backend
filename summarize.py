import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")  # Using the same env var name for now
if not api_key:
    raise ValueError("API key environment variable is not set. Please set it in your .env file or environment variables.")

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-2.0-flash')

def summarize_text(text):
    try:
        response = model.generate_content(f"Summarize the following text: {text}")
        print('output is ', response.text)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"