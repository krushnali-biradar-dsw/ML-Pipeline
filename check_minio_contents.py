import boto3
from botocore.client import Config

# Configure MinIO client
s3_client = boto3.client(
    's3',
    endpoint_url='http://localhost:9002',
    aws_access_key_id='minio',
    aws_secret_access_key='minio123',
    config=Config(signature_version='s3v4'),
    region_name='us-east-1'
)

# List objects in the bucket
try:
    response = s3_client.list_objects_v2(Bucket='mlflow-artifacts')
    
    if 'Contents' in response:
        print("Objects in mlflow-artifacts bucket:")
        for obj in response['Contents']:
            print(f"  {obj['Key']}")
    else:
        print("No objects found in bucket")
        
except Exception as e:
    print(f"Error: {e}")