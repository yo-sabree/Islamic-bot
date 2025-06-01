import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Your environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# LLM Model name from Together API
LLM_MODEL = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"

# System prompt for Islamic answers
SYSTEM_PROMPT = (
    "You are an Islamic teacher chatbot. Only answer based on the Qur’an, authentic Hadith, and respected scholars. "
    "Be kind and respectful to Sunni, Shia, and others. Give short answers for simple questions, and detailed ones when needed."
)

# Function to call Together.ai API
def get_ai_reply(message: str) -> str:
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message}
        ],
        "max_tokens": 500,
        "temperature": 0.6
    }

    try:
        response = requests.post("https://api.together.xyz/v1/chat/completions", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Sorry, something went wrong while contacting the AI: {e}"

# Telegram handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    reply = get_ai_reply(user_message)
    await update.message.reply_text(reply)

# Bot startup
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot is running...")
    app.run_polling()
