import os
import requests
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

# -------------------------
# 🔍 GET REAL PRICE DATA
# -------------------------
def get_price(token):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={token}&vs_currencies=usd&include_24hr_change=true"
    res = requests.get(url).json()

    if token not in res:
        return None

    price = res[token]["usd"]
    change = res[token]["usd_24h_change"]
    return price, change


# -------------------------
# 🧠 SNIPER LOGIC
# -------------------------
def sniper_decision(change):
    if change > 5:
        return "🚀 STRONG BUY", "LOW"
    elif change > 2:
        return "⚡ BUY", "MEDIUM"
    elif change < -5:
        return "❌ DUMP", "HIGH"
    else:
        return "😐 HOLD", "MEDIUM"


# -------------------------
# /start
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🐉 Raiku Sniper is LIVE\n\n"
        "Commands:\n"
        "/analyze bitcoin\n"
        "/scan\n"
        "/auto"
    )


# -------------------------
# /analyze
# -------------------------
async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Usage: /analyze bitcoin")
        return

    token = context.args[0].lower()

    data = get_price(token)

    if not data:
        await update.message.reply_text("Token not found")
        return

    price, change = data
    decision, risk = sniper_decision(change)

    msg = f"""
🐉 RAIKU SNIPER ENGINE
━━━━━━━━━━━━━━

⚡ Token: {token.upper()}
💲 Price: ${price}
📊 24h Change: {change:.2f}%

⚡ Decision: {decision}
⚠ Risk: {risk}

━━━━━━━━━━━━━━
⚡ Speed Layer Active
🕒 {datetime.now().strftime('%H:%M:%S')}
"""

    await update.message.reply_text(msg)


# -------------------------
# 🔥 /scan (MULTI TOKEN SNIPER)
# -------------------------
async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tokens = ["bitcoin", "ethereum", "solana"]

    results = "🐉 LIVE SNIPER SCAN\n━━━━━━━━━━━━━━\n"

    for token in tokens:
        data = get_price(token)
        if not data:
            continue

        price, change = data
        decision, _ = sniper_decision(change)

        if "BUY" in decision:
            results += f"\n🚀 {token.upper()} → {decision} ({change:.2f}%)"

    if results == "🐉 LIVE SNIPER SCAN\n━━━━━━━━━━━━━━\n":
        results += "\nNo sniper opportunities now."

    await update.message.reply_text(results)


# -------------------------
# 🤖 AUTO SNIPER (LOOP ALERT)
# -------------------------
async def auto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    await update.message.reply_text("🤖 Auto Sniper Activated...")

    while True:
        tokens = ["bitcoin", "ethereum", "solana"]

        for token in tokens:
            data = get_price(token)
            if not data:
                continue

            price, change = data
            decision, _ = sniper_decision(change)

            if "BUY" in decision:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"🚀 SNIPER ALERT\n{token.upper()} → {decision}\nPrice: ${price}"
                )

        await asyncio.sleep(30)  # scan every 30 seconds


# -------------------------
# 🚀 RUN BOT
# -------------------------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("analyze", analyze))
app.add_handler(CommandHandler("scan", scan))
app.add_handler(CommandHandler("auto", auto))

app.run_polling()
