from backend import create_app
from backend.socket import socket_io


app = create_app()


if __name__ == '__main__':
    socket_io.run(app, host='0.0.0.0', port=5000)
