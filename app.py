import os
import requests
import fitz  # PyMuPDF
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Function to extract all text from PDF
def extract_text_from_pdf(file_path):
    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()
    return text

# Load the PDF content once when the server starts
PDF_TEXT = extract_text_from_pdf("rayane-profile.pdf")

@app.route("/api/message", methods=["POST"])
def handle_message():
    user_input = request.json.get("message", "")

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt_context = (
    "You are an AI assistant answering questions based ONLY on the PDF content below.\n\n"
    "Please format your responses using:\n"
    "- Bullet points ✅\n"
    "- Short paragraphs 📄\n"
    "- Relevant emojis to make it more friendly and engaging 🎉🤖💡\n\n"
    "Here is the PDF content:\n"
    f"{PDF_TEXT}"
    )


    data = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": prompt_context},
            {"role": "user", "content": user_input}
        ]
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        ai_reply = response.json()["choices"][0]["message"]["content"]
        return jsonify({"response": ai_reply})
    else:
        print("OpenAI error:", response.text)
        return jsonify({"error": "Failed to fetch response"}), 500

@app.route("/")
def home():
    return "✅ Rayane's Chatbot (PDF-powered) is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



# git add app.py requirements.txt
# git commit -m "Added PDF support for chatbot"
# git push origin main


# git push origin main
