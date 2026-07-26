from flask import Flask, request, Response
from flask_cors import CORS

app = Flask(__name__)

# Sadece guideon.rf.gd domaininden gelen isteklere izin ver
CORS(app, origins=[
    "http://guideon.rf.gd",
    "https://guideon.rf.gd",
    "http://www.guideon.rf.gd",
    "https://www.guideon.rf.gd"
])

# ... geri kalan NLP ve /chat route kodların
