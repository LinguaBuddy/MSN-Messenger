import os
import time
from flask import Flask, request, Response
from flask_cors import CORS

app = Flask(__name__)

# Sadece senin InfinityFree domaininden gelen isteklere izin veriyoruz
CORS(app, origins=[
    "http://guideon.rf.gd",
    "https://guideon.rf.gd",
    "http://www.guideon.rf.gd",
    "https://www.guideon.rf.gd"
])

def generate_ai_response(user_message):
    """
    Burada yanıtı parça parça (stream) üretiyoruz.
    Şu an örnek/test yanıtı veriyor. Kendi model/NLP mantığını 
    buraya entegre edebilirsin.
    """
    reply_text = f"Guideon AI yanıtı: '{user_message}' mesajınızı aldım. Size nasıl yardımcı olabilirim?"
    
    # Kelime kelime veya harf harf akış simülasyonu
    for word in reply_text.split(" "):
        yield word + " "
        time.sleep(0.08)  # Yazma efekti hızı

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    user_message = data.get('message', '')

    if not user_message:
        return Response("Mesaj boş olamaz.", status=400)

    # Yanıtı stream (akış) olarak gönderiyoruz
    return Response(
        generate_ai_response(user_message),
        mimetype='text/plain; charset=utf-8'
    )

@app.route('/', methods=['GET'])
def home():
    return "Guideon AI Backend Çalışıyor!", 200

if __name__ == '__main__':
    # Render'ın atadığı dinamik PORT'u alıyoruz
    # host='0.0.0.0' olmak ZORUNDADIR (Render kapanma hatasını çözen kısım)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
