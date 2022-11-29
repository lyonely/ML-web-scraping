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
def nutritional_information_for_multiple_products():
    """Takes a POST request with 'url' and 'macro' fields and returns the relevant information"""
    if request.method == 'POST':
        request_data = request.get_json()
        return pipeline.multiple_products(request_data['url'], request_data['macro'])
    return "Error: received GET request instead of POST request"


@app.route('/one_macro', methods=['POST', 'GET'])
def nutritional_information_for_one_product():
    """Takes a POST request with 'url' and 'macro' fields and returns the relevant information"""
    if request.method == 'POST':
        request_data = request.get_json()
        return pipeline.single_product(request_data['url'], request_data['macro'])
    return "Error: received GET request instead of POST request"


@app.route('/one_macro_html', methods=['POST', 'GET'])
def one_product_with_html():
    """Takes a POST request with 'url' and 'macro' fields and returns the relevant information"""
    if request.method == 'POST':
        request_data = request.get_json()
        return pipeline.single_product_html(request_data['url'], request_data['macro'], request_data['html'])
    return "Error: received GET request instead of POST request"
