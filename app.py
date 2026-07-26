from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
# InfinityFree ve dışarıdan gelen isteklere izin veriyoruz
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return "MSN Messenger Server Çalışıyor!"

# Kullanıcı bağlandığında
@socketio.on('connect')
def handle_connect():
    print("Bir kullanıcı bağlandı!")

# Mesaj geldiğinde herkese anında ilet
@socketio.on('send_message')
def handle_message(data):
    emit('receive_message', data, broadcast=True)

# Titreşim (Nudge) geldiğinde herkesin ekranını salla
@socketio.on('send_nudge')
def handle_nudge(data):
    emit('receive_nudge', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)