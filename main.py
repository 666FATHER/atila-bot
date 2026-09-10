import os, requests
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
TOKEN = (os.getenv("TELEGRAM_TOKEN") or os.getenv("BOT_TOKEN") or "").strip()
app_flask = Flask(__name__)
@app_flask.route('/')
def home(): return "ATILA VIVO"
def get_price(s):
    try:
        return float(requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={s}USDT", timeout=10).json()['price'])
    except: return 0.0
async def marea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    oro=get_price("PAXG");btc=get_price("BTC");eth=get_price("ETH");sol=get_price("SOL")
    await update.message.reply_text(f"🌊 ATILA - MAREA FATHER 🌊\n\n🥇 ORO: ${oro:,.2f}\n₿ BTC: ${btc:,.2f}\n💎 ETH: ${eth:,.2f}\n◎ SOL: ${sol:,.2f}\n\nBot: ACTIVO 24/7")
def main():
    Thread(target=lambda: app_flask.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080))), daemon=True).start()
    print(f"ATILA INICIADO TOKEN ...{TOKEN[-6:]}")
    app=ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("marea", marea))
    app.add_handler(CommandHandler("start", marea))
    app.run_polling()
if __name__ == "__main__": main()
