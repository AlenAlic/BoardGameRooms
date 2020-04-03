from flask_socketio import SocketIO


socket_io = SocketIO()


def init_app(app):
    from .test import socket as test
    from .room import socket as room
    from .games import socket as games
    socket_io.init_app(app, cors_allowed_origins="*")
