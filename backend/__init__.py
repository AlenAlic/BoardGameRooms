import eventlet
from flask import Flask
from config import Config


def create_app(config_class=Config):

    # Create and configure the app
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.url_map.strict_slashes = False

    @app.route("/ping")
    def ping():
        """Ping the server"""
        return "Board Game Rooms server reachable"

    # Import routes
    from backend import socket
    socket.init_app(app)

    return app
