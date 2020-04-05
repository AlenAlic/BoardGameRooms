from flask_socketio import emit


def send_game_message(room, message_id, data=None):
    if room is not None:
        emit("game_message", {
            "message_id": message_id,
            "data": data
        }, room=room)
