from backend.socket import socket_io
from flask_socketio import emit
from flask import request
from backend.games import GAMES_LIST, get_game
from backend.socket.room import ROOMS


@socket_io.on('game_get_list')
def game_get_list():
    # noinspection PyUnresolvedReferences
    sid = request.sid
    emit("game_list", sorted([game().preview() for game in GAMES_LIST], key=lambda x: x["name"]), room=sid)


@socket_io.on('game_create')
def game_create(data):
    game = get_game(data.get("tag"))
    room = data.get("room")
    ROOMS[room].create_game(game, data.get("users"))
    emit("game_new", ROOMS[room].game.json(), room=room)


@socket_io.on('game_action')
def game_action(data):
    room = data.get("room")
    action = data.get("action")
    action_data = data.get("data")
    ROOMS[room].game.action(action, action_data)
    emit("game_update", ROOMS[room].game.json(), room=room)


@socket_io.on('game_stop')
def game_stop(room):
    ROOMS[room].stop_game()
    emit("game_update", ROOMS[room].game.json(), room=room)


@socket_io.on('game_leave')
def game_leave(data):
    room = data.get("room")
    user_id = data.get("user_id")
    ROOMS[room].game.deactivate_user(user_id)
    emit("game_update", ROOMS[room].game.json(), room=room)


@socket_io.on('game_rejoin')
def game_rejoin(data):
    room = data.get("room")
    user_id = data.get("user_id")
    user = ROOMS[room].get_user(user_id)
    if user is not None:
        ROOMS[room].game.rejoin(user)
        emit("game_update", ROOMS[room].game.json(), room=room)
