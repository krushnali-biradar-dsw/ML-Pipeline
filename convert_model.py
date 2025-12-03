import pickle
import joblib
import boto3
from botocore.client import Config
import tempfile
import os

def convert_mlflow_model_to_joblib():
    """Download MLflow model and convert to joblib format for Seldon sklearn server"""
    
    # Configure MinIO client
    s3_client = boto3.client(
        's3',
        endpoint_url='http://localhost:9002',
        aws_access_key_id='minio',
        aws_secret_access_key='minio123',
        config=Config(signature_version='s3v4'),
        region_name='us-east-1'
    )
    
    model_key = "1/models/m-7dbf8b977c304f6fbc9687d81e7ae6dd/artifacts/model.pkl"
    
    print("🔄 Downloading model from MinIO...")
    
    # Download the pickle file
    with tempfile.NamedTemporaryFile() as tmp_file:
        s3_client.download_file('mlflow-artifacts', model_key, tmp_file.name)
        
        # Load the pickle model
        with open(tmp_file.name, 'rb') as f:
            model = pickle.load(f)
        
        print(f"✅ Model loaded: {type(model)}")
        
        # Save as joblib format
        joblib_path = "model.joblib"
        joblib.dump(model, joblib_path)
        print(f"✅ Model saved as {joblib_path}")
        
        # Upload back to MinIO in a simpler format
        simple_model_key = "simple-linear-model/model.joblib"
        s3_client.upload_file(joblib_path, 'mlflow-artifacts', simple_model_key)
        print(f"✅ Uploaded to MinIO as {simple_model_key}")
        
        # Clean up
        os.remove(joblib_path)
        
        return simple_model_key

if __name__ == "__main__":
    try:
        model_path = convert_mlflow_model_to_joblib()
        print(f"🎉 Success! Use model path: {model_path}")
        
        # Save the simple model path for deployment
        with open("simple_model_path.txt", "w") as f:
            f.write(model_path)
        print("💾 Simple model path saved to simple_model_path.txt")
        
    except Exception as e:
        print(f"❌ Error: {e}")