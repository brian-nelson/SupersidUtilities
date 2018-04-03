class AwsConfig:

    def __init__(self, awskey, secretkey, bucket, supersid_path):
        self.Key = awskey
        self.Secret = secretkey
        self.Bucket = bucket
        self.SupersidPath = supersid_path
