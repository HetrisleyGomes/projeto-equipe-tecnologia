from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__, template_folder="../templates", static_folder="../static")
CORS(app, origins=["*"])
socketio = SocketIO(app, cors_allowed_origins=["https://registro-suporte-ma.onrender.com", "http://172.20.9.251:5000"])

@socketio.on("connect")
def handle_connect():
    print("Client connected")


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


@socketio.on("update_request")
def handle_update_request(data):
    # Broadcast update to all clients
    emit("update", data, broadcast=True)


@socketio.on("message")
def handle_message(data):
    print("received message: " + data)
