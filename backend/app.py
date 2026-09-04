from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import os

app = Flask(__name__)

# Allow frontend requests
CORS(app)

# Get current backend folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Model path
MODEL_PATH = os.path.join(BASE_DIR, "house_price_model.pkl")

# Load trained model
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        "house_price_model.pkl not found. Run train_model.py first."
    )

model = joblib.load(MODEL_PATH)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "message": "AI House Price Prediction API is running!",
        "status": "live"
    })


@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        required_fields = [
            "area",
            "bedrooms",
            "bathrooms",
            "parking"
        ]

        # Check fields
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "success": False,
                    "error": f"Missing field: {field}"
                }), 400

        # Convert user input to DataFrame
        input_data = pd.DataFrame([{
            "area": float(data["area"]),
            "bedrooms": int(data["bedrooms"]),
            "bathrooms": int(data["bathrooms"]),
            "parking": int(data["parking"])
        }])

        # Prediction
        prediction = model.predict(input_data)[0]

        return jsonify({
            "success": True,
            "predicted_price": round(float(prediction), 2),
            "formatted_price": f"₹{prediction:,.0f}"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )