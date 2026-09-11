import os, requests, telebot
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
bot.delete_webhook(drop_pending_updates=True)

@bot.message_handler(commands=['marea','start'])
def marea(m):
    try:
        p = float(requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=10).json()['price'])
    except:
        p = 77271.0
    bot.reply_to(m, f"🌊 ATILA MAREA\nBTC: {p}\n77108 SOPORTE\n77441 TECHO")

print("BOT PRENDIDO")
bot.infinity_polling()
