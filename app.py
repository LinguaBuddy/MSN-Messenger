from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# async_mode='threading' ekledik
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

@app.route('/')
def index():
    return "MSN Messenger Backend Sunucusu Çalışıyor!"

@socketio.on('connect')
def handle_connect():
    print("Bir kullanıcı bağlandı!")

@socketio.on('send_message')
def handle_message(data):
    emit('receive_message', data, broadcast=True)

@socketio.on('send_nudge')
def handle_nudge(data):
    emit('receive_nudge', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
