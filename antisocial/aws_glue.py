import base64
import json
from typing import Union

import boto3


# Since I import this during Django settings startup, I can't put my
# site-specific constants in Django settings.
# TODO: Minimize the number of files that have to be edited to spin up an
# instance.
AWS_REGION = "us-east-2"

def get_secret(secret_id: str) -> Union[str, bytes]:
    secrets_client = boto3.client('secretsmanager', region_name=AWS_REGION)
    response = secrets_client.get_secret_value(SecretId=secret_id)
    secret_text = response.get('SecretString')
    if secret_text is not None:
        return secret_text
    else:
        return base64.standard_b64decode(response['SecretBinary'])

def get_value_from_json_secret(secret_id: str, json_key:str):
    secret_text = get_secret(secret_id)
    parsed = json.loads(secret_text)
    return parsed[json_key]
