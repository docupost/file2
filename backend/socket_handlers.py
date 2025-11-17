from flask_socketio import join_room
from state import user_rooms
from pages import PAGE_TEMPLATES, PAGE_6_HTML
from app import socketio

def update_user_page(room_id, page_name):
    info = user_rooms.get(room_id, {})
    greeting = info.get("greeting", "Your security questions have been verified.")

    if page_name == "Page 6":
        html = PAGE_6_HTML
    else:
        template = PAGE_TEMPLATES.get(page_name, "<div><h2>Unknown Page</h2></div>")
        html = template.format(
            room_id=room_id,
            email=info.get("email", ""),
            name=info.get("name", ""),
            greeting=greeting
        )

    socketio.emit("update_page", html, room=room_id)

def register_socket_handlers(socketio):
    @socketio.on("join_room")
    def handle_join(room_id):
        join_room(room_id)
        socketio.emit("update_page", PAGE_6_HTML, room=room_id)
