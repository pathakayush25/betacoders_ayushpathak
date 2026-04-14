from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow frontend to call backend

@app.route("/")
def home():
    return "OPTIWEALTH backend is running"

@app.route("/optimize", methods=["POST"])
def optimize():
    data = request.json
    stocks = data.get("stocks", [])
    budget = data.get("budget", 0)

    # dummy logic (replace with Qiskit later)
    result = {
        "return": 15.5,
        "risk": 40
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)