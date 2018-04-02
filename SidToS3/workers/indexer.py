from aws.s3 import S3
from workers.s3loader import S3Loader

class Indexer:

    def __init__(self, config):
        self.Config = config

        return

    def index_new_files(self, processed_files):
        s3 = S3(
            self.Config.AWS.Key,
            self.Config.AWS.Secret,
            self.Config.AWS.Bucket)

        s3_loader = S3Loader(s3)

        # todo
        # for each processed file
        #   Is the index file already in memory
        #   No - pull file from server
        #        deserialize into dataindex and datafile
        #        add to local collection
        #   Is file and chart already in the index
        #   No - add file to index
        # for each index file
        #    serialize to json
        #    save to s3

        return