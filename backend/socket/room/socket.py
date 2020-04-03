from backend.socket import socket_io
from flask_socketio import emit, send, join_room, leave_room
from flask import request
from datetime import datetime
from backend.models.room import Room
from backend.models.user import User


ROOMS = {}


@socket_io.on("create_game_room")
def create_game_room(data):
    """Create a game room"""
    # noinspection PyUnresolvedReferences
    sid = request.sid
    room = data.get("room", None)
    username = data.get("username", None)
    password = data.get("password", None)
    if all([room not in ROOMS, room is not None, username is not None]):
        admin = User(username=username, sid=sid)
        ROOMS[room] = Room(room=room, password=password, admin=admin)
        join_room(room)
        emit("room_created", {
            "room": ROOMS[room].json(),
            "user": admin.json()
        }, room=room)
    else:
        send("room_exists", room=sid)


def user_join_room(user, room, sid):
    join_room(room)
    emit("room_joined", {
        "room": ROOMS[room].json(),
        "user": user.json(),
    }, room=sid)
    emit("room_user_joined", {
        "room": ROOMS[room].json(),
        "user": user.json(),
    }, room=room, include_self=False)
    # send_chat_message(room, message=f"{user.username} has joined the room.")


@socket_io.on("join_game_room")
def join_game_room(data):
    """Join an existing game room"""
    # noinspection PyUnresolvedReferences
    sid = request.sid
    room = data.get("room")
    username = data.get("username")
    password = data.get("password")
    if all([room is not None, username is not None, room in ROOMS]):
        if ROOMS[room].check_password(password):
            if not ROOMS[room].check_username(username):
                if ROOMS[room].can_join():
                    user = User(username=username, sid=sid)
                    ROOMS[room].join(user)
                    user_join_room(user, room, sid)
                else:
                    send("room_max_capacity", room=sid)
            else:
                send("room_username_taken", room=sid)
        else:
            send("room_password_incorrect", room=sid)
    else:
        send("room_does_not_exist", room=sid)


@socket_io.on("check_active_game_room")
def check_active_game_room(data):
    """Check if the user is a part of an active game room, and rejoin if you were"""
    # noinspection PyUnresolvedReferences
    sid = request.sid
    if data:
        room = data.get("room")
        if room in ROOMS:
            if not ROOMS[room].password:
                user_id = data.get("user_id")
                username = data.get("username")
                user = User(username=username, sid=sid, user_id=user_id)
                if ROOMS[room].check_user_id(user_id):
                    ROOMS[room].update_user(user)
                else:
                    ROOMS[room].join(user)
                user_join_room(user, room, sid)
            else:
                send("room_rejoin_password_required", room=sid)


def user_leave_room(user, room):
    ROOMS[room].remove_user(user.user_id)
    # send_chat_message(room, message=f"{user.username} has left the room.")
    emit("room_left", {
        "room": ROOMS[room].json(),
        "user": user.json(),
    }, room=room)
    if ROOMS[room].is_empty:
        del ROOMS[room]
    leave_room(room)


@socket_io.on("leave_game_room")
def leave_game_room(data):
    """Leave a game room"""
    room = data.get("room")
    user_id = data.get("user_id")
    if all([room is not None, user_id is not None, room in ROOMS]):
        user = ROOMS[room].get_user(user_id)
        if user is not None:
            user_leave_room(user, room)


@socket_io.on('disconnect')
def disconnect():
    # noinspection PyUnresolvedReferences
    sid = request.sid
    for room in ROOMS:
        user = ROOMS[room].get_user_with_sid(sid)
        if user is not None:
            user_leave_room(user, room)
            break


def send_chat_message(room, user_id=None, username="System", message="<Insert gibberish here>",
                      timestamp=datetime.utcnow().timestamp() * 1000):
    if room in ROOMS:
        chat_message = {
            "user_id": user_id,
            "username": username,
            "message": message,
            "timestamp": timestamp,
        }
        ROOMS[room].update_chat(chat_message)
        emit("room_chat_update", chat_message, room=room)


@socket_io.on("chat_game_room")
def chat_game_room(data):
    """Save chat data in room"""
    room = data.get("room")
    if room is not None:
        send_chat_message(room, user_id=data.get("user_id", None), username=data.get("username", None),
                          message=data.get("message", None), timestamp=data.get("timestamp", None))

