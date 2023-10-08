from config import Config
import boto3
from botocore.exceptions import NoCredentialsError

CFG = Config()

s3_client = boto3.client(
    service_name='s3',
    region_name='ap-southeast-2',
    aws_access_key_id=CFG.aws_access_key_id,
    aws_secret_access_key=CFG.aws_secret_access_key
)

bucket_name = CFG.aws_s3_bucket_name

def upload_file_to_s3(file_name: str, key: str) -> str:
    """
    Upload file to Amazon S3

    Args:
        file_name (str): the name of the file to upload
        key (str): the name of the file path to upload

    Returns:
        url (str): The URL of the uploaded file
    """
    try:
        s3_client.upload_file(
            Filename=file_name,
            Bucket=bucket_name,
            Key=key,
            ExtraArgs={
                'ContentType': 'application/pdf',
                'ACL': 'public-read',
                'ContentDisposition': 'inline'
            }
        )

        url = f"https://{bucket_name}.s3.amazonaws.com/{key}"

        return url

    except Exception as e:
        return f"Error: {e}"