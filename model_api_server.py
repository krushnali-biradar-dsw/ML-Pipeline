#!/usr/bin/env python3
"""
Model API Server that loads trained model from MLflow
"""
from flask import Flask, jsonify, request
import json
import numpy as np
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

app = Flask(__name__)

class MLflowModelLoader:
    """Load trained model from MLflow registry"""
    def __init__(self):
        self.model = None
        self.model_name = "LinearRegressionModel"
        self.version = "1"
        self.coefficients = None
        self.intercept = None
        self.load_model()

    def load_model(self):
        """Load the trained model from MLflow"""
        try:
            print(f"🔄 Loading model '{self.model_name}' version {self.version} from MLflow...")

            # Set MinIO/S3 environment variables
            import os
            os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'http://localhost:9002'
            os.environ['AWS_ENDPOINT_URL'] = 'http://localhost:9002'
            os.environ['AWS_ACCESS_KEY_ID'] = 'minioadmin'
            os.environ['AWS_SECRET_ACCESS_KEY'] = 'minioadmin'
            os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

            # Try loading from run artifacts directly
            print("📍 Trying to load from run artifacts...")
            run_id = '860a6755aeef435dbd9eef30c7a195de'  # From earlier output
            model_uri = f"runs:/{run_id}/model"

            print(f"📍 Model URI: {model_uri}")

            # Load the model
            self.model = mlflow.sklearn.load_model(model_uri)

            # Extract coefficients and intercept for display
            if hasattr(self.model, 'coef_'):
                self.coefficients = self.model.coef_.tolist() if hasattr(self.model.coef_, 'tolist') else self.model.coef_
            if hasattr(self.model, 'intercept_'):
                self.intercept = float(self.model.intercept_)

            print("✅ Model loaded successfully from run artifacts!")
            print(f"📊 Coefficients: {self.coefficients}")
            print(f"📊 Intercept: {self.intercept}")

        except Exception as e:
            print(f"❌ Failed to load model from run: {e}")
            print("⚠️ Using fallback mock model...")
            self._use_mock_model()

    def _use_mock_model(self):
        """Fallback to mock model if MLflow loading fails"""
        from sklearn.linear_model import LinearRegression
        self.model = LinearRegression()
        self.model.coef_ = np.array([1.5, 2.0, 0.5])
        self.model.intercept_ = 0.1
        self.coefficients = self.model.coef_.tolist()
        self.intercept = float(self.model.intercept_)

    def predict(self, X):
        """Make predictions using loaded model"""
        if self.model is None:
            return [0.0]

        # Convert input to numpy array
        if isinstance(X, list):
            X = np.array(X)

        # Handle single sample vs batch
        if X.ndim == 1:
            X = X.reshape(1, -1)

        predictions = self.model.predict(X)
        return predictions.tolist()

# Initialize model loader
model_loader = MLflowModelLoader()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model": model_loader.model_name,
        "version": model_loader.version,
        "coefficients": model_loader.coefficients,
        "intercept": model_loader.intercept,
        "source": "MLflow Registry" if model_loader.model else "Mock Fallback"
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Prediction endpoint compatible with Seldon format"""
    try:
        data = request.get_json()
        
        # Handle both Seldon format and simple format
        if 'data' in data:
            input_data = data['data']
        elif 'ndarray' in data:
            input_data = data['ndarray']
        else:
            return jsonify({"error": "Missing 'data' or 'ndarray' field"}), 400
            
        predictions = model_loader.predict(input_data)
        
        # Return in Seldon-compatible format
        return jsonify({
            "data": {
                "ndarray": predictions
            },
            "meta": {
                "model": model_loader.model_name,
                "version": model_loader.version
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1.0/predictions', methods=['POST'])
def seldon_predict():
    """Seldon-compatible prediction endpoint"""
    try:
        data = request.get_json()
        
        # Seldon format: {"data": {"ndarray": [[1,2,3]]}}
        if 'data' in data and 'ndarray' in data['data']:
            input_data = data['data']['ndarray']
        else:
            return jsonify({"error": "Expected Seldon format: {'data': {'ndarray': [[...]]}}"}), 400
            
        predictions = model_loader.predict(input_data)
        
        return jsonify({
            "data": {
                "ndarray": predictions
            },
            "meta": {
                "model": model_loader.model_name,
                "version": model_loader.version
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1.0/metadata', methods=['GET'])
def metadata():
    """Model metadata endpoint"""
    return jsonify({
        "name": model_loader.model_name,
        "versions": [model_loader.version],
        "platform": "sklearn",
        "inputs": [{"name": "features", "datatype": "FP32", "shape": ["-1", "3"]}],
        "outputs": [{"name": "predictions", "datatype": "FP32", "shape": ["-1", "1"]}]
    })

@app.route('/', methods=['GET'])
def root():
    """API documentation"""
    return jsonify({
        "message": "Linear Regression Model API",
        "version": model_loader.version,
        "endpoints": {
            "GET /health": "Health check",
            "POST /predict": "Make predictions (simple format)",
            "POST /api/v1.0/predictions": "Make predictions (Seldon format)",
            "GET /api/v1.0/metadata": "Model metadata"
        },
        "curl_examples": {
            "health": "curl -X GET http://localhost:8080/health",
            "simple_predict": 'curl -X POST http://localhost:8080/predict -H "Content-Type: application/json" -d \'{"data": [1.0, 2.0, 0.5]}\'',
            "seldon_predict": 'curl -X POST http://localhost:8080/api/v1.0/predictions -H "Content-Type: application/json" -d \'{"data": {"ndarray": [[1.0, 2.0, 0.5]]}}\''
        }
    })

if __name__ == '__main__':
    print("🚀 Starting Linear Regression Model API Server...")
    print("📊 Model coefficients:", model_loader.coefficients)
    print("📊 Model intercept:", model_loader.intercept)
    print("🌐 Server starting on http://0.0.0.0:8080")
    print("\n📋 Available endpoints:")
    print("   GET  /health - Health check")
    print("   POST /predict - Simple predictions")
    print("   POST /api/v1.0/predictions - Seldon format predictions")
    print("   GET  /api/v1.0/metadata - Model metadata")
    print()

    app.run(host='0.0.0.0', port=8080, debug=False)