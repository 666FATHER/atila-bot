import os, telebot, requests, time

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    print("Falta BOT_TOKEN o CHAT_ID en Variables")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

def get_klines(symbol, limit=100):
    urls = [
        f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit={limit}",
        f"https://data-api.binance.vision/api/v3/klines?symbol={symbol}&interval=1h&limit={limit}"
    ]
    for url in urls:
        try:
            r = requests.get(url, timeout=15)
            d = r.json()
            # Binance a veces devuelve {"msg": "error"} en vez de lista
            if isinstance(d, list) and len(d) > 20:
                closes = [float(k[4]) for k in d]
                vols = [float(k[5]) for k in d]
                return closes, vols
            else:
                print(f"Respuesta rara de Binance: {str(d)[:100]}")
        except Exception as e:
            print(f"Error pidiendo {symbol} en {url}: {e}")
            continue
    return [], []

def ema(data, p):
    if len(data) < p:
        return 0
    e = sum(data[:p]) / p
    k = 2 / (p + 1)
    for price in data[p:]:
        e = price * k + e * (1 - k)
    return e

def rsi(closes, p=14):
    if len(closes) < p + 1:
        return 50
    gains, losses = [], []
    for i in range(1, len(closes)):
        diff = closes[i] - closes[i-1]
        gains.append(max(diff, 0))
        losses.append(max(-diff, 0))
    ag = sum(gains[-p:]) / p
    al = sum(losses[-p:]) / p
    if al == 0:
        return 75
    rs = ag / al
    return 100 - (100 / (1 + rs))

def check_symbol(symbol):
    closes, vols = get_klines(symbol)
    if not closes:
        print(f"Sin datos para {symbol}, salto")
        return

    price = closes[-1]
    e9 = ema(closes, 9)
    e21 = ema(closes, 21)
    e50 = ema(closes, 50)
    r = rsi(closes, 14)
    vol_prom = sum(vols[-20:]) / 20 if len(vols) >= 20 else 0
    vol_ok = vols[-1] > vol_prom

    print(f"{symbol} P:{price:.2f} EMA9:{e9:.2f} EMA21:{e21:.2f} RSI:{r:.1f} VOL_OK:{vol_ok}")

    # Señal LONG
    if e9 > e21 and e21 > e50 and r > 50 and r < 70 and vol_ok:
        msg = f"🟢 ATILA LONG {symbol}\nPrecio: {price}\nEMA9 {e9:.1f} > EMA21 {e21:.1f} > EMA50 {e50:.1f}\nRSI: {r:.1f}\nVol: OK"
        bot.send_message(CHAT_ID, msg)
        print(f"Enviada señal LONG {symbol}")

def main_loop():
    symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"]
    while True:
        try:
            for sym in symbols:
                check_symbol(sym)
                time.sleep(2)
        except Exception as e:
            print(f"Error en main_loop: {e}")
        print("Durmiendo 5 min...")
        time.sleep(300)

if __name__ == "__main__":
    print("ATILA INICIADO - 666FATHER MODE")
    bot.send_message(CHAT_ID, "✅ ATILA conectado y arreglado FATHER - Ya no se cae")
    main_loop()
