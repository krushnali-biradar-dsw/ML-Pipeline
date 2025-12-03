import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import os
import time

def main():
    # Configure MinIO/S3 environment variables for MLflow
    os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'http://localhost:9002'
    os.environ['AWS_ACCESS_KEY_ID'] = 'minio'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'minio123'
    
    # Configure MLflow
    mlflow.set_tracking_uri("http://localhost:5001")
    mlflow.set_experiment("simple-mlflow-minio-demo")
    
    print("Loading data...")
    try:
        data = pd.read_csv("data.csv")
        print(f"Data loaded successfully. Shape: {data.shape}")
    except FileNotFoundError:
        print("data.csv not found. Please run 'python generate_data.py' first.")
        return
    
    # Prepare features and target
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]
    
    print(f"Features shape: {X.shape}")
    print(f"Target shape: {y.shape}")
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Start MLflow run
    with mlflow.start_run():
        print("Training Linear Regression model...")
        
        # Train the model
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        # Log parameters
        mlflow.log_param("model_type", "LinearRegression")
        mlflow.log_param("test_size", 0.2)
        mlflow.log_param("random_state", 42)
        mlflow.log_param("n_features", X.shape[1])
        mlflow.log_param("n_samples", X.shape[0])
        
        # Log metrics
        mlflow.log_metric("mse", mse)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2_score", r2)
        mlflow.log_metric("score", model.score(X_test, y_test))
        
        # Log model
        print("Logging model to MLflow...")
        mlflow.sklearn.log_model(
            model, 
            "model",
            registered_model_name="LinearRegressionModel"
        )
        
        # Log additional info
        mlflow.set_tag("dataset", "synthetic_linear_data")
        mlflow.set_tag("algorithm", "sklearn.LinearRegression")
        
        print(f"✅ Model training completed!")
        print(f"📊 Metrics:")
        print(f"   - R² Score: {r2:.4f}")
        print(f"   - RMSE: {rmse:.4f}")
        print(f"   - MSE: {mse:.4f}")
        
        # Get run info
        run = mlflow.active_run()
        print(f"🔗 Run ID: {run.info.run_id}")
        print(f"📦 Model URI: runs:/{run.info.run_id}/model")
        
        # Save model path for Seldon deployment
        model_path = f"{run.info.experiment_id}/{run.info.run_id}/artifacts/model"
        with open("model_path.txt", "w") as f:
            f.write(model_path)
        print(f"💾 Model path saved to model_path.txt: {model_path}")

if __name__ == "__main__":
    main()