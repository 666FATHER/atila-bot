import os, telebot, requests
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = telebot.TeleBot(BOT_TOKEN)

def get_klines(symbol, limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=5m&limit={limit}"
    d = requests.get(url, timeout=10).json()
    closes = [float(k[4]) for k in d]
    vols = [float(k[5]) for k in d]
    return closes, vols

def ema(data, p):
    e = sum(data[:p])/p
    k = 2/(p+1)
    for price in data[p:]:
        e = price*k + e*(1-k)
    return e

def rsi(closes, p=14):
    gains, losses = [], []
    for i in range(1, len(closes)):
        diff = closes[i]-closes[i-1]
        gains.append(max(diff,0)); losses.append(abs(min(diff,0)))
    ag = sum(gains[-p:])/p; al = sum(losses[-p:])/p
    if al==0: return 75
    return 100 - (100/(1+ag/al))

def analizar_5m(symbol):
    closes, vols = get_klines(symbol)
    price = closes[-1]
    ema9 = ema(closes, 9); ema21 = ema(closes, 21); ema50 = ema(closes, 50)
    rsi14 = rsi(closes, 14)
    vol_avg = sum(vols[-20:-1])/19; vol_now = vols[-1]
    tendencia = "ALCISTA" if ema9 > ema21 and ema21 > ema50 else "BAJISTA" if ema9 < ema21 and ema21 < ema50 else "LATERAL"
    if ema9 > ema21 and price > ema21 and 35 < rsi14 < 58 and tendencia=="ALCISTA" and vol_now > vol_avg*1.2:
        return f"🟢 ATILA 5M LONG {symbol}\n💰 Entrada 5M: ${price:.4f}\nRSI {rsi14:.1f} Tend {tendencia}\n📍 ENTRADA CIERRE VELA 5M\n🛑 SL ${price*0.997:.4f} (-0.3%)\n🎯 TP1 ${price*1.005:.4f} (+0.5%)\n🎯 TP2 ${price*1.01:.4f} (+1%)"
    elif ema9 < ema21 and price < ema21 and 42 < rsi14 < 68 and tendencia=="BAJISTA" and vol_now > vol_avg*1.2:
        return f"🔴 ATILA 5M SHORT {symbol}\n💰 Entrada 5M: ${price:.4f}\nRSI {rsi14:.1f} Tend {tendencia}\n📍 ENTRADA CIERRE VELA 5M\n🛑 SL ${price*1.003:.4f} (+0.3%)\n🎯 TP1 ${price*0.995:.4f} (-0.5%)\n🎯 TP2 ${price*0.99:.4f} (-1%)"
    else:
        return f"🟡 {symbol} NO ENTRAR 5M\n💰 ${price:.4f} RSI {rsi14:.1f} Tend {tendencia}\nEspera proxima vela 5m FATHER"

@bot.message_handler(commands=['start','analizar','senal'])
def handler(m):
    txt = m.text
    if "senal" in txt:
        bot.reply_to(m, "⚡️ ATILA 5M escaneando...")
        for c in ["BTCUSDT","ETHUSDT","SOLUSDT"]:
            bot.send_message(m.chat.id, analizar_5m(c))
    else:
        parts = txt.split()
        coin = parts[1].upper() if len(parts)>1 else "BTC"
        if "USDT" not in coin: coin+="USDT"
        bot.send_message(m.chat.id, analizar_5m(coin))

print("ATILA 5M PURO INICIADO")
bot.infinity_polling()
