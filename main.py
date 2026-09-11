import os, requests, telebot, pandas as pd
from flask import Flask
import threading

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "ATILA MAREA BOT ONLINE - BTC 77271"

def get_btc_data():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5).json()
        price = float(r['price'])
        kl = requests.get("https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=5m&limit=100", timeout=5).json()
        df = pd.DataFrame(kl, columns=['o','h','l','c','v','ct','qv','n','tb','tq','i'])
        df['c'] = df['c'].astype(float)
        df['h'] = df['h'].astype(float)
        df['l'] = df['l'].astype(float)
        delta = df['c'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rsi = 100 - (100 / (1 + gain/loss))
        tr = pd.concat([df['h']-df['l'], (df['h']-df['c'].shift()).abs(), (df['l']-df['c'].shift()).abs()], axis=1).max(axis=1)
        atr = tr.rolling(14).mean().iloc[-1]
        return price, round(rsi.iloc[-1],2), round(atr,2)
    except:
        return 77271.21, 42.23, 101.96

def get_oi():
    try:
        r = requests.get("https://fapi.binance.com/fapi/v1/openInterest?symbol=BTCUSDT", timeout=5).json()
        return float(r['openInterest'])
    except:
        return 198000 # fallback

@bot.message_handler(commands=['marea'])
def marea(m):
    price, rsi, atr = get_btc_data()
    oi = get_oi()
    oi_usd = oi * price / 1e9

    if atr > 100 and rsi < 45:
        tempo = "🔴 AHORA: M15 REY - M5 solo entrada en 77108 - M1 PROHIBIDO con 0.09"
        accion = f"⚠️ ESTÁS EN {price:.0f} ZONA NEUTRA - BAJÁ 0.09 A 0.05 - SL 77108"
        despues = "🟢 DESPUÉS: M3 cuando ATR <80 para scalp con 0.09"
    else:
        tempo = "🟢 M5 tendencia + M3 entrada"
        accion = "Operá extremos 77108-77441"
        despues = "M1 para TP"

    txt = f"""🌊 /marea ATILA - {price:.2f}

🔥 BTC: {price:.2f} | RSI M5: {rsi} | ATR: {atr}
🐋 OI Binance: {oi:.0f} BTC (~${oi_usd:.1f}B) vs MA $8.3B = INFLADO
📉 Total Red $60.6B - Deleveraging mas violento desde 2023

🎯 NIVELES:
77441.84 LIQ TECHO
{price:.0f} ACTUAL
77108.14 SOPORTE BALLENAS

💀 COT ORO:
Commercials -264K SHORT EXTREMO = DISTRIBUCION
IBIT Blackrock 785K BTC = ACUMULACION

⏱️ {tempo}
⏱️ {despues}

👉 {accion}
"""
    bot.send_message(m.chat.id, txt)

@bot.message_handler(commands=['tempo'])
def tempo(m):
    price, rsi, atr = get_btc_data()
    bot.send_message(m.chat.id, f"⏱️ TEMPO ATILA: BTC {price:.0f} RSI {rsi} ATR {atr}\n{'M15 AHORA' if atr>100 else 'M3 AHORA'}")

def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))
