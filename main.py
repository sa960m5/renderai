from flask import Flask, request
import requests
import os

app = Flask(__name__)
API_KEY = os.getenv("GEMINI_API_KEY")

@app.route('/')
def home():
    return "✅ Gemini AI Chatbot is running!"

@app.route('/chat', methods=['GET'])
def chat():
    user_message = request.args.get('msg', '')

    if not user_message:
        return "⚠️ No message provided."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=GEMINI_API_KEY"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [{"text": user_message}]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        ai_reply = response.json()['candidates'][0]['content']['parts'][0]['text']
        return ai_reply[:200]  # Trim to 200 characters for Nightbot
    except Exception as e:
        return f"❌ Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
