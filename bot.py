import os
import requests
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# 🔍 Get trending pairs (DexScreener)
def get_trending():
    url = "https://api.dexscreener.com/latest/dex/tokens/solana"
    data = requests.get(url).json()

    pairs = data.get("pairs", [])
    results = []

    for pair in pairs[:5]:  # top 5
        name = pair["baseToken"]["name"]
        price = pair.get("priceUsd", "0")
        change = pair.get("priceChange", {}).get("h24", 0)
        volume = pair.get("volume", {}).get("h24", 0)
        liquidity = pair.get("liquidity", {}).get("usd", 0)

        # 🧠 SNIPER LOGIC
        if volume > 10000 and liquidity > 20000:
            signal = "🚀 BUY"
        else:
            signal = "⚠️ WATCH"

        results.append({
            "name": name,
            "price": price,
            "change": change,
            "volume": volume,
            "liquidity": liquidity,
            "signal": signal
        })

    return results


# 📊 Analyze command (keep your old feature)
async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /scan for live sniper signals")


# 🚀 SNIPER SCAN
async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_trending()

    msg = "🐉 RAIKU SNIPER SCAN\n━━━━━━━━━━━━━━━\n\n"

    for coin in data:
        msg += f"""
⚡ {coin['name']}
💲 ${coin['price']}
📊 24h: {coin['change']}%
💧 Liquidity: ${coin['liquidity']}
📈 Volume: ${coin['volume']}
🎯 Signal: {coin['signal']}

━━━━━━━━━━━━━━━
"""

    msg += f"\n⚡ Scan Time: {datetime.now().strftime('%H:%M:%S')}"

    await update.message.reply_text(msg)


# 🟢 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🐉 Raiku Sniper ACTIVE\n\nCommands:\n/analyze bitcoin\n/scan (LIVE SNIPER)"
    )


# 🚀 RUN BOT
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("analyze", analyze))
app.add_handler(CommandHandler("scan", scan))

app.run_polling()
