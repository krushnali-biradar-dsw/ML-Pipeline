import boto3
from botocore.client import Config
import time

def create_minio_bucket():
    """Create the mlflow-artifacts bucket in MinIO"""
    
    # Configure MinIO client
    s3_client = boto3.client(
        's3',
        endpoint_url='http://localhost:9002',
        aws_access_key_id='minio',
        aws_secret_access_key='minio123',
        config=Config(signature_version='s3v4'),
        region_name='us-east-1'
    )
    
    bucket_name = 'mlflow-artifacts'
    
    try:
        # Check if bucket exists
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"✅ Bucket '{bucket_name}' already exists")
        
    except Exception as e:
        if '404' in str(e) or 'NoSuchBucket' in str(e):
            # Create bucket
            print(f"📦 Creating bucket '{bucket_name}'...")
            try:
                s3_client.create_bucket(Bucket=bucket_name)
                print(f"✅ Bucket '{bucket_name}' created successfully")
            except Exception as create_error:
                print(f"❌ Error creating bucket: {create_error}")
                return False
        else:
            print(f"❌ Error checking bucket: {e}")
            return False
    
    # List buckets to verify
    try:
        response = s3_client.list_buckets()
        print("📋 Available buckets:")
        for bucket in response['Buckets']:
            print(f"   - {bucket['Name']}")
        return True
        
    except Exception as e:
        print(f"❌ Error listing buckets: {e}")
        return False

if __name__ == "__main__":
    print("🪣 Setting up MinIO bucket for MLflow...")
    
    # Wait a moment for MinIO to be fully ready
    time.sleep(5)
    
    success = create_minio_bucket()
    if success:
        print("✅ MinIO setup completed!")
    else:
        print("❌ MinIO setup failed!")