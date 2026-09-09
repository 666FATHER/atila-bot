import os, telebot, requests, time
from datetime import date
BOT_TOKEN=os.getenv("BOT_TOKEN");CHAT_ID=os.getenv("CHAT_ID");TD_KEY=os.getenv("TWELVEDATA_KEY","demo")
bot=telebot.TeleBot(BOT_TOKEN)
GENESIS_BTC=date(2009,1,3)
def get_klines_binance(symbol,interval="5m",limit=100):
    url=f"https://data-api.binance.vision/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        r=requests.get(url,timeout=15).json()
        if isinstance(r,list): return [float(k[4]) for k in r],[float(k[5]) for k in r]
    except: pass
    return [],[]
def get_klines_xauusd(interval="5min",limit=100):
    try:
        url=f"https://api.twelvedata.com/time_series?symbol=XAU/USD&interval={interval}&apikey={TD_KEY}&outputsize={limit}"
        r=requests.get(url,timeout=15).json()
        if 'values' in r:
            vals=r['values'][::-1]
            return [float(v['close']) for v in vals],[0]*len(vals)
    except: pass
    return [],[]
def get_price_xauusd():
    try: return float(requests.get("https://api.gold-api.com/price/XAU",timeout=10).json()['price'])
    except: return 0
def ema(data,p):
    if len(data)<p: return 0
    e=sum(data[:p])/p;k=2/(p+1)
    for v in data[p:]: e=v*k+e*(1-k)
    return e
def rsi(closes,p=14):
    if len(closes)<p+1: return 50
    g,l=[],[]
    for i in range(1,len(closes)):
        d=closes[i]-closes[i-1]
        g.append(max(d,0));l.append(max(-d,0))
    ag=sum(g[-p:])/p;al=sum(l[-p:])/p
    if al==0: return 70
    return 100-(100/(1+ag/al))
def btc_power_law():
    days=(date.today()-GENESIS_BTC).days
    fair=(10**-17)*(days**5.8)
    return fair,fair*0.42
def gold_power_law():
    closes,_=get_klines_xauusd("1week",250)
    if len(closes)<200: closes,_=get_klines_binance("PAXGUSDT","1w",250)
    ma200=sum(closes[-200:])/200 if len(closes)>=200 else 2000
    return ma200,ma200*0.78
def get_cot_us(q="GOLD"):
    try:
        name="GOLD - COMMODITY EXCHANGE INC" if q=="GOLD" else "BITCOIN"
        url=f"https://public-reporting.cftc.gov/resource/6dca-aqww.json?$limit=1&$order=report_date_as_yyyy_mm_dd DESC&$where=market_and_exchange_names like '%{name}%'"
        r=requests.get(url,timeout=15).json()
        if not r: return 1.0,0,"N/A"
        last=r[0]
        cl=float(last.get('prod_merc_positions_long_all',0))+float(last.get('swap_positions_long_all',0))
        cs=float(last.get('prod_merc_positions_short_all',0))+float(last.get('swap_positions_short_all',0))
        ratio=cl/cs if cs>0 else 1.0
        return ratio,cl-cs,last.get('report_date_as_yyyy_mm_dd','')
    except: return 1.0,0,"err"
def check_scalp_5m(typ):
    if typ=="BTCUSD": c,v=get_klines_binance("BTCUSDT","5m",100)
    else:
        c,v=get_klines_xauusd("5min",100)
        if not c: c,v=get_klines_binance("PAXGUSDT","5m",100)
    if len(c)<30: return False,0,0,0,0
    e9=ema(c,9);e21=ema(c,21);r=rsi(c,14)
    ok=e9>e21 and c[-2]<e21 and r>52 and r<72
    return ok,c[-1],e9,e21,r
def main_loop():
    while True:
        try:
            fair_btc,low_btc=btc_power_law()
            c_btc,_=get_klines_binance("BTCUSDT","1h",2)
            p_btc=c_btc[-1] if c_btc else 0
            ratio_btc,net_btc,date_btc=get_cot_us("BTC")
            dist_btc=p_btc/low_btc if low_btc else 10
            htf_btc=dist_btc<1.6 and ratio_btc>0.8
            print(f"BTCUSD ${p_btc:.0f} Low ${low_btc:.0f} Dist {dist_btc:.2f}x COT_US {ratio_btc:.2f}")
            if htf_btc:
                ok,price5,e9,e21,r=check_scalp_5m("BTCUSD")
                if ok: bot.send_message(CHAT_ID,f"🟢 SEÑA SCALP BTCUSD FATHER\nHTF EEUU: PowerLow {dist_btc:.2f}x + COT {ratio_btc:.2f} ({date_btc})\n5m: ${price5:.0f} EMA9 {e9:.0f}>EMA21 {e21:.0f} RSI {r:.0f}")
            fair_g,low_g=gold_power_law()
            p_gold=get_price_xauusd()
            ratio_g,net_g,date_g=get_cot_us("GOLD")
            dist_g=p_gold/low_g if low_g else 10
            htf_g=dist_g<1.18
            print(f"XAUUSD ${p_gold:.0f} Low ${low_g:.0f} Dist {dist_g:.2f}x COT_US {ratio_g:.2f}")
            if htf_g:
                ok,price5,e9,e21,r=check_scalp_5m("XAUUSD")
                if ok: bot.send_message(CHAT_ID,f"🟡 SEÑA SCALP XAUUSD FATHER\nHTF EEUU: PowerLow {dist_g:.2f}x + COT {ratio_g:.2f} Net {net_g:.0f} ({date_g})\n5m: ${price5:.0f} EMA9 {e9:.0f}>EMA21 {e21:.0f} RSI {r:.0f}")
        except Exception as e: print(f"Error: {e}")
        time.sleep(300)
if __name__=="__main__":
    bot.send_message(CHAT_ID,"✅ ATILA SCALP EEUU ON FATHER\nBTCUSD + XAUUSD\nPower Low + COT CFTC USA + 5m")
    main_loop()
