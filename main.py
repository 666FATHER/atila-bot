import os, requests, telebot
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
bot.delete_webhook(drop_pending_updates=True)
@bot.message_handler(commands=['marea','start'])
def h(m):
    try:
        p = float(requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=10).json()['price'])
    except:
        p = 77271
    bot.reply_to(m, f"🌊 ATILA MAREA\nBTC: {p}\n77108 SOPORTE\n77441 LIQ TECHO")

bot.infinity_polling()
