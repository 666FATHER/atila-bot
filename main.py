import os, threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
TOKEN=os.getenv("BOT_TOKEN","").strip()
app_f=Flask(__name__)
@app_f.route("/")
def home(): return "OK"
async def pro(u,c): await u.message.reply_text("ATILA VIVO FATHER")
async def start(u,c): await u.message.reply_text("VIVO /pro")
def run(): app_f.run(host="0.0.0.0",port=int(os.environ.get("PORT",8080)))
if __name__=="__main__":
 threading.Thread(target=run,daemon=True).start()
 a=Application.builder().token(TOKEN).build()
 a.add_handler(CommandHandler("start",start))
 a.add_handler(CommandHandler("pro",pro))
 print("ATILA OK")
 a.run_polling()
