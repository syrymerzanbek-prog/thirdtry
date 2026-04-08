from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json
import os

TOKEN =("8650085467:AAEm-esCEKUaAaIjUcJwSLM1UF16eyJK2dw")
ADMIN_ID = 5964805785
FILE_NAME = "data.json"

# --- загрузка текста ---
def load_message():
    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)["text"]
    except:
        return "Стандартное сообщение"

# --- сохранение текста ---
def save_message(text):
    with open(FILE_NAME, "w") as f:
        json.dump({"text": text}, f)

# --- команды ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["/send"], ["/set"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Добро пожаловать 👋",
        reply_markup=reply_markup
    )

async def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = load_message()
    await update.message.reply_text(text)

async def set_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("У тебя нет доступа ❌")
        return

    new_text = " ".join(context.args)
    if not new_text:
        await update.message.reply_text("Напиши текст после команды")
        return

    save_message(new_text)
    await update.message.reply_text("Сохранено ✅")

# --- запуск ---
app = (
    ApplicationBuilder()
    .token(TOKEN)
    .connect_timeout(30)
    .read_timeout(30)
    .write_timeout(30)
    .pool_timeout(30)
    .build()
)

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("send", send_message))
app.add_handler(CommandHandler("set", set_message))

app.run_polling()
