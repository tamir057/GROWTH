from flask import Flask

from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route("/members")
def members():
    return {"members" : ["Rida", "Tracy", "Tas"]}

if __name__ == "__main__":
    app.run(debug=True)
# 169.254.59.97s (Raspberry Pi IP)