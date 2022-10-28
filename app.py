from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def health():
    """Used to test if the app is running"""
    return "hello world"
