class AwsConfig:

    def __init__(self, awskey, secretkey, bucket, datapath, chartpath):
        self.Key = awskey
        self.Secret = secretkey
        self.Bucket = bucket
        self.DataPath = datapath
        self.ChartPath = chartpath
