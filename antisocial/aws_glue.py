from typing import Union

import boto3


# Since I import this during Django settings startup, I can't put my
# site-specific constants in Django settings.
# TODO: Minimize the number of files that have to be edited to spin up an
# instance.
AWS_REGION = "us-east-2"

def get_secret(secret_id: str) -> Union[str, bytes]:
    secrets_client = boto3.client('secretsmanager')
    response = secrets_client.get_secret_value(SecretId=secret_id)
    return response.get('SecretString',
        base64.standard_b64decode(response['SecretBinary']))
