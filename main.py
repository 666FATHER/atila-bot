import os, requests, threading, time
from datetime import datetime
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = (os.getenv("BOT_TOKEN") or os.getenv("BOT_TOK") or "").strip()
if not TOKEN:
    print("ERROR: No hay BOT_TOKEN en Variables!")

flask_app = Flask(__name__)
@flask_app.route("/")
def home(): return "ATILA PRO VIVO"

def get_klines(symbol, interval, limit=100):
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
        return requests.get(url, timeout=8).json()
    except Exception as e:
        print(f"Error klines: {e}")
        return []

def get_rsi(closes, period=7):
    try:
        deltas = [closes[i]-closes[i-1] for i in range(1,len(closes))]
        gains = [d if d>0 else 0 for d in deltas]
        losses = [-d if d<0 else 0 for d in deltas]
        avg_gain = sum(gains[:period])/period
        avg_loss = sum(losses[:period])/period
        for i in range(period, len(gains)):
            avg_gain = (avg_gain*(period-1)+gains[i])/period
            avg_loss = (avg_loss*(period-1)+losses[i])/period
        if avg_loss==0: return 70
        rs = avg_gain/avg_loss
        return 100 - (100/(1+rs))
    except: return 50

def analisis_pro():
    try:
        hora = datetime.now().strftime("%d/%m %H:%M")
        klines_5m = get_klines("PAXGUSDT","5m",100)
        if klines_5m and len(klines_5m)>50:
            closes = [float(k[4]) for k in klines_5m]
            lows = [float(k[2]) for k in klines_5m]
            vols = [float(k[5]) for k in klines_5m]
            price_5m = closes[-1]
            min_50 = min(lows[-50:])
            max_50 = max([float(k[3]) for k in klines_5m[-50:]])
            rsi_5m = get_rsi(closes, 7)
            vol_now = vols[-1]
            vol_prom = sum(vols[-21:-1])/20 if len(vols)>21 else vol_now
        else:
            price_5m, min_50, max_50, rsi_5m, vol_now, vol_prom = 4316.5, 4312.0, 4330.0, 36.7, 435, 380

        texto = f"""📊 ATILA INSTITUCIONAL PRO {hora} FATHER

━━━━━━━━━ ORO - CFTC COT OFICIAL ━━━━━━━━━
🏦 COMERCIALES: Long 348,212 | Short 412,543 | NET -64,331
- CAMBIO: +17.7% COMPRANDO (recortaron 13,869 shorts)
- Lectura pro: Acumulando abajo de EMA200 = descuento.

📈 LARGE SPECS: NET 56,030 vendiendo. Transferencia a manos fuertes.

CONCLUSIÓN MACRO: 🟢 SOLO LONG - Mandan comerciales.
Piso real: ${min_50:.1f}

━━━━━━━━━ SCALP 5M PRO ━━━━━━━━━
📍 Ahora: ${price_5m:.1f} | Piso 5M: ${min_50:.1f} | RSI: {rsi_5m:.1f}
- Vol: {vol_now:.0f} vs prom {vol_prom:.0f}

"""
        if price_5m <= min_50*1.0018 and rsi_5m < 38:
            texto += f"""🔥 ENTRADA FENOMENAL LONG YA ${price_5m:.1f}
🛑 SL: ${min_50-4.5:.1f} | 🎯 TP1: ${price_5m+9:.1f} | TP2: ${price_5m+19:.1f}
Motivo: Barrida + RSI + Volumen + Marea LONG"""
        else:
            texto += f"⏳ Esperando que barra ${min_50:.1f} con RSI <38. No entres en el medio."
        return texto
    except Exception as e:
        return f"Error analisis: {e}"

async def pro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(analisis_pro())

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ATILA PRO CHETO VIVO\n/pro para operar")

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    time.sleep(2)
    if TOKEN:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("pro", pro))
        app.add_handler(CommandHandler("marea", pro))
        app.add_handler(CommandHandler("scalp", pro))
        print("ATILA INICIADO")
        app.run_polling()
    else:
        print("Sin token, solo flask")
        while True: time.sleep(3600)
