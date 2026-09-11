import os, requests, telebot, pandas as pd, time

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    print("FALTA BOT_TOKEN!")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)

def get_btc():
    try:
        p = float(requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5).json()['price'])
        kl = requests.get("https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=5m&limit=100", timeout=5).json()
        df = pd.DataFrame(kl)
        df[4] = df[4].astype(float)
        delta = df[4].diff()
        gain = delta.where(delta>0,0).rolling(14).mean()
        loss = -delta.where(delta<0,0).rolling(14).mean()
        rsi = 100 - (100/(1+gain/loss))
        return p, round(float(rsi.iloc[-1]),2)
    except Exception as e:
        print("Error BTC:", e)
        return 77271.21, 42.23

@bot.message_handler(commands=['marea','start','tempo'])
def marea(m):
    price, rsi = get_btc()
    txt = f"""🌊 /marea ATILA - BTC {price:.2f}

RSI M5: {rsi}
77108 SOPORTE BALLENAS
77441 LIQ TECHO

⏱️ M15 REY AHORA - M5 solo entrada 77108
👉 Bajá 0.09 a 0.05 SL 77108
"""
    bot.send_message(m.chat.id, txt)

print("BOT ATILA INICIADO")
while True:
    try:
        bot.infinity_polling(timeout=20, long_polling_timeout=20)
    except Exception as e:
        print("Crash, reiniciando en 5s:", e)
        time.sleep(5)
