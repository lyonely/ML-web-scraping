import logging
from flask import Flask, request
from flask_cors import CORS

from backend.pipeline import main

app = Flask(__name__)
CORS(app)

logging.critical("Flask app started running")

@app.route("/")
def health():
    """Used to test if the app is running"""
    return "Hello World"


@app.route('/macro', methods=['POST', 'GET'])
def login():
    """Takes a POST request with 'url' and 'macro' fields and returns the relevant information"""
    if request.method == 'POST':
        if request.form['url'] and request.form['macro']:
            return main(request.form['url'], request.form['macro'])
    return "Error: received GET request instead of POST request"
