from flask import Flask

app = Flask(__name__)

@app.route("/")
def health():
    """Used to test if the app is running"""
    return "hello world"
