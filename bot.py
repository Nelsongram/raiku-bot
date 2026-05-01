import random
import datetime
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = "8502726343:AAHuZ-vsi-7iFjhj3rwgj9qqy_phRxJmHkU"


# 🔹 GET REAL DATA FROM COINGECKO
def get_price_data(token):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{token}"
        data = requests.get(url).json()
        price = data["market_data"]["current_price"]["usd"]
        change = data["market_data"]["price_change_percentage_24h"]
        return price, change
    except:
        return None, None


# 🔹 ANALYSIS ENGINE
def generate_analysis(user_input):
    price, change = get_price_data(user_input)

    if price is None:
        return None

    if change > 5:
        decision = "⚡ STRONG BUY"
        risk = "LOW"
        mood = "BULLISH"
    elif change > 0:
        decision = "⚡ BUY"
        risk = "MEDIUM"
        mood = "NEUTRAL"
    else:
        decision = "⏳ WAIT"
        risk = "HIGH"
        mood = "BEARISH"

    fee = 12000
    window = 3

    return decision, risk, mood, fee, change, window, price


# 🔹 FORMAT RESPONSE
def format_response(user_input):
    result = generate_analysis(user_input)

    if result is None:
        return "❌ Token not found. Try: bitcoin, ethereum, solana"

    decision, risk, mood, fee, change, window, price = result
    time_now = datetime.datetime.now().strftime("%H:%M:%S")

    return f"""
🐉 <b>RAIKU SNIPER ENGINE</b>

━━━━━━━━━━━━━━━━━━━
⚡ <b>Token:</b> {user_input.upper()}
💲 <b>Price:</b> ${price}
📊 <b>24h Change:</b> {change:.2f}%
⚡ <b>Decision:</b> {decision}
⚠️ <b>Risk:</b> {risk}
━━━━━━━━━━━━━━━━━━━

📊 <b>Market Pulse:</b> {mood}
🚀 <b>Priority Fee:</b> {fee}
⏱ <b>Entry Window:</b> {window}s

━━━━━━━━━━━━━━━━━━━
⚡ <i>Speed Layer Active</i>
🕒 <i>{time_now}</i>
"""


# 🔹 COMMANDS
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🐉 Raiku is ACTIVE. Use /analyze bitcoin")


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🐉 COMMANDS:
/start
/help
/analyze bitcoin
""")


async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /analyze bitcoin")
        return

    token = context.args[0].lower()
    response = format_response(token)
    await update.message.reply_text(response, parse_mode="HTML")


# 🔹 HANDLE NORMAL TEXT
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.lower()
    response = format_response(user_input)
    await update.message.reply_text(response, parse_mode="HTML")


# 🔹 RUN BOT
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("analyze", analyze))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("🐉 Raiku Sniper Engine is LIVE...")

app.run_polling()