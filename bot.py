import os
import threading
from flask import Flask
from dotenv import load_dotenv
from urllib.parse import quote
from openai import OpenAI

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

# Flask app
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# OpenRouter AI client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Amazon affiliate link generator
def create_amazon_link(product_name):

    affiliate_tag = "productaffi07-21"

    search_query = quote(product_name)

    return f"https://www.amazon.in/s?k={search_query}&tag={affiliate_tag}"

# Telegram message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text

    try:

        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Suggest exactly 3 best budget-friendly products for:
                    {user_text}

                    IMPORTANT:
                    Write in this exact format:

                    Product: product name
                    Price: ₹price
                    Features: short features

                    Only give 3 products.
                    """
                }
            ]
        )

        ai_text = response.choices[0].message.content

        reply_text = "🔥 Best Recommendations\n\n"

        products = ai_text.split("Product:")

        for product in products[1:]:

            lines = product.strip().split("\n")

            product_name = lines[0].strip()

            amazon_link = create_amazon_link(product_name)

            reply_text += f"🛍 Product: {product_name}\n"

            for line in lines[1:]:
                reply_text += f"{line}\n"

            reply_text += f"\n🛒 Buy Here:\n{amazon_link}\n\n"

        await update.message.reply_text(reply_text)

    except Exception as e:

        print("REAL ERROR:", e)

        await update.message.reply_text(
            "⚠️ Something went wrong with AI."
        )

# Telegram app
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, handle_message))

print("AI Affiliate Bot Running...")

# Run Flask in separate thread
threading.Thread(target=run_flask).start()

# Run Telegram bot
app.run_polling()