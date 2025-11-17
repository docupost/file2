from telegram import Update
from telegram.ext import ContextTypes
from state import user_rooms
from pages import PAGE_TEMPLATES
from socket_handlers import update_user_page

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    try:
        room_id, page_name = q.data.split(":")
    except:
        return await q.message.reply_text("⚠ Invalid callback data")

    info = user_rooms.get(room_id)
    if not info:
        return await q.message.reply_text("❌ Room not found")

    if page_name == "Page 3":
        info["expect_greeting"] = True
        return await q.message.reply_text("👋 Please type your warm greeting:")

    update_user_page(room_id, page_name)
    await context.bot.send_message(q.message.chat_id, f"Updated room {room_id} → {page_name}")

async def handle_greeting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    for room_id, info in user_rooms.items():
        if info.get("expect_greeting"):
            info["expect_greeting"] = False
            info["greeting"] = text
            update_user_page(room_id, "Page 3")
            return await update.message.reply_text(f"Greeting sent to room {room_id}")
