from flask import Flask

app = Flask(__name__)

@app.route("/")
def health():
    """Used to test if the app is running"""
    return 200

if __name__ == "__main__":
    app.run(debug=True)
