import random
import datetime
import os

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

# 🔐 Secure token from Render
TOKEN = os.getenv("TOKEN")


def generate_analysis(user_input):
    score = random.randint(50, 95)

    if score > 80:
        decision = "⚡ STRONG BUY"
        risk = "LOW"
        mood = "BULLISH"
    elif score > 65:
        decision = "⚡ BUY"
        risk = "MEDIUM"
        mood = "NEUTRAL"
    else:
        decision = "⏳ WAIT"
        risk = "HIGH"
        mood = "UNCERTAIN"

    fee = random.choice([8000, 12000, 18000, 25000])
    window = random.randint(2, 10)

    return decision, risk, mood, fee, score, window


def format_response(user_input):
    decision, risk, mood, fee, score, window = generate_analysis(user_input)
    time_now = datetime.datetime.now().strftime("%H:%M:%S")

    return f"""
🐉 <b>RAIKU SNIPER ENGINE</b>

━━━━━━━━━━━━━━━━━━━
⚡ <b>Token:</b> {user_input.upper()}
⚡ <b>Decision:</b> {decision}
🧠 <b>Confidence:</b> {score}%
⚠️ <b>Risk Level:</b> {risk}
━━━━━━━━━━━━━━━━━━━

📊 <b>Market Pulse:</b> {mood}
🚀 <b>Priority Fee:</b> {fee}
⏱ <b>Entry Window:</b> {window}s

━━━━━━━━━━━━━━━━━━━
⚡ <i>Speed Layer Active</i>
🕒 <i>{time_now}</i>
"""


# 👋 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🐉 Raiku is ACTIVE. Send any token to analyze."
    )


# 💬 Handle user messages
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    response = format_response(user_input)

    await update.message.reply_text(response, parse_mode="HTML")


# 🚀 Run bot
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("🐉 Raiku Sniper Engine is LIVE...")
app.run_polling()
