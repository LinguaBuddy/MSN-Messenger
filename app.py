from flask import Flask, render_template, request, Response, jsonify
from flask_cors import CORS
import time
import json

app = Flask(__name__)
CORS(app)

# Guideon'un Temel Kimliği ve Bilgi Tabanı (Tamamen Anonim)
GUIDEON_CONTEXT = {
    "name": "Guideon",
    "version": "1.0.0-Local",
    "creator": "Geliştirici",
    "role": "Gelişmiş Yerel Yapay Zeka Asistanı"
}

def generate_guideon_response(user_message):
    """
    Dış API kullanmadan sunucu tarafında çalışan Guideon zekası.
    """
    msg = user_message.lower().strip()
    
    # 1. Kimlik ve Selamlaşma
    if any(w in msg for w in ["kimsin", "adin ne", "adın ne", "sen kimsin"]):
        text = f"Ben **{GUIDEON_CONTEXT['name']}**. Tamamen yerel sunucu mimarisi üzerinde çalışan, harici hiçbir API'ye bağımlı olmayan özel yapay zeka asistanıyım."
    
    elif any(w in msg for w in ["selam", "merhaba", "sa", "hey"]):
        text = "Selam! Ben Guideon. Bugün sana nasıl yardımcı olabilirim? Kodlama, sistem analizi veya genel konularda konuşabiliriz."

    elif any(w in msg for w in ["kim yaptı", "geliştirici", "sahibin kim"]):
        text = "Ben bağımsız bir yerel yapay zeka projesiyim."

    # 2. Kod veya Teknik Sorular
    elif "python" in msg or "kod" in msg:
        text = "Python veya yazılım konusunda yardımcı olabilirim. Arka planda çalışan sistemim tamamen Flask ve yerel Python algoritmaları üzerine kurulu. Nasıl bir kod yazmamı istersin?"

    elif "saat" in msg or "zaman" in msg:
        current_time = time.strftime("%H:%M:%S")
        text = f"Şu anki sunucu saati: **{current_time}**"

    # 3. Genel/Varsayılan Zeka Mantığı
    else:
        text = f"'{user_message}' konusunu analiz ettim. Dış API kullanmadan çalışan yerel çekirdeğimle bu isteği işliyorum. Sana bu konuda nasıl destek olmamı istersin?"

    # Harf harf akış (Streaming)
    for char in text:
        yield char
        time.sleep(0.015)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    return Response(generate_guideon_response(user_message), mimetype='text/plain; charset=utf-8')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
