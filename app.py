import os
import re
from flask import Flask, request, Response
from flask_cors import CORS
from duckduckgo_search import DDGS

app = Flask(__name__)

# InfinityFree sitenden gelen isteklere izin veriyoruz
CORS(app, origins=[
    "http://guideon.rf.gd",
    "https://guideon.rf.gd",
    "http://www.guideon.rf.gd",
    "https://www.guideon.rf.gd"
])

def replace_branding(text):
    """
    Model yanıtlarında geçebilecek rakip marka isimlerini 'Guideon' ile değiştirir.
    """
    pattern = re.compile(r'\b(chatgpt|openai|llama|meta|mistral|claude|gpt-4|gpt-3\.5|duckduckgo)\b', re.IGNORECASE)
    return pattern.sub('Guideon', text)

def generate_guideon_response(user_message):
    try:
        # DDGS istemcisini başlatıyoruz (API Key gerektirmez)
        ddgs = DDGS()
        
        prompt = f"Senin adın Guideon. Sen Guideon AI adında yardımcı bir yapay zekasın. Kendini hiçbir zaman başka bir model olarak tanıtma. Sadece Guideon olarak Türkçe yanıt ver. Kullanıcının sorusu: {user_message}"
        
        # DuckDuckGo'nun ücretsiz AI Chat API'sini çağırıyoruz
        results = ddgs.chat(prompt, model='gpt-4o-mini')
        
        cleaned_text = replace_branding(results)
        yield cleaned_text

    except Exception as e:
        yield f"Guideon şu an yanıt veremiyor: {str(e)}"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    user_message = data.get('message', '')

    if not user_message:
        return Response("Mesaj boş olamaz.", status=400)

    return Response(
        generate_guideon_response(user_message),
        mimetype='text/plain; charset=utf-8'
    )

@app.route('/', methods=['GET'])
def home():
    return "Guideon AI Backend Çalışıyor!", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
