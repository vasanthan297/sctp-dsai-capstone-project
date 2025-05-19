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

# -------------------------------------------
# Instructions:
# 1. Set environment variables:
#    TELEGRAM_TOKEN, OPENAI_API_KEY (and optionally OPENAI_MODEL).
# 2. Deploy this app to Render.com (select Python service). 
#    start command in Render should be: gunicorn webhook:app
# 3. After deployment, set your Telegram webhook:
#    https://api.telegram.org/bot<YOUR_TELEGRAM_TOKEN>/setWebhook?url=https://<YOUR_RENDER_URL>/webhook
# 4. Test the bot by sending messages to it on Telegram.    
# -------------------------------------------
# Note: Ensure you have Flask and requests installed in your environment.
# You can install them using:
# pip install Flask requests openai
# -------------------------------------------
# This code is a simple Telegram bot that uses OpenAI's Chat API to respond to messages.
# It sets up a webhook to receive messages and sends replies using the OpenAI API.
# The bot is designed to be deployed on Render.com, but can be adapted for other platforms.
# -------------------------------------------
# This code is provided as a basic template and may require additional error handling and features
# depending on your specific use case.
# -------------------------------------------
# Make sure to follow best practices for security and error handling in production.
# -------------------------------------------