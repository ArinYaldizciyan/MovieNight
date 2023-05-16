from dotenv import load_dotenv
import os
import boto3
from botocore.exceptions import ClientError


class Parameter:
    def __init__(self, prefix="GPT"):
        load_dotenv('.env')
        self.ssm = boto3.client("ssm")
        self.prefix = prefix

    def get_parameter(self, name, from_environment=True):
        if from_environment:
            value = os.environ.get(name)
            if value is not None:
                return value

        try:
            response = self.ssm.get_parameter(
                Name=f"/{self.prefix}/{name}", WithDecryption=True
                )
            return response["Parameter"]["Value"]
        except ClientError as e:
            if e.response["Error"]["Code"] == "ParameterNotFound":
                print(f"Parameter {name} not found in AWS SSM.")
            else:
                print(f"Error: {e}")
            return None
