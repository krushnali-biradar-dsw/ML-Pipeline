"""
🔥 WORKING CURL COMMANDS FOR MODEL API 🔥

The model API server is running on http://localhost:8080

1. HEALTH CHECK:
===============
PowerShell:
Invoke-RestMethod -Uri "http://localhost:8080/health" -Method GET

Linux/Mac curl:
curl -X GET http://localhost:8080/health

Expected Response:
{
  "status": "healthy",
  "model": "LinearRegressionModel",
  "version": "1.0",
  "coefficients": [1.5, 2.0, 0.5],
  "intercept": 0.1
}

2. SIMPLE PREDICTION:
====================
PowerShell:
$body = '{"data": [1.0, 2.0, 0.5]}' | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8080/predict" -Method POST -Body $body -ContentType "application/json"

Linux/Mac curl:
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"data": [1.0, 2.0, 0.5]}'

Expected Response:
{
  "data": {
    "ndarray": [3.85]
  },
  "meta": {
    "model": "LinearRegressionModel",
    "version": "1.0"
  }
}

3. SELDON FORMAT PREDICTION:
===========================
PowerShell:
$body = '{"data": {"ndarray": [[1.0, 2.0, 0.5], [2.0, 1.0, 1.5]]}}' | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8080/api/v1.0/predictions" -Method POST -Body $body -ContentType "application/json"

Linux/Mac curl:
curl -X POST http://localhost:8080/api/v1.0/predictions \
  -H "Content-Type: application/json" \
  -d '{"data": {"ndarray": [[1.0, 2.0, 0.5], [2.0, 1.0, 1.5]]}}'

Expected Response:
{
  "data": {
    "ndarray": [3.85, 3.85]
  },
  "meta": {
    "model": "LinearRegressionModel",
    "version": "1.0"
  }
}

4. MODEL METADATA:
=================
PowerShell:
Invoke-RestMethod -Uri "http://localhost:8080/api/v1.0/metadata" -Method GET

Linux/Mac curl:
curl -X GET http://localhost:8080/api/v1.0/metadata

Expected Response:
{
  "name": "LinearRegressionModel",
  "versions": ["1.0"],
  "platform": "sklearn",
  "inputs": [{"name": "features", "datatype": "FP32", "shape": ["-1", "3"]}],
  "outputs": [{"name": "predictions", "datatype": "FP32", "shape": ["-1", "1"]}]
}

5. API DOCUMENTATION:
====================
PowerShell:
Invoke-RestMethod -Uri "http://localhost:8080/" -Method GET

Linux/Mac curl:
curl -X GET http://localhost:8080/

🎯 CALCULATION EXAMPLE:
======================
For input [1.0, 2.0, 0.5]:
Prediction = (1.0 * 1.5) + (2.0 * 2.0) + (0.5 * 0.5) + 0.1
           = 1.5 + 4.0 + 0.25 + 0.1
           = 5.85

🚀 YOUR MODEL API IS READY FOR TESTING! 🚀
"""

print(__doc__)