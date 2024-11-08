import boto3
import json
import botocore.exceptions
from typing import Dict

def fetch_secrets(secret_name: str) -> Dict[str, str]:
    """Fetch secrets from AWS Secrets Manager."""
    region_name = "us-east-1"  # Change this to your region

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        
        # Secrets can be either in 'SecretString' or 'SecretBinary'
        if "SecretString" in get_secret_value_response:
            secret = get_secret_value_response["SecretString"]
        else:
            secret = get_secret_value_response["SecretBinary"]
            secret = secret.decode("utf-8")

        # Parse the secret string into a dictionary
        return json.loads(secret)
    
    except botocore.exceptions.ClientError as e:
        raise Exception(f"Failed to retrieve secret {secret_name}: {str(e)}")
