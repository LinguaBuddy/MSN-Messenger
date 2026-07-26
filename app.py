import os
import re
from flask import Flask, request, Response
from flask_cors import CORS
from huggingface_hub import InferenceClient

app = Flask(__name__)

CORS(app, origins=[
    "http://guideon.rf.gd",
    "https://guideon.rf.gd",
    "http://www.guideon.rf.gd",
    "https://www.guideon.rf.gd"
])

# Bulutta çalışan ücretsiz açık kaynak model (PC'ni HİÇBİR ŞEKİLDE yormaz)
client = InferenceClient("mistralai/Mistral-7B-Instruct-v0.2")

def replace_branding(text):
    """
    Modelin ağzından kaçabilecek marka isimlerini Guideon ile değiştirir.
    """
    pattern = re.compile(r'\b(ollama|llama|meta|mistral|chatgpt|openai)\b', re.IGNORECASE)
    return pattern.sub('Guideon', text)

def generate_guideon_response(user_message):
    messages = [
        {"role": "system", "content": "Senin adın Guideon. Sen Guideon AI adında yardımcı bir yapay zekasın. Kendini hiçbir zaman başka bir model veya marka olarak tanıtma, her zaman Guideon olarak yanıt ver."},
        {"role": "user", "content": user_message}
    ]

    try:
        # Buluttan kelime kelime yanıt çekme
        response_stream = client.chat_completion(
            messages=messages,
            max_tokens=500,
            stream=True
        )

        for chunk in response_stream:
            if chunk.choices and chunk.choices[0].delta.content:
                raw_text = chunk.choices[0].delta.content
                # Marka isimlerini anında 'Guideon' olarak sansürleyip gönder
                cleaned_text = replace_branding(raw_text)
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
