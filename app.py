from flask import Flask, render_template, request, Response
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time
import os

app = Flask(__name__)
CORS(app)

# Guideon Bilgi / Hafıza Tabanı
KNOWLEDGE_BASE = [
    "Guideon yerel ve bağımsız çalışan bir yapay zeka asistanıdır.",
    "Harici hiçbir API veya ücretli servis kullanmadan kendi çekirdeğiyle yanıt üretir.",
    "Yazılım, kodlama, sistem mimarisi ve algoritma konularında analiz yapabilir.",
    "Render ve GitHub altyapısı üzerinde canlı olarak barındırılabilir.",
    "Kullanıcının yazdığı metinleri doğal dil işleme teknikleriyle analiz eder."
]

def generate_dynamic_response(user_input):
    """
    Hazır cevap içermez. Kullanıcı cümlesini vektör uzayına taşır
    ve dinamik olarak yanıtı oluşturur.
    """
    documents = KNOWLEDGE_BASE + [user_input]
    vectorizer = TfidfVectorizer().fit_transform(documents)
    vectors = vectorizer.toarray()
    
    user_vector = vectors[-1]
    base_vectors = vectors[:-1]
    
    similarities = cosine_similarity([user_vector], base_vectors)[0]
    best_match_idx = similarities.argmax()
    score = similarities[best_match_idx]

    if score > 0.15:
        response = f"**Guideon Analizi:** {KNOWLEDGE_BASE[best_match_idx]}"
    else:
        words = [w for w in user_input.split() if len(w) > 2]
        keywords = ", ".join(words) if words else "girdi"
        response = f"'{keywords}' konusundaki girdini analiz ettim. Dış API kullanmadan yerel NLU motorumla bunu işliyorum."

    # Harf harf canlı akış efekti (Streaming)
    for char in response:
        yield char
        time.sleep(0.012)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}
    user_message = data.get("message", "")
    return Response(generate_dynamic_response(user_message), mimetype='text/plain; charset=utf-8')

if __name__ == "__main__":
    # Render ortamındaki portu otomatik alır
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
