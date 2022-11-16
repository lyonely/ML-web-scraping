from flask import Flask, request
from flask_cors import CORS

import backend.pipeline

app = Flask(__name__)
CORS(app, supports_credentials=True)

pipeline = backend.pipeline.Pipeline()

@app.route("/")
def health():
    """Used to test if the app is running"""
    return "hello world"


@app.route('/macro', methods=['POST', 'GET'])
def login():
    """Takes a POST request with 'url' and 'macro' fields and returns the relevant information"""
    if request.method == 'POST':
        request_data = request.get_json()
        return pipeline.main(request_data['url'],
                             request_data['macro'])
    return "Error: received GET request instead of POST request"
