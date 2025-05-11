# backend/main.py

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from leaf_utils import save_image
from gemini_predictor import predict_leaf_description

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

@app.route("/analyze-leaf/", methods=["POST"])
def analyze_leaf():
    if "file" not in request.files:
        return jsonify(error="No file part in request"), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify(error="No file selected"), 400

    try:
        image_path = save_image(file)
        result = predict_leaf_description(image_path)
        return jsonify(result=result)
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
