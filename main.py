import os
import google.generativeai as genai
from telegram.ext import Updater, MessageHandler, Filters

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
chats = {}

def handle_message(update, context):
    user_id = update.effective_user.id
    text = update.message.text
    if user_id not in chats:
        chats[user_id] = model.start_chat(history=[])
    try:
        response = chats[user_id].send_message(text)
        update.message.reply_text(response.text)
    except Exception as e:
        update.message.reply_text("Ошибка 🙏")
        print(e)

updater = Updater(TELEGRAM_TOKEN)
updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
updater.start_polling()
updater.idle()

