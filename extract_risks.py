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

def extract_risks(text):
    try:
        prompt = f"""Extract risks from the following text. For each risk:
        1. Identify the risky term or clause
        2. Explain why it's risky
        Format each risk as 'Term: Explanation'
        
        Text: {text}"""
        
        response = model.generate_content(prompt)
        risks_text = response.text
        # Split risks by newline and return as an array
        risks_array = [risk.strip() for risk in risks_text.split('\n') if risk.strip()]
        return risks_array
    except Exception as e:
        return [f"Error: {str(e)}"]