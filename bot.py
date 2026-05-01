import os
import requests
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# 🔍 Fetch real data from CoinGecko
def get_crypto_data(coin):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd&include_24hr_change=true"
    response = requests.get(url).json()

    if coin not in response:
        return None

    price = response[coin]["usd"]
    change = response[coin]["usd_24h_change"]

    return price, change


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🐉 Raiku is ACTIVE.\nUse /analyze bitcoin"
    )


async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /analyze bitcoin")
        return

    coin = context.args[0].lower()
    data = get_crypto_data(coin)

    if not data:
        await update.message.reply_text("❌ Coin not found")
        return

    price, change = data

    # Simple logic (you can improve later)
    decision = "BUY" if change > 0 else "SELL"
    risk = "LOW" if abs(change) < 3 else "HIGH"

    time_now = datetime.now().strftime("%H:%M:%S")

    response = f"""
🐉 RAIKU SNIPER ENGINE
━━━━━━━━━━━━━━━━━━━

⚡ Token: {coin.upper()}
💲 Price: ${price:,.2f}
📊 24h Change: {change:.2f}%

⚡ Decision: {decision}
⚠️ Risk: {risk}

━━━━━━━━━━━━━━━━━━━

📊 Market Pulse: {"BULLISH" if change > 0 else "BEARISH"}
🚀 Priority Fee: 12000
⏱ Entry Window: 3s

━━━━━━━━━━━━━━━━━━━

⚡ Speed Layer Active
🕒 {time_now}
"""

    await update.message.reply_text(response)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("analyze", analyze))

app.run_polling()
