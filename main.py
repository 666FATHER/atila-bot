import os
import requests
import telebot
import pandas as pd
import time

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

def get_btc():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        price = float(requests.get(url, timeout=10).json()['price'])
        return price
    except:
        return 77271.21

@bot.message_handler(commands=['marea','start'])
def marea(m):
    price = get_btc()
    bot.send_message(m.chat.id, f"🌊 ATILA MAREA\nBTC: {price}\n77108 SOPORTE\n77441 LIQ TECHO\nM15 REY - Entrada 77108")

print("BOT ATILA INICIADO")
while True:
    try:
        bot.infinity_polling()
    except Exception as e:
        print(e)
        time.sleep(5)
