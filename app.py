import os
import requests
from flask import Flask, request, Response
import openai
from openai import OpenAI

# Load environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
SEA_LION_API_KEY = os.getenv("SEA_LION_API_KEY")


TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
SEA_LION_API="https://api.sea-lion.ai/v1" 

client = OpenAI(
    api_key=SEA_LION_API_KEY,
    base_url=SEA_LION_API
)


app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Telegram Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()    
    # Check incoming message
    if not update or "message" not in update:
        return Response("", status=204)

    msg = update["message"]
    chat_id = msg["chat"]["id"]
    user_text = msg.get("text")

    if user_text:
        # Call OpenAI Chat API
        completion = client.chat.completions.create(
        model="aisingapore/Gemma-SEA-LION-v3-9B-IT",
        messages=[
            {
                "role": "user",
                "content": user_text
            }
        ]
        )       
        
        reply_text = completion.choices[0].message.content

        # Send reply back to Telegram
        requests.post(
            f"{TELEGRAM_API_URL}/sendMessage",
            json={"chat_id": chat_id, "text": reply_text}
        )

    return Response("OK", status=200)

if __name__ == "__main__":
    # Render.com will provide PORT environment variable
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
