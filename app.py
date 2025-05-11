from flask import Flask, request, jsonify
from flask_cors import CORS
from pdf_to_text import pdf_to_text
from summarize import summarize_text
from extract_risks import extract_risks
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",
            os.environ.get("FRONTEND_URL", ""),
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set. Please set it in your .env file or environment variables.")

client = OpenAI(
    api_key= api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    print("analyzing text")
    try:
        data = request.get_json()
        text = data.get('text')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Get summary and risks
        summary = summarize_text(text)
        risks = extract_risks(text)

        # Format risks into the expected structure
        risky_terms = []
        for risk in risks:
            # Split risk into term and explanation
            parts = risk.split(':', 1)
            if len(parts) == 2:
                term = parts[0].strip()
                explanation = parts[1].strip()
                # Determine severity based on keywords
                severity = "medium"
                if any(word in term.lower() for word in ["critical", "severe", "high"]):
                    severity = "high"
                elif any(word in term.lower() for word in ["minor", "low"]):
                    severity = "low"
                
                risky_terms.append({
                    "term": term,
                    "severity": severity,
                    "explanation": explanation
                })

        response = {
            "simplifiedExplanation": summary,
            "riskyTerms": risky_terms
        }
        
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/followup', methods=['POST'])
def followup():
    try:
        data = request.get_json()
        question = data.get('question')
        original_text = data.get('originalText')
        
        if not question or not original_text:
            return jsonify({"error": "Question and original text are required"}), 400

        prompt = f"""You are a legal expert assistant. Answer the following question about this legal clause clearly and concisely.

Original text: {original_text}

Question: {question}

Answer:"""

        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[
                {"role": "system", "content": "You are a legal expert assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        
        answer = response.choices[0].message.content
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/extract', methods=['POST'])
def extract():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
            
        file = request.files['file']
        if not file.filename.endswith('.pdf'):
            return jsonify({"error": "Only PDF files are supported"}), 400

        # Extract text from PDF
        text, error = pdf_to_text(file)
        if error:
            return jsonify({"error": error}), 400

        return jsonify({"text": text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Get port from environment variable for Render
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("DEBUG", "False").lower() == "true"
    app.run(host='0.0.0.0', port=port, debug=debug)