import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

chats = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in chats:
        chats[user_id] = model.start_chat(history=[])

    await update.message.chat.send_action("typing")

    try:
        response = chats[user_id].send_message(text)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("Ошибка, попробуй ещё раз 🙏")
        print(f"Ошибка: {e}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущен v2!")
    app.run_polling()

if __name__ == "__main__":
    main()

