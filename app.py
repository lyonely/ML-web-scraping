from flask import Flask, request
from flask_cors import CORS

from backend.pipeline import products_to_macro_json

app = Flask(__name__)
CORS(app)


@app.route("/")
def health():
    """Used to test if the app is running"""
    return "hello world"


@app.route('/macro', methods=['POST', 'GET'])
def login():
    """Takes a POST request with 'url' and 'macro' fields and returns the relevant information"""
    if request.method == 'POST':
        if request.form['url'] and request.form['macro']:
            return products_to_macro_json(request.form['url'], request.form['macro'])
    return "Error: received GET request instead of POST request"
