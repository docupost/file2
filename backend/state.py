# state.py
# Global shared application state

# Stores data for each active user room.
# Structure:
# user_rooms = {
#     "room_id": {
#         "email": "user@example.com",
#         "name": "John Doe",
#         "greeting": "Hello!",
#         "expect_greeting": False
#     }
# }

user_rooms = {}
