import boto3
import botocore


class S3:

    def __init__(self, key, secret, bucket):
        self.Key = key
        self.Secret = secret
        self.Bucket = bucket
        return

    def upload_file(self, local_file, remote_file):
        s3 = boto3.resource(
            's3',
            aws_access_key_id=self.Key,
            aws_secret_access_key=self.Secret)

        try:
            s3.Bucket(self.Bucket).upload_file(local_file, remote_file)

        except botocore.exceptions.ClientError as e:

            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise

    def download_file(self, remote_file, local_file):
        s3 = boto3.resource('s3')

        try:
            s3.Bucket(self.Bucket).download_file(remote_file, local_file)

        except botocore.exceptions.ClientError as e:

            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise
