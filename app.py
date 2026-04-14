from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

# Try importing yfinance safely
try:
    import yfinance as yf
    import pandas as pd
except ImportError:
    yf = None

app = Flask(__name__)   # ✅ CORRECT
CORS(app)

@app.route("/")
def home():
    return "OPTIWEALTH backend running ✅"

@app.route("/optimize", methods=["POST"])
def optimize():
    try:
        data = request.json
        stocks = data.get("stocks", [])
        budget = data.get("budget", 0)

        if len(stocks) < 2:
            return jsonify({"error": "Minimum 2 stocks required"}), 400

        if yf is None:
            return jsonify({"error": "yfinance not installed"}), 500

        # Convert to Yahoo Finance format (for Indian stocks)
        stocks_yf = [s + ".NS" for s in stocks]

        # Fetch stock data
        prices = yf.download(stocks_yf, period="1y")["Close"]

        if prices.empty:
            return jsonify({"error": "Invalid stock symbols"}), 400

        # Calculate returns
        returns = prices.pct_change().dropna()
        mean_returns = returns.mean()
        cov_matrix = returns.cov()

        # Generate random weights (you can replace with Qiskit later)
        weights = np.random.dirichlet(np.ones(len(stocks)))

        # Portfolio calculations
        portfolio_return = float(np.dot(weights, mean_returns) * 252)
        portfolio_risk = float(np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252))

        # Allocation
        allocation = {
            stocks[i]: float(weights[i] * budget)
            for i in range(len(stocks))
        }

        return jsonify({
            "stocks": stocks,
            "weights": weights.tolist(),
            "return": portfolio_return,
            "risk": portfolio_risk,
            "allocation": allocation,
            "latest_prices": prices.iloc[-1].to_dict()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ VERY IMPORTANT (correct underscores)
if __name__ == "__main__":
    app.run(debug=True)
