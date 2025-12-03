
from flask import Flask, jsonify, request
import pickle
import numpy as np

app = Flask(__name__)

# Mock model for demo
class SimpleModel:
    def predict(self, X):
        return [sum(x) * 1.5 + 0.1 for x in X] if len(X) > 0 and isinstance(X[0], list) else [sum(X) * 1.5 + 0.1]

model = SimpleModel()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "model": "LinearRegression"})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        predictions = model.predict(data.get('data', []))
        return jsonify({"predictions": predictions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
