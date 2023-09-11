from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World 12345!</p>"

app.run(host="0.0.0.0")
# 169.254.59.97