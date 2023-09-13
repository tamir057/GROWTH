from flask import Flask

app = Flask(__name__)

@app.route("/members")
def members():
    return {"members" : ["Rida", "Tracy", "Tas"]}

if __name__ == "__main__":
    app.run(debug=True)
# 169.254.59.97s (Raspberry Pi IP)