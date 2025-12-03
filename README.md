# Linear Pipeline

Small end-to-end ML pipeline that demonstrates training, artifact storage (MinIO), MLflow tracking, and model serving (Seldon Core / local test server).

Quick overview
- MLflow server and MinIO are orchestrated via `docker-compose.yml`.
- Training and model logging are in `train.py` (writes artifacts to MLflow/MinIO).
- Kubernetes/Seldon deployment manifests are under `seldon-*.yaml` and `simple-deployment.yaml`.
- A local test model API is available at `model_api_server.py` for quick curl testing.

Prerequisites
- Docker & Docker Compose
- Minikube (if you want to use Seldon Core locally)
- Python 3.10+ and a virtual environment (`.venv` present in repo)
- `pip` packages: `mlflow`, `flask`, `scikit-learn`, `boto3`, `pandas`, `numpy` (install into `.venv`)

Quick start (development/testing)
1. Activate Python venv (PowerShell):

```
.\.venv\Scripts\Activate.ps1
```

2. Start MLflow + MinIO (Docker Compose):

```
docker-compose up -d
```

3. (Optional) Create MinIO bucket used by MLflow:

```
python setup_minio_bucket.py
```

4. Run training (logs model to MLflow + MinIO):

```
python generate_data.py
python train.py
```

5. Run local model API server (loads from MLflow if available):

```
python model_api_server.py
```

6. Test predictions (PowerShell):

```
#$ health
Invoke-RestMethod -Uri "http://localhost:8080/health" -Method GET

#$ Seldon-format prediction
$body = '{"data": {"ndarray": [[1.0, 2.0, 0.5]]}}'
Invoke-RestMethod -Uri "http://localhost:8080/api/v1.0/predictions" -Method POST -Body $body -ContentType "application/json"
```

Notes
- MinIO console: `http://localhost:9003` (default credentials used in code: `minioadmin`/`minioadmin`).
- MLflow UI: `http://localhost:5001`
- If you prefer to test without MLflow/Seldon, use `model_api_server.py` which falls back to a mock model if MLflow is unavailable.
- Consider adding a `.gitignore` that excludes `minio-data/` and other runtime artifacts before pushing final history.

Files of interest
- `docker-compose.yml` — MLflow + MinIO
- `train.py` — training + MLflow logging
- `setup_minio_bucket.py` — creates required bucket in MinIO
- `model_api_server.py` — local API that loads MLflow model (or falls back)
- `seldon-deployment-final.yaml` — example SeldonDeployment manifest
- `run_pipeline.py` — single-file pipeline runner (development/testing)

License
- None provided. Use as you like.
